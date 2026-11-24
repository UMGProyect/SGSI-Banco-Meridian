"""Variante educativa distribuida. Servicios solo loopback; TLS y túnel SSH/IAP.
No es aplicación bancaria productiva ni MFA real. No publicar configuración runtime.
"""
import argparse, json, os, ssl, secrets, time, threading
from pathlib import Path
from contextlib import contextmanager, ExitStack
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from hashlib import sha256
from datetime import timedelta
from ipaddress import ip_address
from hmac import compare_digest
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
import laboratorio_meridian as orig

HOST='127.0.0.1'

def write_private(path, data):
    with path.open('xb') as f:
        try: os.chmod(path, 0o600)
        except OSError: pass
        f.write(data)

def prepare(root):
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    local=root/'local'; cloud=root/'cloud'; local.mkdir(mode=0o700); cloud.mkdir(mode=0o700)
    cfg={k:secrets.token_urlsafe(32) for k in ('key','normal','stronger','admin')}
    for directory in (local,cloud):
        write_private(directory/'config.json',json.dumps(cfg).encode())
        key=ec.generate_private_key(ec.SECP256R1()); now=orig.utc_now()
        name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Meridian '+directory.name)])
        cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now-timedelta(minutes=2))
            .not_valid_after(now+timedelta(hours=12))
            .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ip_address(HOST))]),critical=False)
            .sign(key,hashes.SHA256()))
        write_private(directory/'key.pem',key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        (directory/'cert.pem').write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    (local/'peer.pem').write_bytes((cloud/'cert.pem').read_bytes()); (cloud/'peer.pem').write_bytes((local/'cert.pem').read_bytes())
    print('Configuración generada. Copiar únicamente cloud al servidor; nunca a Git.')

def contexts(root):
    server=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); server.minimum_version=ssl.TLSVersion.TLSv1_2
    server.load_cert_chain(root/'cert.pem',root/'key.pem')
    client=ssl.create_default_context(cafile=str(root/'peer.pem')); client.minimum_version=ssl.TLSVersion.TLSv1_2
    return server,client

class Server(ThreadingHTTPServer):
    daemon_threads=True
    allow_reuse_address=True
    def get_request(self):
        sock, addr=super().get_request(); sock.settimeout(6); return sock,addr

@contextmanager
def serve(port,context,app):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 2<=size<=2048: raise ValueError('size')
                body=json.loads(self.rfile.read(size))
                if not isinstance(body,dict): raise ValueError('body')
                status,result=app(self.path,self.headers,body)
            except (ValueError,TypeError,KeyError): status,result=400,{'resultado':'solicitud_invalida'}
            data=json.dumps(result,ensure_ascii=False).encode()
            self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
        def log_message(self,*args): pass
    with Server((HOST,port),Handler) as srv:
        srv.socket=context.wrap_socket(srv.socket,server_side=True)
        t=threading.Thread(target=srv.serve_forever,kwargs={'poll_interval':.05},daemon=True); t.start()
        try: yield srv.server_port
        finally: srv.shutdown(); t.join(5)

class EventLog(list):
    def append(self,event):
        super().append(event)
        # Structured stdout; no credentials; synthetic data only.
        print(json.dumps(event,ensure_ascii=False),flush=True)

def gateway(root,port,core_port):
    cfg=json.loads((root/'config.json').read_text()); server,client=contexts(root)
    events=EventLog(); base_send=orig.send
    def safe_send(*args,**kwargs):
        try: return base_send(*args,**kwargs)
        except (OSError, ssl.SSLError):
            return 503,{'resultado':'adaptador_no_disponible'},None
    # A network failure must never generate a confirmed transfer.
    import http.client
    def resilient_send(*args,**kwargs):
        try: return safe_send(*args,**kwargs)
        except http.client.HTTPException: return 503,{'resultado':'adaptador_no_disponible'},None
    orig.send=resilient_send
    handle=orig.gateway(core_port,client,cfg['key'],{cfg['normal']:('cliente-a',False),cfg['stronger']:('cliente-a',True)},events)
    def app(path,headers,body):
        if path=='/__lab/events':
            if not compare_digest(headers.get('X-Lab-Admin',''),cfg['admin']): return 403,{'resultado':'denegado'}
            return 200,{'eventos':list(events)}
        return handle(path,headers,body)
    with serve(port,server,app):
        print(f'API HTTPS lista en loopback:{port}',flush=True)
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt: pass

def test(root,api_port,core_port,output):
    cfg=json.loads((root/'config.json').read_text()); server,api_client=contexts(root)
    core_client=ssl.create_default_context(cafile=str(root/'cert.pem')); core_client.minimum_version=ssl.TLSVersion.TLSv1_2
    key,normal,stronger=(cfg[k] for k in ('key','normal','stronger'))
    tests=[]; events=[]; start_utc=orig.utc_now().isoformat()
    def record(identifier,expected,observed,success):
        tests.append({'id':identifier,'esperado':expected,'observado':observed,'resultado':'Aprobada' if success else 'Fallida'})
        print(identifier,tests[-1]['resultado'],flush=True)
        if not success: raise RuntimeError('Criterio fallido: '+identifier)
    def ask(path,body,token=normal,channel='web'):
        return orig.send(api_port,path,body,api_client,{'Authorization':f'Bearer {token}','X-Lab-Channel':channel})
    def read_events():
        status,data,_=orig.send(api_port,'/__lab/events',{},api_client,{'X-Lab-Admin':cfg['admin']})
        if status!=200: raise RuntimeError('No se pudieron obtener los eventos')
        return data['eventos']
    error=None
    try:
        with TemporaryDirectory(prefix='meridian-distribuido-') as work, ExitStack() as stack:
            work=Path(work); core=orig.Core(work/'principal.sqlite',key); snapshot=work/'respaldo.sqlite'
            stack.enter_context(serve(core_port,server,core.request))
            order={'cuenta':'CTA-A','destino':'CTA-B','referencia':'LAB-TX-01','monto_centavos':7500}
            web,mobile=(ask('/saldo',{'cuenta':'CTA-A'},channel=x) for x in ('web','movil'))
            record('LAB01','Consulta autorizada web/móvil por HTTPS',{'web':web[0],'movil':mobile[0],'tls':web[2],'saldo_centavos':web[1].get('saldo_centavos')},web[0]==mobile[0]==200 and web[1].get('saldo_centavos')==mobile[1].get('saldo_centavos')==100000)
            denied=ask('/transferencia',order); unknown=ask('/saldo',{'cuenta':'CTA-A'},token='sesion-inexistente')
            record('LAB02','Señal reforzada sintética requerida; sesión inválida rechazada',{'sin_refuerzo':denied[0],'sin_sesion':unknown[0]},denied[0]==403 and unknown[0]==401 and denied[1].get('resultado')=='verificacion_adicional')
            other=ask('/saldo',{'cuenta':'CTA-B'}); bad=ask('/transferencia',{**order,'cuenta':'CTA-B','destino':'CTA-A'},stronger)
            direct=orig.send(core_port,'/saldo',{'cuenta':'CTA-A','actor':'cliente-a'},core_client,{})
            record('LAB03','Cuenta ajena y adaptador sin clave rechazados',{'consulta_ajena':other[0],'orden_ajena':bad[0],'adaptador_sin_clave':direct[0]},other[0]==bad[0]==direct[0]==403 and core.summary()['asientos']==[])
            with ThreadPoolExecutor(2) as pool: first,second=list(pool.map(lambda _:ask('/transferencia',order,stronger),range(2)))
            posted=core.summary(); reread=ask('/estado',{'referencia':order['referencia']})
            record('LAB04','Concurrencia: un asiento y estado consultable',{'codigos':sorted([first[0],second[0]]),'estado':reread[0],**posted},sorted([first[0],second[0]])==[200,201] and reread[0]==200 and len(posted['asientos'])==1 and posted['saldos_centavos']=={'CTA-A':92500,'CTA-B':32500})
            altered=ask('/transferencia',{**order,'monto_centavos':7600},stronger)
            record('LAB05','Referencia en conflicto conserva asiento original',{'codigo':altered[0],'asientos':len(core.summary()['asientos'])},altered[0]==409 and core.summary()==posted)
            events=read_events(); trace=denied[1]['traza']; matching=[e for e in events if e['traza']==trace]; serialized=json.dumps(events)
            record('LAB06','Evento y alerta correlacionados, sin credenciales del ensayo',{'traza':trace,'registros_correlacionados':len(matching)},len(matching)==2 and any('alerta' in e for e in matching) and all(t not in serialized for t in cfg.values()))
            core.backup(snapshot); begin=time.perf_counter(); stack.close()
            offline=ask('/transferencia',{**order,'referencia':'LAB-CAIDA-01'},stronger)
            record('LAB07','Servicio core detenido: 503 sin asiento nuevo',{'codigo':offline[0],'asientos':len(core.summary()['asientos'])},offline[0]==503 and core.summary()==posted)
            core.path=work/'restaurado.sqlite'
            with orig.database(snapshot) as source, orig.database(core.path) as target: source.backup(target)
            stack.enter_context(serve(core_port,server,core.request))
            result=ask('/estado',{'referencia':order['referencia']}); balance=ask('/saldo',{'cuenta':'CTA-A'}); interrupted=ask('/estado',{'referencia':'LAB-CAIDA-01'}); after=core.summary()
            record('LAB08','Restauración de copia disponible, conciliación y estado',{'estado':result[0],'consulta':balance[0],'orden_durante_caida':interrupted[0],'tiempo_ensayo_ms':round((time.perf_counter()-begin)*1000,2),'asientos_perdidos_en_fixture':len(posted['asientos'])-len(after['asientos']),'saldos':after['saldos_centavos']},result[0]==balance[0]==200 and interrupted[0]==404 and after==posted and sum(after['saldos_centavos'].values())==125000)
            events=read_events()
    except Exception as exc:
        error=type(exc).__name__; print('Prueba interrumpida:',error,flush=True)
    evidence={'inicio_utc':start_utc,'cierre_utc':orig.utc_now().isoformat(),'entorno_declarado':args.environment,'advertencia':'No verifica por sí mismo la ubicación GCP, MFA real, SIEM, HA, MDM/DLP ni BIA. Adjuntar evidencia externa de despliegue.','huella_original':sha256(Path(orig.__file__).read_bytes()).hexdigest(),'huella_variante':sha256(Path(__file__).read_bytes()).hexdigest(),'motor':orig.sqlite3.sqlite_version,'pruebas':tests,'eventos':events,'error':error}
    output.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Registro: {output}',flush=True)
    return 1 if error or len(tests)!=8 else 0

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest='mode',required=True)
    p=sub.add_parser('prepare'); p.add_argument('--root',type=Path,default=Path('meridian-runtime'))
    p=sub.add_parser('gateway'); p.add_argument('--root',type=Path,required=True); p.add_argument('--port',type=int,default=8443); p.add_argument('--core-port',type=int,default=9443)
    p=sub.add_parser('test'); p.add_argument('--root',type=Path,required=True); p.add_argument('--api-port',type=int,default=18443); p.add_argument('--core-port',type=int,default=9443); p.add_argument('--environment',default='local de validación'); p.add_argument('--output',type=Path,default=Path('evidencia_distribuida.json'))
    args=parser.parse_args()
    if args.mode=='prepare': prepare(args.root)
    elif args.mode=='gateway': gateway(args.root,args.port,args.core_port)
    else: raise SystemExit(test(args.root,args.api_port,args.core_port,args.output))
