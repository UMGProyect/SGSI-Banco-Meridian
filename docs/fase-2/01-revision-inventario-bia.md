# Fase 2 — Revisión de línea base E2.1 y E2.2

Fecha: 24 de noviembre de 2026. Fuentes: Matrices del SGSI Banco Meridian.xlsx (hojas Inventario, BIA y Riesgos), Proyecto final SGSI Banco Meridian v.3 - fase 1.docx (3.2, 4.2 y 4.3), y documentos de fase 1. Rama derivada de fase-1-modelo-sgsi en d226d2e; integración de fase 1 en main aún pendiente. Esta revisión no modifica archivos originales ni constituye validación operativa.

## Inventario

23 activos con identificadores únicos, campos de propietario, custodio, tipo, ubicación, información tratada, CID, criticidad, dependencias y procesos. Se conservan los 23 con criticidad alta: 3.2 establece impacto material sobre fondos, operación, recuperación u obligación como criterio. La criticidad no equivale a prioridad cronológica de restauración. No reclasificar sin evidencia. Los servicios y funciones compartidos solo se incluyen por su efecto en P01/P02.

### Hallazgos de dependencias

| ID | Evidencia | Acción propuesta |
|---|---|---|
| DEP01 | A02.2 y A08.1 se referencian mutuamente | Distinguir autenticación del equipo de administración del directorio; verificar acceso de emergencia autorizado e independiente del equipo habitual. |
| DEP02 | A02.2 y A10.1 se referencian mutuamente | Distinguir custodia/administración de llaves de uso de certificados; probar recuperación de identidad y acceso seguro a material criptográfico sin dependencia circular. |
| DEP03 | A06.1 y A09.1 se referencian mutuamente | Separar generación de respaldos en operación normal de restauración de datos durante contingencia. |
| DEP04 | A06.2 y A09.1 se referencian mutuamente | Separar respaldo de recuperación; verificar durabilidad y reconciliación para RPO cero de asientos confirmados. |
| DEP05 | A08.1 y A08.2 se referencian mutuamente | Distinguir inscripción/telemetría del equipo y aplicación de postura/políticas; probar recuperación de acceso de soporte sin eludir controles. |

Dos grupos fuertemente conexos en el grafo de dependencias por ID: A02.2/A08.1/A08.2/A10.1 y A06.1/A06.2/A09.1. No implica ciclos de ejecución demostrados. Validar dirección y tipo de dependencia con propietarios. A09.3/A09.4 tienen dependencias de instalaciones descritas en texto; conservarlas como dependencias externas o físicas, no introducir identificadores arbitrarios.

## BIA

| Proceso | RTO min | RPO min | MTPD min | Demanda estimada/h |
|---|---:|---:|---:|---:|
| P01 | 120 | 5 | 360 | 300 |
| P02 | 60 | 0 (asientos confirmados) | 240 | 90 |

RTO inferior a MTPD para ambos. Los 10 valores de demanda potencial almacenados concuerdan con demanda por hora x minutos / 60. P01: 150, 300, 600, 1200 y 1800. P02: 45, 90, 180, 360 y 540. Son solicitudes potenciales bajo demanda estimada de alta actividad, no pérdidas observadas, capacidad mínima de servicio ni montos monetarios. Las cinco dimensiones de impacto están presentes y no decrecen conforme al tiempo.

| ID | Observación | Acción propuesta |
|---|---|---|
| BIA01 | A05.1 adaptador no figura directamente en lista BIA, pero A03.1 lo referencia en Inventario | Identificar dependencias directas y transitivas; incorporar el adaptador explícitamente al recorrido crítico de los ejercicios. |
| BIA02 | La meta de RPO de P01 ya distingue datos de lectura y remite al criterio más estricto cuando se comparte fuente con P02 | Conservar; no permitir pérdida de asientos confirmados ni presentar saldos obsoletos como vigentes. |
| BIA03 | 300/90 representan demanda por hora estimada, no capacidad mínima validada | Definir capacidad mínima y criterio de cola/conciliación con Operaciones. No inventar capacidad ni cifras de pérdida monetaria. |
| BIA04 | RTO/RPO/MTPD e impactos son supuestos académicos | Mantener objetivos; verificar recuperación funcional, referencias, saldos, durabilidad y escenarios de interrupción representativos. |

Secuencia de recuperación propuesta, pendiente de prueba: (1) infraestructura, energía, conectividad, resolución, identidad y material criptográfico indispensables; (2) core, datos, réplica y adaptador con integridad verificada; (3) API, perímetro y canales, controles de autorización y trazabilidad; (4) conciliación y reapertura autorizada por Operaciones. Las actividades pueden ser paralelas; priorizar la recuperación P02 sin impedir P01 si su integridad está verificada. La secuencia no sustituye controles de seguridad ni supone tiempos de recuperación por activo ya medidos.

## Control de cambios

R07 en Riesgos!C12 incluye A02.1 (identidad de clientes), A05.1 y A10.1 para secretos técnicos; revisar en fase 3 si A02.1 es dependencia pertinente o si el inventario debe explicitar identidades de carga de trabajo. No modificar riesgos en esta actividad. Las fórmulas de mapa y tratamiento referencian filas 6–13 de Riesgos: extender y probar de forma coordinada si se añaden riesgos en fase 3; no es error para ocho escenarios.

## Vigencia normativa

Consulta de catálogo ISO 24/11/2026: ISO/IEC 27005:2022 (https://www.iso.org/standard/80585.html); ISO 22301:2019 (https://www.iso.org/standard/75106.html) con Amd 1:2024 (https://www.iso.org/standard/88412.html). Existe revisión ISO/CD 22301 en desarrollo (https://www.iso.org/es/contents/data/standard/09/36/93606.html), no sustituye la edición publicada. Considerar cambio climático en dependencias eléctricas, conectividad, climatización y sitio alterno sin ampliar alcance. No se afirma certificación ni cumplimiento regulatorio exhaustivo.

## Cierre de actividad

Revisión de línea base realizada; pendientes: validación de tipos de dependencia, criterios de recuperación y capacidad mínima; pruebas de fórmulas ante cambios; actualización coordinada de Excel y Word. Conservar original y proponer modificaciones sobre copia antes de integración. No se modifica main, ni se incorpora información bancaria real.
