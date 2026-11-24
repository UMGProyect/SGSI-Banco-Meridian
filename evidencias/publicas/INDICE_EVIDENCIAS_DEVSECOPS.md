# Evidencias complementarias DevSecOps y gestión de parches

Fecha de ejecución y recopilación: 24 de noviembre de 2026. Alcance: P01 consulta de saldos y P02 transferencias intrabanco. Complementa INDICE_EVIDENCIAS.md; no sustituye el conjunto previo ni su manifiesto.

| ID | Archivo | Resultado observado | Controles ISO/IEC 27002:2022 relacionados |
|---|---|---|---|
| EV-DEV-01 | [Gitleaks](DevSecOps/EV-DEV-01_Gitleaks.png) | Dos escaneos sin hallazgos (historial y árbol actual). | 8.4, 8.25, 8.28 |
| EV-DEV-02 | [Terraform Validate](DevSecOps/EV-DEV-02_Terraform_Validate.png) | Job satisfactorio; validación de configuración, no prueba integral del despliegue. | 8.9, 8.32 |
| EV-DEV-03 | [Checkov](DevSecOps/EV-DEV-03_Checkov_IaC.png) | 21 aprobadas, 1 fallida (CKV_GCP_38), 0 omitidas y 0 errores de parseo. | 8.9, 8.24, 8.27 |
| EV-DEV-04 | [Semgrep](DevSecOps/EV-DEV-04_Semgrep_SAST.png) | 200 reglas, 3 objetivos, 1 WARNING, 0 errores; HTTPSConnection en línea 60, pendiente de validación negativa TLS. | 8.25, 8.28, 8.29 |
| EV-DEV-05 | [OSV GCP](DevSecOps/EV-DEV-05_OSV_SCA_GCP.png) | 9 avisos PyPI en cryptography 41.0.7: 5 altos, 3 medios, 1 desconocido; aplicabilidad a 41.0.7-4ubuntu0.4 pendiente. | 8.8, 8.25 |
| EV-DEV-06 | [OSV Windows](DevSecOps/EV-DEV-06_OSV_SCA_Windows.png) | 3 paquetes analizados, sin hallazgos; no cubre todo el sistema operativo. | 8.8, 8.25 |
| EV-GCP-15 | [APT](GCP/EV-GCP-15_Evaluacion_Actualizaciones_Seguridad.png) | Índices no descargados, uso de caché anterior. VM privada sin NAT; gestión de parches pendiente. | 8.8, 8.9, 8.20 |

## Trazabilidad
- IaC y Gitleaks: https://github.com/UMGProyect/SGSI-Banco-Meridian/actions/runs/45477095164
- SAST: https://github.com/UMGProyect/SGSI-Banco-Meridian/actions/runs/45477241010/job/138740587196
- SCA GCP: https://github.com/UMGProyect/SGSI-Banco-Meridian/actions/runs/45477729883/job/138742299666
- SCA Windows: https://github.com/UMGProyect/SGSI-Banco-Meridian/actions/runs/45477729883/job/138742299263
- Inventario y evaluación: ../../docs/seguridad/INVENTARIO-DEPENDENCIAS-2026-11-24.md

Las capturas de DevSecOps se conservan byte a byte (tres nombres normalizados). EV-GCP-15 contiene ocultaciones opacas de usuario y panel de historial; no se modifica la salida de APT. Los originales se mantienen fuera de este paquete. No se infiere cierre de riesgos ni cumplimiento integral de controles. Tratamiento propuesto de APT: salida controlada mediante NAT o repositorio interno; pendiente de implementación y verificación. Las referencias a controles son relaciones de evidencia, no certificación.
