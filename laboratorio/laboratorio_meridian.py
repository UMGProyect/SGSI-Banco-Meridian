"""Ejercicio de controles para Banco Meridian. Solo escucha en 127.0.0.1."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, contextmanager
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from hmac import compare_digest
from http.client import HTTPSConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
import json
from pathlib import Path
import secrets
import sqlite3
import ssl
from tempfile import TemporaryDirectory
import threading
import time
from uuid import uuid4

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

LOCAL = "127.0.0.1"
ACCOUNTS = {"CTA-A": ("cliente-a", 100_000), "CTA-B": ("cliente-b", 25_000)}
CENTAVOS_UMBRAL = 5_000


def utc_now():
    return datetime.now(timezone.utc)


def contexts(path):
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Meridian lab localhost")])
    now = utc_now()
    cert = (
        x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
        .serial_number(x509.random_serial_number()).not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(hours=1))
        .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ip_address(LOCAL))]), critical=False)
        .sign(key, hashes.SHA256())
    )
    cert_path, key_path = path / "cert.pem", path / "key.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(serialization.Encoding.PEM,
                                          serialization.PrivateFormat.PKCS8,
                                          serialization.NoEncryption()))
    server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server.minimum_version = ssl.TLSVersion.TLSv1_2
    server.load_cert_chain(cert_path, key_path)
    client = ssl.create_default_context(cafile=str(cert_path))
    client.minimum_version = ssl.TLSVersion.TLSv1_2
    return server, client


def send(endpoint, path, payload, context, headers):
    connection = HTTPSConnection(LOCAL, endpoint, context=context, timeout=5)
    try:
        connection.connect()
        tls = connection.sock.version()
        connection.request("POST", path, json.dumps(payload),
                           {**headers, "Content-Type": "application/json"})
        response = connection.getresponse()
        return response.status, json.loads(response.read()), tls
    finally:
        connection.close()


@contextmanager
def serve(context, app):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size < 2 or size > 2048:
                    raise ValueError("Tamaño inválido")
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict):
                    raise ValueError("Cuerpo inválido")
                status, result = app(self.path, self.headers, body)
            except (ValueError, TypeError):
                status, result = 400, {"resultado": "solicitud_invalida"}
            value = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(value)))
            self.end_headers()
            self.wfile.write(value)

        def log_message(self, _format, *args):
            pass

    with ThreadingHTTPServer((LOCAL, 0), Handler) as server:
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": .05})
        thread.start()
        try:
            yield server.server_port
        finally:
            server.shutdown()
            thread.join(timeout=5)


@contextmanager
def database(path):
    with closing(sqlite3.connect(path, timeout=5)) as connection, connection:
        yield connection


class Core:
    def __init__(self, path, key):
        self.path = path
        self.key = key
        self.online = True
        with database(self.path) as db:
            db.executescript("""
                CREATE TABLE cuentas(id TEXT PRIMARY KEY, owner TEXT, saldo INTEGER CHECK(saldo >= 0));
                CREATE TABLE ordenes(ref TEXT PRIMARY KEY, actor TEXT, origen TEXT,
                                     destino TEXT, monto INTEGER CHECK(monto > 0));
            """)
            db.executemany("INSERT INTO cuentas VALUES(?,?,?)",
                           [(number, actor, amount) for number, (actor, amount) in ACCOUNTS.items()])

    def backup(self, destination):
        with database(self.path) as origin, database(destination) as backup:
            origin.backup(backup)

    def summary(self):
        with database(self.path) as db:
            balances = dict(db.execute("SELECT id,saldo FROM cuentas ORDER BY id").fetchall())
            orders = db.execute("SELECT ref,origen,destino,monto FROM ordenes ORDER BY ref").fetchall()
        return {"saldos_centavos": balances, "asientos": orders}

    def request(self, path, headers, body):
        if not compare_digest(headers.get("X-Service-Key", ""), self.key):
            return 403, {"resultado": "servicio_denegado"}
        if not self.online:
            return 503, {"resultado": "adaptador_no_disponible"}
        with database(self.path) as db:
            return self.transaction(db, path, body)

    @staticmethod
    def transaction(db, path, body):
        actor, account = body["actor"], body.get("cuenta")
        if path == "/estado":
            row = db.execute("SELECT actor FROM ordenes WHERE ref = ?", (body["referencia"],)).fetchone()
            return ((200, {"resultado": "confirmada", "referencia": body["referencia"]})
                    if row and row[0] == actor else (404, {"resultado": "sin_confirmacion"}))
        if path == "/transferencia":
            db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT owner,saldo FROM cuentas WHERE id = ?", (account,)).fetchone()
        if row is None or row[0] != actor:
            return 403, {"resultado": "cuenta_denegada"}
        if path == "/saldo":
            return 200, {"resultado": "autorizado", "saldo_centavos": row[1]}
        destination, amount, ref = body["destino"], body["monto_centavos"], body["referencia"]
        previous = db.execute("SELECT actor,origen,destino,monto FROM ordenes WHERE ref = ?", (ref,)).fetchone()
        if previous:
            if previous == (actor, account, destination, amount):
                return 200, {"resultado": "confirmada", "referencia": ref, "reutilizada": True}
            return 409, {"resultado": "referencia_en_conflicto"}
        if destination == account or not db.execute("SELECT 1 FROM cuentas WHERE id=?", (destination,)).fetchone():
            return 422, {"resultado": "destino_invalido"}
        if row[1] < amount:
            return 422, {"resultado": "saldo_insuficiente"}
        db.execute("UPDATE cuentas SET saldo=saldo-? WHERE id=?", (amount, account))
        db.execute("UPDATE cuentas SET saldo=saldo+? WHERE id=?", (amount, destination))
        db.execute("INSERT INTO ordenes VALUES(?,?,?,?,?)", (ref, actor, account, destination, amount))
        return 201, {"resultado": "confirmada", "referencia": ref, "reutilizada": False}


def gateway(core_port, client, key, tokens, events):
    def handle(path, headers, body):
        auth = headers.get("Authorization", "").removeprefix("Bearer ")
        identity = tokens.get(auth)
        profile = headers.get("X-Lab-Channel", "")
        trace = uuid4().hex
        event = {"traza": trace, "hora_utc": utc_now().isoformat(), "canal": profile,
                 "actividad": path, "usuario": identity[0] if identity else "sin_autenticar",
                 "dispositivo_sintetico": f"equipo-{profile}"}
        if path == "/transferencia":
            event.update({"monto_centavos": body.get("monto_centavos"), "destino": body.get("destino")})
        if identity is None:
            code, result = 401, {"resultado": "sesion_denegada"}
        elif path not in {"/saldo", "/transferencia", "/estado"} or profile not in {"web", "movil"}:
            code, result = 400, {"resultado": "solicitud_invalida"}
        elif path == "/transferencia" and (
            type(body.get("monto_centavos")) is not int or body["monto_centavos"] <= 0
            or any(not isinstance(body.get(k), str) or not body[k] for k in ("cuenta","destino","referencia"))
        ):
            code, result = 400, {"resultado": "orden_invalida"}
        elif path == "/estado" and not isinstance(body.get("referencia"), str):
            code, result = 400, {"resultado": "referencia_invalida"}
        elif path == "/transferencia" and body["monto_centavos"] >= CENTAVOS_UMBRAL and not identity[1]:
            code, result = 403, {"resultado": "verificacion_adicional"}
        else:
            code, result, tls = send(core_port, path, {**body, "actor": identity[0]}, client,
                                     {"X-Service-Key": key})
            event["tls_adaptador"] = tls
        event.update({"codigo": code, "resultado": result["resultado"]})
        events.append(event)
        if result["resultado"] == "verificacion_adicional":
            events.append({"traza": trace, "hora_utc": utc_now().isoformat(),
                           "alerta": "operacion_fuera_de_perfil_sintetico"})
        return code, {**result, "traza": trace}
    return handle


def demand(condition, identifier):
    if not condition:
        raise RuntimeError(f"Criterio fallido en {identifier}")


def run(root):
    server, client = contexts(root)
    key, normal, stronger = (secrets.token_urlsafe(24) for _ in range(3))
    core = Core(root / "principal.sqlite", key)
    events, tests = [], []
    order = {"cuenta": "CTA-A", "destino": "CTA-B", "referencia": "LAB-TX-01", "monto_centavos": 7_500}
    snapshot = root / "sitio_alterno.sqlite"

    def record(identifier, expected, observed, success):
        demand(success, identifier)
        tests.append({"id": identifier, "esperado": expected, "observado": observed, "resultado": "Aprobada"})

    with serve(server, core.request) as core_port:
        with serve(server, gateway(core_port, client, key,
                                  {normal: ("cliente-a", False), stronger: ("cliente-a", True)},
                                  events)) as api_port:

            def ask(path, body, token=normal, channel="web"):
                return send(api_port, path, body, client,
                            {"Authorization": f"Bearer {token}", "X-Lab-Channel": channel})

            web, mobile = (ask("/saldo", {"cuenta": "CTA-A"}, channel=name) for name in ("web", "movil"))
            record("LAB01", "Consulta web y móvil responden 200 con el mismo saldo autorizado",
                   {"web":web[0], "movil":mobile[0], "saldo_centavos":web[1]["saldo_centavos"], "tls":web[2]},
                   web[0] == mobile[0] == 200 and web[1]["saldo_centavos"] == mobile[1]["saldo_centavos"])
            denied = ask("/transferencia", order)
            unknown = ask("/saldo", {"cuenta": "CTA-A"}, token="sesion-inexistente")
            record("LAB02", "Una orden sobre el umbral sin señal reforzada se detiene y una sesión inválida se rechaza",
                   {"sin_refuerzo":denied[0], "sin_sesion":unknown[0], "traza_desafio":denied[1]["traza"]},
                   denied[0] == 403 and denied[1]["resultado"] == "verificacion_adicional" and unknown[0] == 401)
            other = ask("/saldo", {"cuenta": "CTA-B"})
            bad_order = ask("/transferencia", {**order,"cuenta":"CTA-B","destino":"CTA-A"}, stronger)
            direct = send(core_port, "/saldo", {"cuenta":"CTA-A","actor":"cliente-a"}, client, {})
            record("LAB03", "Rechazo del acceso de cliente a cuenta ajena y del acceso directo sin clave de servicio",
                   {"consulta_ajena":other[0],"orden_ajena":bad_order[0], "adaptador_sin_clave":direct[0]},
                   other[0] == bad_order[0] == direct[0] == 403 and core.summary()["asientos"] == [])
            with ThreadPoolExecutor(2) as pool:
                first, second = list(pool.map(lambda _: ask("/transferencia", order, stronger), range(2)))
            posted = core.summary()
            reread = ask("/estado", {"referencia":order["referencia"]})
            record("LAB04", "Dos solicitudes concurrentes generan un solo asiento y un estado consultable",
                   {"codigos":sorted([first[0],second[0]]),"estado":reread[0], **posted},
                   sorted([first[0],second[0]]) == [200,201] and reread[0] == 200
                   and len(posted["asientos"]) == 1 and posted["saldos_centavos"] == {"CTA-A":92_500,"CTA-B":32_500})
            altered = ask("/transferencia", {**order, "monto_centavos":7_600}, stronger)
            record("LAB05", "Misma referencia con un monto distinto produce 409 y conserva el registro original",
                   {"codigo":altered[0], "asientos":len(core.summary()["asientos"])},
                   altered[0] == 409 and core.summary() == posted)
            trace = denied[1]["traza"]
            matching = [e for e in events if e["traza"] == trace]
            serialized = json.dumps(events)
            record("LAB06", "Evento y alerta comparten traza. Los eventos no guardan credenciales",
                   {"traza":trace, "registros_correlacionados": len(matching),
                    "alerta": next((e["alerta"] for e in matching if "alerta" in e), None)},
                   len(matching) == 2 and any("alerta" in e for e in matching)
                   and all(token not in serialized for token in (key, normal, stronger)))
            core.backup(snapshot)
            start = time.perf_counter()
            core.online = False
            offline = ask("/transferencia", {**order, "referencia":"LAB-CAIDA-01"}, stronger)
            record("LAB07", "Adaptador indisponible devuelve 503 y no confirma una transferencia",
                   {"codigo":offline[0], "asientos":len(core.summary()["asientos"])},
                   offline[0] == 503 and core.summary() == posted)
            core.path = root / "restaurado.sqlite"
            with database(snapshot) as source, database(core.path) as target:
                source.backup(target)
            core.online = True
            result = ask("/estado", {"referencia":order["referencia"]})
            balance = ask("/saldo", {"cuenta":"CTA-A"})
            interrupted = ask("/estado", {"referencia":"LAB-CAIDA-01"})
            elapsed = round((time.perf_counter()-start)*1000, 2)
            after = core.summary()
            record("LAB08", "Restauración de la copia disponible. Consulta y estado recuperados, sin orden de la caída",
                   {"estado_confirmado":result[0],"consulta":balance[0],"orden_durante_caida":interrupted[0],
                    "tiempo_local_ms":elapsed,"asientos_perdidos_en_fixture":len(posted["asientos"])-len(after["asientos"]),
                    "saldos_restaurados_centavos": after["saldos_centavos"]},
                   result[0] == balance[0] == 200 and interrupted[0] == 404 and after == posted
                   and sum(after["saldos_centavos"].values()) == 125_000)

    return {"inicio_entorno":"laboratorio HTTPS en 127.0.0.1 con dos servicios y certificado efímero",
            "factores":"niveles de identidad sintéticos. No corresponde a MFA de un proveedor.",
            "motor":f"SQLite {sqlite3.sqlite_version}", "cierre_utc":utc_now().isoformat(),
            "huella_codigo_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
            "pruebas":tests,"eventos":events}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evidencia.json"))
    args = parser.parse_args()
    with TemporaryDirectory(prefix="meridian-local-") as directory:
        evidence = run(Path(directory))
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for test in evidence["pruebas"]:
        print(f'{test["id"]} {test["resultado"]}')
    print(f'Registro: {args.output}')


if __name__ == "__main__":
    main()
