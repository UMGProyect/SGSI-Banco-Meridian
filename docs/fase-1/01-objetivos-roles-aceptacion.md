# Fase 1 — Objetivos, responsabilidades y aceptación de riesgos

Estado: propuesta para revisión del equipo. No acredita aprobación institucional ni ejecución de controles.
Base: Proyecto final SGSI Banco Meridian v.2, apartados 3.3, 4.1, 4.6, 4.8, 4.9.1, 4.12 y Anexo A.
Alcance: P01 consulta de saldos de cuentas autorizadas y P02 transferencias internas en banca web y móvil. No se amplían los procesos ni se cambian identificadores, valoraciones o plazos del plan de tratamiento.

## 1. Objetivos de seguridad — incorporar en 4.9.1, después de la tabla de cláusulas

Los objetivos del SGSI se establecen para los procesos P01 y P02, tomando en consideración las necesidades de las partes interesadas, los resultados del BIA y los riesgos identificados. Su evaluación corresponde a los propietarios funcionales y técnicos, bajo seguimiento de la Unidad de Administración de Riesgos. Las metas siguientes son propuestas del caso académico y requieren aprobación antes de su aplicación. D+0 corresponde a la aprobación del plan de tratamiento, conforme al apartado 4.6.

| ID | Objetivo y proceso | Indicador y meta propuesta | Responsable | Recursos necesarios | Plazo de validación | Fuente / frecuencia prevista | Riesgos y controles |
|---|---|---|---|---|---|---|---|
| OBJ01 | Impedir accesos y operaciones sobre cuentas no autorizadas (P01/P02) | 100 % de los casos obligatorios de autorización superados; ningún acceso indebido confirmado en las pruebas | Desarrollo de Canales / Operaciones Digitales | Identidades de prueba, matriz de permisos, API y adaptador | D+30 | LAB03 y regresión integrada; en cada cambio | R02 / C02 |
| OBJ02 | Proteger la autenticación y las órdenes fuera de perfil (P01/P02) | 100 % de casos obligatorios de autenticación y verificación reforzada superados; ninguna orden elegible confirmada sin verificación | Seguridad e IAM / Operaciones | Directorio, factores de autenticación y reglas de perfil | R08 D+10; R01 D+30; revisión R08 D+45 | LAB02, registros de identidad y órdenes; mensual y tras cambios | R01, R08 / C01, C04 |
| OBJ03 | Preservar la integridad de transferencias (P02) | Cero asientos duplicados o discrepancias en los casos de concurrencia y reenvío; 100 % de órdenes inciertas del ejercicio conciliadas antes de reprocesar | Integraciones / Operaciones Digitales | Adaptador, registro transaccional y referencias persistentes | D+30 | LAB04, LAB05 y conciliación; por ejercicio y cambio | R03 / C02, C05 |
| OBJ04 | Recuperar los procesos críticos (P01/P02) | P01 RTO <=120 min y RPO <=5 min para datos de consulta; P02 RTO <=60 min y RPO 0 para asientos confirmados | TI y Continuidad / Operaciones | Enlaces, réplica, respaldo y sitio alterno | D+60 | Ejercicios representativos; semestral y tras cambios relevantes | R03, R04 / C03, C05, C07 |
| OBJ05 | Mantener trazabilidad de eventos críticos (P01/P02) | 100 % de eventos esperados de los casos de aceptación con referencia y campos obligatorios; alertas correlacionadas cuando proceda | Seguridad / SOC | Bitácoras, reglas y SIEM | D+45 | LAB06 y aceptación integrada; mensual | R05, R08 / C04 |
| OBJ06 | Proteger datos en equipos corporativos de soporte (P01/P02) | 100 % de casos obligatorios de cumplimiento, bloqueo y DLP superados en plataformas compatibles | TI / Seguridad | Equipos de prueba, MDM, DLP y EDR | D+60 | Registros de políticas y pruebas de aceptación; mensual | R06 / C06 |
| OBJ07 | Controlar identidades y secretos técnicos (P01/P02) | 100 % de identidades técnicas incluidas inventariadas y permisos revisados; rotación y revocación superadas en los casos obligatorios | TI / Seguridad | Inventario, repositorio de secretos y registros | D+60 | Registros de IAM y rotación; trimestral y tras cambios | R07 / C01, C08 |

Los porcentajes se calculan dividiendo el número de casos conformes entre el total de casos aplicables y multiplicando por 100. Si no hay casos aplicables o no hay evidencia, registrar no evaluado, no 100 %. La superación de casos de prueba no equivale a una garantía de eficacia permanente en producción. El RPO de P01 no autoriza la pérdida de asientos confirmados de P02. Las metas se revisan al menos trimestralmente y cuando cambie el riesgo, el alcance o los requisitos. Consolidar estos indicadores con 4.12.1, evitando duplicar tablas.

## 2. Roles y autoridades — complementar 4.1.3 y referenciar en 4.9.1

El Consejo de Administración aprueba el alcance, la política, los recursos y los criterios de aceptación del riesgo. El Comité de Gestión de Riesgos supervisa el tratamiento y eleva al Consejo las decisiones que excedan sus atribuciones. El Oficial de Seguridad coordina el SGSI, las medidas de protección y respuesta y reporta su desempeño. Operaciones Digitales conserva la propiedad de P01/P02 y autoriza la reapertura funcional tras las verificaciones técnicas y conciliación. TI ejecuta y mantiene los controles tecnológicos. Riesgos verifica la evaluación, el tratamiento y la evidencia residual; Cumplimiento revisa obligaciones aplicables; Auditoría Interna evalúa de forma independiente sin asumir la ejecución ni aceptación de controles.

Matriz propuesta de responsabilidades (A: autoridad final de la actividad; R: ejecutor; C: consultado; I: informado). Los roles pueden repetirse como A/R cuando corresponda. La aceptación residual se sujeta a la delegación formal y a los criterios del apartado 3.

| Actividad | Consejo | Comité | Seguridad | Operaciones | TI | Riesgos | Cumplimiento | Auditoría |
|---|---|---|---|---|---|---|---|---|
| Aprobar alcance, política y recursos | A | C | R | C | C | C | C | I |
| Evaluar riesgos y mantener matriz | I | A | C | C | C | R | C | I |
| Ejecutar tratamiento tecnológico | I | I | C | C | A/R | C | C | I |
| Conciliar y autorizar reapertura P01/P02 | I | I | C | A/R | R | C | C | I |
| Coordinar respuesta a incidentes | I | I | A/R | R | R | C | C | I |
| Supervisar plan y escalar riesgos | I | A | C | C | C | R | C | I |
| Evaluar obligaciones regulatorias | I | I | C | C | C | C | A/R | I |
| Auditoría independiente | I | I | C | C | C | C | C | A/R |
| Revisión del desempeño del SGSI | A | C | R | C | C | C | C | I |

Esta matriz complementa las funciones existentes; no presupone nuevos departamentos ni personal contratado. Las autoridades se formalizan mediante el proyecto de acta del Anexo A, sin simular firmas o aprobaciones reales.

## 3. Aceptación de riesgos — complementar 3.3, con referencia desde 4.6

Se mantienen los umbrales del modelo vigente. La aceptación se basa en el residual evaluado con evidencias, no en la proyección del plan de tratamiento. La propuesta de apetito distingue la operación ordinaria de excepciones temporales.

| Nivel | Criterio propuesto | Autoridad y seguimiento |
|---|---|---|
| Bajo (1–4) | Admisible si no incumple obligaciones ni criterios obligatorios de P01/P02 | Propietario del riesgo con delegación formal; revisión trimestral |
| Medio (5–9) | Admisible condicionadamente, con controles comprobados y seguimiento | Propietario del riesgo con validación de Riesgos, según delegación del Consejo; revisión trimestral |
| Alto (10–16) | Fuera de tolerancia ordinaria; requiere tratamiento. Excepción temporal solo si existe decisión expresa, medidas compensatorias, plazo y ausencia de incumplimiento | Comité dentro de atribuciones; Consejo cuando las exceda; revisión mensual o ante incidentes |
| Crítico (17–25) | No admisible en operación ordinaria; contención inmediata, escalamiento y restricción de la función afectada | Comité coordina escalamiento al Consejo; seguimiento hasta contención y nueva evaluación |

No se autorizará la operación afectada si existe incumplimiento obligatorio o no se puede verificar la integridad de los asientos confirmados y la autorización de las operaciones. La aceptación debe documentar ID del riesgo, propietario, puntuación actual, evidencia de eficacia, obligaciones, justificación, medidas compensatorias si proceden, autoridad, fecha, vencimiento y próxima revisión. No se considerará cerrado un tratamiento pendiente solo porque tenga un residual esperado bajo o medio.

Aplicación a los escenarios vigentes: R03 y R08 tienen residual actual estimado crítico (20); conservan contención inmediata del plan. R08 tiene residual esperado alto (10), que no constituye autorización de puesta en producción; exige la revisión y decisión previstas en 4.6. Las proyecciones de R01–R07 tampoco son aceptaciones efectivas.

## 4. Registro de cambios y verificación

- Insertar objetivos en 4.9.1 y consolidar con indicadores de 4.12.1.
- Complementar roles en 4.1.3; conservar alcance y contexto de 4.1 y proyecto de acta.
- Complementar 3.3 con criterios de aceptación; referenciar en 4.6.
- No modificar tablas de riesgo ni BIA en esta actividad.
- Pendiente de revisión del equipo: delegaciones, metas y recursos; anexos B y C; justificación verídica de organización ficticia.
- Criterio de cierre de esta actividad: revisión de coherencia con v.2 y aprobación del equipo antes de integrar. Sin evidencias de Azure nuevas.
