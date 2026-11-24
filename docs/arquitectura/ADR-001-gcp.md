# ADR-001 — Google Cloud como IaaS
Fecha: 2026-11-24. Estado: cambio de proveedor autorizado por el equipo interlocutor; diseño y despliegue pendientes de validación.
Decisión: sustituir Azure por Google Cloud Compute Engine para P01 (consulta de saldos) y P02 (transferencias internas), sin ampliar alcance. El proyecto académico TCP/IP existente queda fuera y no se modificará. Usar proyecto GCP nuevo y VPC independiente, sin Shared VPC, peering ni reutilización de cuentas de servicio del proyecto anterior. Cuenta de facturación compartida, saldo indicado de USD 280, no verificado por el repositorio. Presupuesto orientativo USD 60, alertas 50/75/90/100%; no son límite de gasto.
## Diseño incremental
- Fase A: red personalizada y acceso administrativo IAP/OS Login, sin IP pública ni reglas SSH desde Internet. Compute y NAT opcionales, inicialmente desactivados.
- Fase B: portal/API (Nginx y aplicación), IAM de clientes (Keycloak, OIDC y MFA real), Wazuh (SIEM y seguridad de endpoint). VM separadas, Ubuntu LTS. Separar IAM de clientes de IAM administrativo Google Cloud. Evitar credenciales y datos reales.
- Fase C: perímetro público HTTPS mediante Application Load Balancer y Cloud Armor Standard, origen privado. Dominio/certificado válido, reglas de acceso de backend y health checks según tipo de balanceador. Suricata opcional como sensor o IPS en ruta explícita; su instalación no demuestra inspección ni bloqueo de tráfico si la topología no lo dirige por él.
- Fase D: core/adaptador y PostgreSQL en VMware local. Ruta cifrada por VPN, solo API->adaptador TLS y adaptador->DB. HA VPN con BGP requiere equipo local compatible y conectividad de extremo; si CGNAT o falta de BGP, evaluar túnel WireGuard iniciado desde local hacia una VM dedicada. No etiquetar este último como HA VPN ni afirmar alta disponibilidad. Si ambos lados están en GCP, documentar simulación, no arquitectura híbrida real.
- Fase E: MDM/DLP/XDR con herramientas y licencias verificadas, independientemente del proveedor IaaS. Wazuh no acredita automáticamente MDM, DLP ni XDR integral. Se pueden mantener Intune/Purview como diseño objetivo si se justifica disponibilidad/licencias; no inventar equivalencias. Validar pruebas representativas o declarar brechas.
## Red propuesta (confirmar sin solapamientos)
| Segmento | CIDR | Uso |
|---|---|---|
| app | 10.20.10.0/24 | Portal/API |
| seguridad | 10.20.20.0/24 | IAM y SIEM |
| administración | 10.20.30.0/24 | Administración reservada |
| local | 10.30.10.0/24 | Adaptador y DB en VMware |
Región us-central1, zona us-central1-a inicialmente. Una zona de laboratorio no demuestra redundancia. Sin VPN ni acceso público hasta etapa de conectividad/perímetro.
## Trazabilidad
C01/R01,R07,R08: IAM/Keycloak; C02/R02,R03: API/adaptador e integridad PostgreSQL; C03/R04: VPC/firewall/VPN; C04/R05,R08: Wazuh/Cloud Logging y registros de aplicación; C05/R03,R04: restauración y conciliación; C06/R06: MDM/DLP/EDR pendientes; C07/R04: responsabilidad compartida y facturación GCP; C08/R07: Secret Manager/KMS o custodia autorizada, TLS, configuración.
Mantener objetivos BIA P01 120/5 min y P02 60/0 para asientos confirmados. La demanda 300/90 por hora no es capacidad mínima validada. Conservar 23 activos y R01–R08 hasta revisión formal.
## Fuentes oficiales consultadas 2026-11-24
- IAP: https://docs.cloud.google.com/iap/docs/using-tcp-forwarding
- HA VPN: https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/automate-vpn-setup-with-terraform
- Cloud Router: https://docs.cloud.google.com/network-connectivity/docs/router
- Cloud Armor: https://docs.cloud.google.com/armor/docs/security-policy-overview
- Firewall: https://docs.cloud.google.com/firewall/docs/using-firewalls
- Presupuestos: https://docs.cloud.google.com/billing/docs/how-to/budgets
Revalidar precios, cuotas, proveedor Terraform, licencias y restricciones de prueba gratuita al desplegar.
