# SGSI Banco Meridian

Sistema de Gestión de Seguridad de la Información para una entidad bancaria ficticia. El proyecto abarca la consulta de saldos de cuentas autorizadas (P01) y las transferencias intrabanco (P02). Se utilizaron exclusivamente datos sintéticos.

## Documentación y evidencias

| Componente | Ubicación |
|---|---|
| Alcance del SGSI | [Alcance](docs/ALCANCE.md) |
| Modelo de gobierno y políticas | [Documentación del SGSI](docs/fase-1/) |
| Inventario y BIA | [Revisión de activos y continuidad](docs/fase-2/) |
| Arquitectura híbrida GCP | [Decisión de arquitectura](docs/arquitectura/ADR-001-gcp.md) |
| Infraestructura como código | [Terraform](infraestructura/gcp/) |
| Código de la API y laboratorio | [Código Python](laboratorio/) |
| Matrices del SGSI | [Matrices](matrices/) |
| Implementación GCP | [Capturas y JSON](evidencias/publicas/GCP/) · [Índice](evidencias/publicas/INDICE_EVIDENCIAS.md) |
| DevSecOps (SAST, SCA, IaC y secretos) | [Capturas](evidencias/publicas/DevSecOps/) · [Índice](evidencias/publicas/INDICE_EVIDENCIAS_DEVSECOPS.md) |
| DAST (OWASP ZAP) | [Capturas e informes](evidencias/publicas/DAST/) · [Índice](evidencias/publicas/INDICE_EVIDENCIAS_DAST.md) |
| Evaluación de dependencias | [Inventario y resultados](docs/seguridad/INVENTARIO-DEPENDENCIAS-2026-11-24.md) |

## Resultados experimentales del 24 de noviembre de 2026

| Evaluación | Resultado |
|---|---|
| Pruebas funcionales y de seguridad distribuidas | [8/8 aprobadas (JSON)](evidencias/publicas/GCP/EV-GCP-11_evidencia_distribuida.json) |
| Gitleaks y Terraform Validate | [Aprobados](https://github.com/UMGProyect/SGSI-Banco-Meridian/actions/runs/45477095164) |
| Checkov | 21 de 22 comprobaciones aprobadas; CMEK por tratar |
| Semgrep (SAST) | [1 advertencia de auditoría](evidencias/publicas/DevSecOps/EV-DEV-04_Semgrep_SAST.png) |
| OSV-Scanner (SCA) | [GCP upstream: 9 avisos](evidencias/publicas/DevSecOps/EV-DEV-05_OSV_SCA_GCP.png); [Windows: 0 en 3 paquetes](evidencias/publicas/DevSecOps/EV-DEV-06_OSV_SCA_Windows.png) |
| OWASP ZAP 2.17.0 (DAST) | 4/4 pruebas dirigidas aprobadas; 2 tipos de alerta baja, 8 instancias |

Los informes originales de ZAP están disponibles en [HTML](evidencias/publicas/DAST/EV-DAST-05_Informe_ZAP.html) y [JSON](evidencias/publicas/DAST/EV-DAST-05_Informe_ZAP.json). El archivo HTML puede descargarse y abrirse localmente en un navegador. Los manifiestos SHA-256 permiten comprobar la integridad de las copias publicables.

## Alcance de la validación

El laboratorio utilizó una VM privada en Compute Engine y un core bancario sintético local, conectados mediante SSH/IAP. No representa un servicio bancario de producción. El análisis ZAP fue pasivo y no autenticado, no un pentest exhaustivo. Los avisos de PyPI para GCP requieren contraste con los parches del paquete Ubuntu. La gestión de parches, CMEK y los demás controles no validados se mantienen como limitaciones o tratamientos propuestos. No se acredita la implementación integral del SGSI ni la certificación ISO.

La evidencia técnica se conserva en el commit [2d786c0](https://github.com/UMGProyect/SGSI-Banco-Meridian/tree/2d786c084cc6b48a089b1ca705196e76b2df1394/evidencias/publicas). La [política de seguridad](SECURITY.md) establece las restricciones de uso y publicación. El repositorio no concede acceso a la infraestructura.
