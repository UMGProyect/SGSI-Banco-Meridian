# Registro de cambios documentales pendientes
Fuentes inspeccionadas: Word v.3 fase 1, Excel original y ZIP original. No hacer sustitución global de nombres. Conservar resultados LAB01–LAB08 y SHA-256 original; la demostración cloud será evidencia nueva.
| Ubicación | Cambio requerido |
|---|---|
| Word resumen, contexto, 4.9.1, discusión y conclusiones | GCP como proveedor objetivo; distinguir plan, despliegue y evidencia. |
| 4.2 inventario | A01.1, A03.1, A03.2, A04.1: localización GCP y segmentos específicos. Conservar IDs y CID. |
| 4.6 tratamiento R01 | Pruebas de factores, revocación y bitácoras de Keycloak en entorno GCP; no asumir MFA real por LAB02. |
| 4.7 Figura 1 y 4.7.1 | Rehacer diagrama y explicación. App Service/private endpoints/VNet integration se reemplazan por VMs privadas, backend de balanceador, VPC firewall, rutas y VPN. Entra External ID por Keycloak, no por IAM de GCP. |
| 4.10.1 | Revisar Intune/Purview por disponibilidad y licencia; mantener como diseño pendiente hasta elección sustentada. |
| 4.10.2 | Wazuh como SIEM, telemetría de endpoint y correlación; validar EDR/XDR por separado, no sustituir automáticamente Defender XDR. |
| 4.11 continuidad | Escenario de pérdida de identidad o región GCP. Prueba real de recuperación pendiente; no cambiar RTO/RPO. |
| 4.13.1 y anexos D/F | Criterios de aceptación GCP: HTTPS/perímetro, identidad, VPN, protección de equipos, detección. Mantener resultados locales y estado pendiente. |
| Referencias | Añadir documentación GCP oficial; conservar fuentes Microsoft solo para controles que sigan en diseño. |
| Excel Inventario G6,G10,G11,G12 | Cambiar ubicaciones de Azure a GCP, manteniendo ID, valoración, propietario y dependencias. |
| Excel Tratamiento L6 | Actualizar evidencia de aceptación de R01. |
| Excel Aplicabilidad E28 | Documentar adquisición, uso y salida de servicios de GCP. |
| Excel Riesgos, BIA, OCTAVE, mapa de calor | Conservar fórmulas y puntuaciones; revisar dependencias/escenarios específicos del proveedor antes de aprobar. |
| ZIP Anexo C | Preservar original intacto. Crear variante de integración separada, con nuevas evidencias, fecha y huella. |
## Criterios de aceptación tecnológica
1. Capturar ID del proyecto y recursos (sin datos privados), plan Terraform, VPC/subredes y reglas efectivas.
2. Acceso administrativo IAP, sin SSH público; comprobar acceso permitido y denegado.
3. P01/P02 con cuentas sintéticas, MFA real y autorización por recurso; probar revocación y rechazo de cuenta ajena.
4. HTTPS y WAF en perímetro; origen no expuesto directamente.
5. Túnel cifrado y ruta privada entre API y adaptador local, demostrar conectividad permitida y aislamiento de DB.
6. Integridad/idempotencia, alertas correlacionadas y restauración con conciliación; distinguir límites del laboratorio.
7. Medir y documentar consumo, apagar instancias al terminar pruebas y eliminar recursos facturables innecesarios.
No modificar Word/Excel base hasta fijar el diseño técnico de etapa C/D y revisar el diff. La configuración inicial se limita a red y acceso administrativo; no es despliegue completo.
