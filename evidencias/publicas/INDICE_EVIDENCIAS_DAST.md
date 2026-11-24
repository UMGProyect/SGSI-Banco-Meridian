# Evidencias DAST — Banco Meridian

Fecha del ensayo: 24 de noviembre de 2026. Alcance: API P01/P02 en GCP, accesible por túnel SSH/IAP desde Docker; datos sintéticos. ZAP 2.17.0 según informes originales, generado a las 20:43:35 UTC.

| ID | Archivo | Resultado |
|---|---|---|
| EV-DAST-01 | [Versión Docker](DAST/EV-DAST-01_Version_Docker.png) | Docker CLI 29.9.3; versión ZAP confirmada por informes, no por esta captura. |
| EV-DAST-02 | [Conectividad](DAST/EV-DAST-02_Conectividad_Docker_GCP.png) | TCP hacia puerto local del túnel 18443; captura posterior al ensayo (20:47:54 UTC). |
| EV-DAST-03 | [Caja negra dirigida](DAST/EV-DAST-03_Pruebas_Caja_Negra.png) | 3 POST sin autenticación: 401; JSON malformado: 400. 4/4 aprobadas. |
| EV-DAST-04 | [Alertas](DAST/EV-DAST-04_Alertas_OWASP_ZAP.png) | Cola pasiva 0; 8 instancias bajas, 0 altas/medias/informativas. |
| EV-DAST-05 | [HTML](DAST/EV-DAST-05_Informe_ZAP.html) / [JSON](DAST/EV-DAST-05_Informe_ZAP.json) | 2 tipos de alerta, 4 instancias cada uno. Informes íntegros. |

## Tratamiento propuesto (no aplicado)

| Regla | Riesgo / confianza | Instancias | Tratamiento | Verificación de cierre |
|---|---|---:|---|---|
| 10036 — cabecera Server divulga versión | Bajo / alta | 4 | Minimizar cabecera en servidor/gateway; ISO 27002:2022 8.9, 8.28 | Repetir pruebas y ZAP, comprobar cabecera genérica o ausente. |
| 10035 — HSTS ausente | Bajo / alta | 4 | Definir HSTS en terminación HTTPS de producción, con certificados y dominio válidos; ISO 27002:2022 8.24, 8.28 | Validar cabecera y política en clientes compatibles y repetir ZAP. |

Controles adicionales relacionados: 8.8 y 8.29. HSTS aplica principalmente a navegadores con nombre DNS y TLS válido; el laboratorio no acredita su aplicación en producción. La ausencia de HSTS no prueba tráfico en claro. No se recalcula riesgo residual sin evaluación.

## Limitaciones e integridad

Análisis pasivo y cuatro solicitudes dirigidas no autenticadas; no escaneo activo, no cobertura exhaustiva ni prueba de autorización autenticada. Cliente de ensayo con verify=False para interceptación; no valida confianza del certificado en esa ruta. Los informes contienen 100 % de respuestas 4xx y un indicador informativo de respuestas lentas, que no representa prueba de rendimiento/BIA. Se mantuvo la API privada; el resultado TCP por sí solo no acredita TLS extremo a extremo. Las capturas son copias con ocultación de indicadores de usuario/ruta local; el ZIP original se conserva aparte. No se modificaron los informes HTML/JSON. SHA256 de publicación en SHA256SUMS_DAST.txt.
