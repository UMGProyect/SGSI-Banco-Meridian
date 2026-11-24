# Preparación para publicación — SGSI Banco Meridian
Fecha: 2026-11-24. Alcance: repositorio UMGProyect/SGSI-Banco-Meridian; sin cambios en proyecto TCP/IP ni despliegue GCP.
Estado: preparativos de seguridad; publicación NO autorizada.

| Control | Evidencia / mecanismo | Criterio antes de publicar |
|---|---|---|
| Exclusión de datos sensibles | .gitignore y check_tracked_files.py | Cero rutas prohibidas rastreadas o en historia alcanzable |
| Secretos | Gitleaks CLI en CI, imagen fija v8.30.1 y digest | Escanear ramas, tags, HEAD y árbol; cero hallazgos no tratados; revisión manual de falsos positivos |
| IaC | Terraform init -backend=false y validate; revisión manual de reglas, IAM, redes y configuración | Validación exitosa y análisis IaC específico (Checkov u otro) revisado |
| SAST/SCA/DAST | Semgrep/OSV-Scanner/ZAP previstos al incorporar aplicación y dependencias | Ejecutar contra código real y entorno autorizado; documentar resultados y remediación |
| Dependencias de automatización | SHA de acciones, imagen por digest, Dependabot para github-actions | Revisar actualizaciones, lockfile Terraform y dependencias de app |
| Historial y metadatos | Revisión de ramas/tags, autores/emails, PR, issues, releases, Actions y archivos adjuntos | Sin material privado ni datos personales no autorizados |
| Evidencias | Revisión manual de capturas, PDF, DOCX, XLSX, ZIP y metadatos | Publicar solo copias depuradas; originales fuera de Git |
| Acceso a GCP | Revisar IAM efectivo, cuentas de servicio, reglas y exposición; sin credenciales en CI | No acceso público administrativo; sin permisos inesperados ni claves expuestas |
| Ajustes GitHub | Actions de lectura, evitar aprobación automática, secret scanning y push protection si disponibles, protección de main/PR | Verificar en consola; disponibilidad depende de plan/visibilidad |
| Autorización | Revisión por equipo y aprobación explícita | Acta/registro de publicación con fecha y commit revisado |

## Procedimiento de verificación final
1. En clon nuevo y autorizado, obtener todas las ramas y etiquetas y revisar refs; ejecutar el workflow y una revisión independiente del historial. Revisar también PR cerrados, ramas eliminadas, objetos no alcanzables cuando proceda, forks, LFS, releases, logs, artefactos, issues y wikis. El escaneo Git no cubre automáticamente esas superficies.
2. Revisar documentos y archivos binarios manualmente, incluidos comentarios, cambios controlados, propiedades, hojas ocultas y adjuntos. No subir originales sensibles al repositorio.
3. Validar resultados en el commit que se pretende publicar y corregir hallazgos. Un PASS de Gitleaks solo acredita su cobertura, no ausencia universal de secretos. No subir reportes crudos. Revocar credenciales descubiertas incluso si todavía eran privadas.
4. Confirmar que el despliegue no requiere exponer IP, cuentas ni secretos. Si la infraestructura sigue activa, evaluar si conviene apagar/eliminar recursos públicos al finalizar las pruebas; revisar créditos y permisos antes de hacerlo.
5. Verificar ajustes en Settings > Actions y Settings > Security (o Advanced Security), y reglas de ramas; activar lo disponible con mínimo privilegio. GitHub Free privado puede no ofrecer todos los controles nativos; confirmar antes y después del cambio. No modificar visibilidad por automatización.
6. Autorizar publicación explícita y verificar acceso anónimo a contenido revisado, no a Google Cloud.

## Registro de control
| Fecha | Commit revisado | Control | Resultado observado | Evidencia | Responsable/decisión |
|---|---|---|---|---|---|
| | | | Pendiente | | |

## Relación SGSI
POL04, POL06, C08 y controles ISO/IEC 27001:2022 Anexo A 8.4, 8.9, 8.12, 8.24, 8.25, 8.28, 8.29 y 8.32. No modifica la SoA ni acredita implementación integral de dichos controles.

## Fuentes verificadas
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository
- https://github.com/gitleaks/gitleaks
- https://github.com/gitleaks/gitleaks/pkgs/container/gitleaks
- https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines
