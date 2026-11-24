# Inventario observado y primera evaluación SAST/SCA

Fecha: 2026-11-24. Alcance P01/P02. Fuente de versiones: salida de comandos facilitada por el operador (GCP 20:07 UTC; Windows sin timestamp independiente). No se han modificado los archivos Python ni los paquetes instalados.

| Componente | Ubuntu 24.04 GCP | Windows local |
|---|---|---|
| Python | 3.12.3 | 3.14.6 |
| cryptography | 41.0.7-4ubuntu0.4 (dpkg) | 50.0.2 (pip) |
| CFFI | python3-cffi-backend 1.16.0-2build1 (dpkg) | 2.1.1 |
| pycparser | No verificado | 3.0 |
| OpenSSL | libssl3t64 3.0.13-0ubuntu3.16 | ssl.OPENSSL_VERSION 3.5.7 |
| SQLite | libsqlite3-0 3.45.1-1ubuntu2.9 | sqlite3.sqlite_version 3.50.4 |

## Primera ejecución
Run: https://github.com/UMGProyect/SGSI-Banco-Meridian/actions/runs/45477241010 (commit 716db2fd3a163422ab34690af2b67f1bc82d270a).
SAST Semgrep 1.186.0: 3 objetivos (2 Python y 1 inventario), 200 reglas ejecutadas, 1 WARNING, 0 errores. Job 138740587196. Regla python.lang.security.audit.httpsconnection-detected.httpsconnection-detected, laboratorio/laboratorio_meridian.py:60. Revisión inicial: HTTPSConnection recibe contexto explícito; los contextos observados utilizan ssl.create_default_context(cafile=...) y mínimo TLS 1.2. No se aprecia desactivación de verificación en estos contextos. Alerta de auditoría, no vulnerabilidad confirmada; pendiente prueba negativa de certificado no confiable y revisión de todos los llamadores. No se suprime la regla.
SCA OSV 2.7.1, job 138740586474: 1 paquete PyPI analizado, 9 avisos (5 altos, 3 medios, 1 desconocido, 0 críticos). Identificadores: PYSEC-2024-225, PYSEC-2026-1283, PYSEC-2026-1285, PYSEC-2026-2141, PYSEC-2026-35, PYSEC-2026-3553, PYSEC-2026-3554, GHSA-537c-gmf6-5ccf, GHSA-h4gh-qq45-vh27. Los alias GHSA de avisos PYSEC no se cuentan por separado.
No atribuir automáticamente los avisos de PyPI al paquete Ubuntu con backports. Pendiente contraste con avisos de Canonical y versiones instaladas. La matriz de SCA separa Windows y GCP upstream, sin combinar sus resultados. Los inventarios no son instrucciones de instalación ni SBOM completo. Python, OpenSSL, SQLite y paquetes del SO quedan fuera del escaneo PyPI; requieren evaluación específica.
Controles relacionados: ISO/IEC 27002:2022 8.8, 8.25, 8.28, 8.29. No recalcular riesgo residual a partir de estos hallazgos sin evaluación y pruebas.
