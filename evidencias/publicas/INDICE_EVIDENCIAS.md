# Índice de evidencias GCP — Banco Meridian

Fecha de recopilación: 24 de noviembre de 2026. Alcance exclusivo P01/P02. Copias derivadas de las capturas proporcionadas, con rectángulos opacos sobre datos personales o información no pertinente. Se conserva la resolución original; los originales no se versionan. Los controles indicados son relaciones de trazabilidad parcial, no declaración de cumplimiento integral.

| Evidencia | Observación | Anexo A ISO/IEC 27001:2022 |
|---|---|---|
| [EV-GCP-01](GCP/EV-GCP-01_Recursos_Terraform.png) | Terraform validate y state list con seis recursos; no es la salida original de apply. | 8.9, 8.32 |
| [EV-GCP-02](GCP/EV-GCP-02_Compute_Engine_VM_Privada.png) | VM RUNNING, IP interna 10.20.10.2, sin IP externa; Shielded VM activa. | 8.9, 8.20, 8.22 |
| [EV-GCP-03](GCP/EV-GCP-03_VPC_Segmentacion_Subredes.png) | VPC personalizada, tres subredes y Flow Logs habilitados. | 8.20, 8.22, 8.15 |
| [EV-GCP-04](GCP/EV-GCP-04_Firewall_Acceso_Seguro_IAP.png) | Regla activa TCP/22 desde 35.235.240.0/20, target tag y logging. | 8.3, 8.20, 8.22 |
| [EV-GCP-05](GCP/EV-GCP-05_Verificacion_API_HTTPS_Integridad_SHA256.png) | Hostname, fecha UTC, listeners loopback 8443/9443 y huellas SHA-256 coincidentes. | 8.20, 8.24, 8.29 |
| [EV-GCP-06](GCP/EV-GCP-06_Control_Identidad_OS_Login.png) | Metadatos enable-oslogin y block-project-ssh-keys en TRUE. | 5.16, 8.2, 8.5 |
| [EV-GCP-07](GCP/EV-GCP-07_VPC_Flow_Logs.png) | Registros de flujos TCP y direcciones de origen/destino; no prueba por sí sola conexión exitosa a Internet. | 8.15, 8.16, 8.20 |
| [EV-GCP-08](GCP/EV-GCP-08_Visual_Studio_Code_Remoto.png) | VS Code conectado por SSH y eventos de API; nombre personal ocultado. | 8.2, 8.15, 8.20 |
| [EV-GCP-09](GCP/EV-GCP-09_Tunel_Bidireccional.png) | Reenvíos SSH -L/-R y TcpTestSucceeded True en 18443. | 8.20, 8.24 |
| [EV-GCP-10](GCP/EV-GCP-10_Resultados_LAB01_LAB08.png) | JSON muestra LAB01/LAB02 y terminal LAB03–LAB08; ejecución aprobada según evidencia comunicada. | 8.26, 8.29, 8.15 |
| [EV-GCP-11](GCP/EV-GCP-11_evidencia_distribuida.json) | JSON original: LAB01–LAB08 aprobadas, 15 eventos, TLS 1.3 y restauración experimental en 4051.02 ms. | 8.15, 8.24, 8.26, 8.29, 8.13 |
| [EV-GCP-12](GCP/EV-GCP-12_Cloud_Audit_Logs.png) | Operaciones administrativas de creación de VPC, subredes y firewall registradas. | 8.15, 8.16, 8.32 |
| [EV-GCP-13](GCP/EV-GCP-13_Auditoria_Autenticacion_SSH.png) | Autenticaciones Accepted publickey en sshd desde rango IAP; identidad ocultada. | 5.16, 8.2, 8.15 |
| [EV-GCP-14](GCP/EV-GCP-14_Acceso_SSH_IAP.png) | Acceso exitoso vía gcloud compute ssh --tunnel-through-iap; Ubuntu 24.04.5. | 8.2, 8.5, 8.20 |

## EV-GCP-11

El [JSON original de la ejecución distribuida](GCP/EV-GCP-11_evidencia_distribuida.json) fue recibido por separado y se incorpora sin modificaciones. SHA-256: `09ec0d61f2133889f9c9e54e8a634d60f3397712687001a3fa94762b9b392dd2`. Contiene ocho pruebas aprobadas, 15 eventos y error nulo. Las identidades y cuentas son sintéticas. La ubicación declarada se contrasta con EV-GCP-05, EV-GCP-08, EV-GCP-09 y EV-GCP-10; el JSON por sí solo no certifica ubicación ni cumplimiento integral. Consultar [registro de ejecución distribuida](2026-11-24-laboratorio-distribuido.md).

## Matrices

[Excel v4 — GCP](../../matrices/Matrices%20SGSI%20Banco%20Meridian%20v4%20-%20GCP.xlsx): copia exacta del archivo actualizado, 188 fórmulas y verificación CRC satisfactoria.

## Integridad

El archivo SHA256SUMS.txt contiene hashes de las copias destinadas a GitHub y del Excel (rutas relativas a la raíz del repositorio). Los hashes de originales y derivados de las capturas se relacionan en MANIFIESTO_CAPTURAS.csv. Las huellas de imágenes no prueban por sí mismas origen ni autenticidad.

No se acredita MFA real, SIEM externo, WAF, MDM/DLP, XDR ni recuperación integral del BIA. La publicación sigue pendiente de revisión final y autorización.
