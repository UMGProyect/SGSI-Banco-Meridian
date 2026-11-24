# Política de seguridad y publicación académica

Banco Meridian es un escenario ficticio limitado a P01/P02. Repositorio en desarrollo privado hasta revisión y autorización explícita. El código no autoriza acceso a Google Cloud ni al laboratorio TCP/IP separado.

## Material publicable
Código y configuraciones sin secretos, ejemplos con valores ficticios, documentación SGSI, matrices con datos sintéticos y evidencias depuradas y revisadas. Revisar derechos de autor, datos personales, metadatos, direcciones públicas, identificadores de infraestructura y nombres de usuario antes de publicar. Los identificadores de proyecto no son credenciales; el ID real ya figura en el historial y debe evaluarse en la revisión de exposición.

## Material prohibido
Contraseñas, tokens, claves privadas, factores MFA, JSON de credenciales, ADC, archivos de estado y planes Terraform, variables reales, bases de datos, respaldos, capturas de tráfico y registros sin depurar. Usar almacenamiento privado y autorizado fuera de Git. .gitignore no elimina archivos ya rastreados ni reemplaza controles de acceso.
Nunca publicar una captura de una consola con cuentas, tokens, datos de facturación o información personal. Mantener original de evidencia en expediente privado; publicar versión depurada con identificación de prueba, fecha, versión, criterio y resultado.

## Hallazgos
Notificar de forma privada al mantenedor del repositorio (canal acordado con el equipo). No abrir un issue público con secretos ni detalles explotables de servicios activos. Si se detecta un secreto, revocar/rotar primero, investigar uso, revisar referencias e historial y retirar copias expuestas; reescribir historia solo con autorización y coordinación, sin asumir que elimina forks o clones existentes. Nunca realizar pruebas sobre infraestructura ajena.

## GitHub Actions
Validación sin credenciales de GCP, permisos contents: read, acciones fijadas por SHA, sin pull_request_target, sin secretos, sin OIDC y sin despliegue automático. No imprimir valores ni adjuntar informes crudos de secretos. Antes de ejecutar nuevos analizadores, revisar su procedencia, versiones, dependencias, salidas y condiciones de uso. Los resultados de un workflow de PR no son prueba suficiente de autorización de publicación.

La futura WIF debe ser una decisión separada: identidad de despliegue de mínimo privilegio, condiciones de emisor/audiencia, IDs numéricos de propietario y repositorio, ref y flujo autorizado, entorno protegido cuando disponible, sin confianza a PR/forks. No se crea ningún pool ni se otorgan roles en esta actividad.

Ver docs/seguridad/PUBLICACION.md para las verificaciones y criterios.
