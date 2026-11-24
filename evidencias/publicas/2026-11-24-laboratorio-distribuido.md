# Registro de ejecución distribuida — Banco Meridian
Fecha: 24/11/2026. Alcance exclusivo P01 (consulta de saldos) y P02 (transferencias intrabanco). Datos sintéticos.
## Procedencia
Transcripción resumida del JSON comunicado por el operador y de las salidas de Cloud Shell, SSH, OpenSSH y terminal remota compartidas durante el despliegue. No es el JSON original ni una auditoría independiente. Conservar originales de consola y JSON fuera del repositorio hasta revisión y depuración. No publicar claves, datos de facturación, cuentas personales ni configuraciones runtime.
Inicio UTC 2026-11-24T19:05:54.016452+00:00; cierre UTC 2026-11-24T19:06:02.980190+00:00. Duración aproximada 8,96 s. SQLite 3.50.4. Error informado: null. Código original SHA-256 134bdfbcd2f9e78a07d14a112731fff500242b5dd0987f93cd261eed2b8bbc64; variante ca6bda378a47561dce400a62da99304f88c050817e9dfa2982a75c19547a7b75. Ambas huellas coinciden con los archivos del ZIP de variante revisado.
## Infraestructura observada
Terraform 1.17.2, proveedor Google 8.6.0: validate satisfactorio; plan y apply de seis altas, cero cambios y cero bajas. Proyecto dedicado; VPC personalizada, tres subredes (aplicaciones 10.20.10.0/24, seguridad 10.20.20.0/24, administración 10.20.30.0/24), regla SSH desde IAP, VM meridian-app e2-medium, Ubuntu 24.04.5 LTS, Python 3.12.3, cryptography 41.0.7, IP privada 10.20.10.2, sin IP externa en el listado. Flow Logs, OS Login y Shielded VM configurados en plan; verificación efectiva de registros pendiente. Acceso SSH inicialmente denegado y luego exitoso mediante IAP/OS Login desde Cloud Shell y Windows. API en loopback:8443; reenvío local 18443 y remoto 9443 mediante SSH sobre IAP, core SQLite en Windows. Prueba de puerto local positiva. No VPN IPsec, balanceador, WAF ni exposición pública. No afirmar arquitectura empresarial redundante.
## Resultados
| Prueba | Observación | Resultado |
|---|---|---|
| LAB01 | web/móvil HTTP 200; TLS 1.3; 100000 centavos | Aprobada |
| LAB02 | señal reforzada sintética ausente 403; sesión inválida 401 | Aprobada |
| LAB03 | consulta ajena, orden ajena y adaptador sin clave: 403 | Aprobada |
| LAB04 | HTTP 200/201, estado 200, una transferencia de 7500 centavos; saldos 92500/32500 | Aprobada |
| LAB05 | HTTP 409, permanece un asiento | Aprobada |
| LAB06 | dos registros con traza común; alerta y evento | Aprobada |
| LAB07 | servicio core detenido, HTTP 503; sin asiento nuevo | Aprobada |
| LAB08 | estado y saldo 200, orden durante caída 404, 4051.02 ms, cero asientos perdidos en fixture, saldos 92500/32500 | Aprobada |
## Interpretación
TLS 1.3 observado en cliente/API y API/adaptador. Certificados temporales verificados por los clientes; no mTLS. LAB02 utiliza tokens sintéticos, no un segundo factor real. LAB01 representa canales mediante atributos de solicitudes, no aplicaciones nativas ni dispositivos reales. LAB06 correlaciona eventos y alerta en la aplicación, no SIEM externo. LAB08 mide interrupción y restauración de copia disponible del fixture, no RTO integral ni RPO cero generalizable; no prueba pérdida completa del sitio ni conmutación. No recalificar riesgos sin revisión de eficacia y aprobación. Mantener R08 alto esperado y objetivos BIA originales. El entorno declarado del JSON no autentica ubicación de ejecución por sí solo: se complementa con salidas y capturas de despliegue.
## Próximas evidencias
Capturar/depurar: inventario VM sin IP externa; configuración efectiva de red y firewall; logs Flow Logs; SSH/IAP y listeners en VM; salida de pruebas y JSON original; huellas de fuentes local/remota. Registrar CI (Gitleaks, Checkov, Terraform) por commit y sus hallazgos. Aún no se afirma MFA real, SIEM, MDM, DLP, XDR, WAF, VPN IPsec, HA ni BIA operativo. No modificar matriz residual ni SoA a implementado integral.
