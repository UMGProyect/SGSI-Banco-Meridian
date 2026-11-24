# Fase 1 — Evaluación del desempeño y mejora continua

Estado: propuesta académica para revisión. No constituye auditoría realizada, revisión directiva aprobada ni prueba nueva.
Base: informe v.2, apartados 4.6, 4.9.1, 4.11, 4.12, 4.12.1, 4.13 y Anexo A; propuestas 01–03 de esta fase.
Alcance: P01 consulta de saldos y P02 transferencias internas de banca web y móvil, incluidos únicamente sus activos y dependencias necesarios.

## 1. Seguimiento, medición, análisis y evaluación (ISO/IEC 27001:2022, 9.1)

Consolidar los siguientes indicadores con la tabla de objetivos OBJ01–OBJ07 y sustituir la tabla de indicadores de 4.12.1, conservando el caso de R03 sobre incidente y cambio. Las metas son propuestas; los plazos y prioridades del plan de tratamiento original prevalecen.

| Indicador | Objetivo | Método y meta de aceptación | Fuente / responsable | Frecuencia propuesta |
|---|---|---|---|---|
| IND01 Autorización por cuenta | OBJ01 | Casos obligatorios superados / casos obligatorios aplicables x 100 = 100 %; cero accesos indebidos confirmados en el ejercicio | LAB03 y regresión integrada; Desarrollo/Operaciones | Por cambio y ejercicio |
| IND02 Autenticación reforzada | OBJ02 | Órdenes elegibles con verificación válida / órdenes elegibles x 100 = 100 % en el ejercicio; casos obligatorios de identidad superados = 100 % | LAB02 y registros IAM/órdenes; Seguridad/IAM y Operaciones | Mensual y por cambio |
| IND03 Integridad de transferencias | OBJ03 | Conteo de asientos duplicados = 0 en regresión; órdenes inciertas conciliadas antes de reprocesar / órdenes inciertas del ejercicio x 100 = 100 % | LAB04–LAB05, libro transaccional; Operaciones/Integraciones | Por cambio y ejercicio |
| IND04a RTO P01 | OBJ04 | Tiempo desde interrupción hasta recuperación funcional verificada <=120 min | Registro de ejercicio; TI/Operaciones | Semestral y por cambio relevante |
| IND04b RPO P01 | OBJ04 | Antigüedad del punto recuperado respecto del evento <=5 min, sin presentar saldos obsoletos como vigentes | Registro de recuperación y conciliación; TI/Operaciones | En cada ejercicio |
| IND04c RTO P02 | OBJ04 | Tiempo desde interrupción hasta recuperación funcional y conciliación verificadas <=60 min | Registro de ejercicio; TI/Operaciones | En cada ejercicio |
| IND04d RPO P02 | OBJ04 | Cero asientos confirmados perdidos; comparar referencias, importes y estados contra registro de referencia independiente | Libro y registro de prueba; TI/Operaciones | En cada ejercicio |
| IND05 Trazabilidad | OBJ05 | Eventos esperados con campos obligatorios y referencia / eventos esperados x 100 = 100 %; correlacionar alertas cuando proceda | LAB06 y registros integrados; SOC | Mensual y por ejercicio |
| IND06 Protección de equipos | OBJ06 | Casos obligatorios conformes de postura, DLP y EDR / casos aplicables x 100 = 100 % | Registros de política y aceptación; TI/Seguridad | Mensual y por cambio |
| IND07 Identidades técnicas | OBJ07 | Identidades en inventario con permisos revisados / identidades técnicas descubiertas en alcance x 100 = 100 %; pruebas obligatorias de rotación y revocación = 100 % | Inventario y registros IAM; TI/Seguridad | Trimestral y por cambio |
| IND08 Tratamiento | Transversal | Acciones vencidas abiertas (conteo) = 0; reportar también acciones completadas con evidencia / acciones previstas al corte | Matriz E4.6; Riesgos | Trimestral y ante riesgo crítico |
| IND09 Detección y contención | OBJ05 | Registrar tiempos desde evento detectable hasta detección y desde detección hasta contención verificada; metas según SLA aprobados, aún no definidos | Registro de incidentes; SOC | Mensual y por ejercicio |

Para cada medición registrar periodo, versión, alcance, población, casos excluidos justificados, resultado, fuente, responsable y análisis. Comparar resultados homogéneos; separar laboratorio local y arquitectura objetivo. Sin evidencia o con denominador cero registrar no evaluado/no aplicable justificado, no cumplimiento automático. Un resultado de laboratorio no se extrapola a producción ni acredita el BIA. Riesgos consolida los resultados trimestralmente, los propietarios analizan desviaciones y el Oficial de Seguridad presenta informe al Comité. Ante pérdida de integridad, autorización o un riesgo crítico aplicar contención y escalamiento sin esperar el corte periódico.

## 2. Auditoría interna (9.2)

Auditoría Interna prepara un programa anual propuesto basado en importancia de procesos, riesgos, cambios, resultados previos y capacidad disponible. Cada auditoría define objetivo, alcance P01/P02, criterios (requisitos aplicables del SGSI, políticas propias y controles seleccionados), métodos, muestreo, responsables, fecha y destinatarios. Designar auditores competentes e independientes de las actividades auditadas; no auditar el propio trabajo. Comunicar resultados a la dirección pertinente y conservar programa, plan, papeles de trabajo, informe y seguimiento.

| Auditoría propuesta | Prioridad / periodo | Objeto y muestra mínima propuesta | Evidencia requerida |
|---|---|---|---|
| AUD01 | Alta / primer trimestre del ciclo | Alcance, política, objetivos, BIA, riesgos y SoA; revisar R03/R08 y sus tratamientos | Versiones, autorizaciones, matriz y evidencia residual |
| AUD02 | Alta / segundo trimestre | Identidad, autorización, integridad y trazabilidad; revisar casos de P01/P02 y controles C01/C02/C04/C08 | Casos, configuraciones, registros y conciliación |
| AUD03 | Alta / tercer trimestre | Continuidad, conectividad híbrida, equipos y proveedores; C03/C05/C06/C07 | Ejercicios, configuración, contratos o supuestos identificados |
| AUD04 | Seguimiento / cuarto trimestre | Cierre de hallazgos, objetivos y mejora; ajustar por resultados previos | Acciones, revalidaciones y decisiones |

El calendario corresponde a una propuesta para el escenario objetivo, no a fechas comprometidas del curso. Puede ajustarse por riesgos y disponibilidad, justificando los cambios. Mientras el entorno objetivo no exista, una auditoría documental solo evalúa el diseño y sus registros disponibles; las pruebas de eficacia pendientes se mantienen como tales.

Clasificación interna propuesta: no conformidad cuando existe incumplimiento de un criterio identificado con evidencia objetiva; observación cuando hay una debilidad sin incumplimiento demostrado; oportunidad de mejora cuando se propone optimizar un aspecto conforme. La ausencia de una prueba de producción en una etapa de diseño es una brecha pendiente, no automáticamente una no conformidad. Registrar criterio, hecho, evidencia, impacto y responsable sin confundir una vulnerabilidad técnica con una no conformidad del SGSI.

## 3. Revisión por la dirección (9.3)

El Consejo, como autoridad propuesta del modelo, revisa el SGSI al menos anualmente y tras cambios relevantes o exposición que requiera decisión extraordinaria. El Comité prepara el informe con el Oficial de Seguridad y Riesgos; no sustituye la autoridad del Consejo. La supervisión trimestral prevista en 4.12 se conserva.

Entradas mínimas: estado de decisiones anteriores; cambios internos y externos pertinentes; cambios de necesidades y expectativas de partes interesadas; tendencias de no conformidades y acciones correctivas, resultados de seguimiento y medición, auditorías y cumplimiento de objetivos; retroalimentación de partes interesadas; resultados de evaluación de riesgos y estado del tratamiento; oportunidades de mejora. Incorporar también suficiencia de recursos, dependencias y resultados de continuidad pertinentes a P01/P02.

Salidas: decisiones sobre oportunidades de mejora y cambios necesarios al SGSI, acciones, recursos, responsables, plazos y seguimiento. Registrar también decisiones sobre riesgos dentro de atribuciones, con su evidencia y justificación. Conservar acta y anexos; no simular aprobación, firma ni reunión que no haya ocurrido. Revisar el alcance vigente sin ampliarlo por defecto.

## 4. No conformidades, acciones correctivas y mejora continua (10.1 y 10.2)

Ante una no conformidad: reaccionar y controlar/corregir el incumplimiento y atender sus consecuencias; evaluar la necesidad de eliminar su causa mediante revisión y análisis, incluyendo si existen o podrían ocurrir situaciones similares; ejecutar acciones necesarias; verificar eficacia y modificar el SGSI cuando proceda. La acción debe ser proporcional a los efectos. Conservar naturaleza del hallazgo, acciones y resultados de eficacia.

Flujo: hallazgo registrado -> corrección/contención -> análisis causal -> acción correctiva con responsable y plazo -> verificación independiente cuando corresponda -> cierre o reapertura. Actualizar matriz de riesgos, SoA, documentación y pruebas si el análisis lo requiere, sin cambiar puntuaciones por presunción. El cierre no equivale a aceptar riesgo residual. Mejorar continuamente adecuación, suficiencia y eficacia del SGSI mediante decisiones basadas en IND01–IND09, auditorías, incidentes, cambios y revisiones.

Ejemplo de aplicación hipotética a R03: si una prueba integrada generase un asiento duplicado contrariando la política de integridad, Operaciones detendría el reproceso, conciliaría el estado y abriría incidente. TI analizaría la causa (sin asumirla antes de investigar), evaluaría otros flujos afectados, propondría cambio autorizado y repetiría pruebas de concurrencia y reenvío. Un revisor verificaría que el criterio se cumple y que no reaparece la desviación. Riesgos revisaría el residual con evidencia. El informe v.2 reporta LAB04/LAB05 satisfactorias; este ejemplo no declara un fallo observado.

## 5. Integración en el informe

- Complementar 4.9.1 con referencias a 4.12 y a los instrumentos de gestión; sustituir la tabla de 4.12.1 por la versión consolidada de indicadores.
- Añadir a 4.12, después del seguimiento existente, la síntesis de auditoría, revisión directiva y mejora; no duplicar la explicación de COBIT/ITIL.
- Mantener intactos BIA, riesgos, plan de tratamiento y resultados del laboratorio.
- Instrumentos: 05-plantillas-evaluacion-mejora.md; incorporar al anexo de gestión o conservar como documentación editable vinculada.
- Cierre documental: trazabilidad de objetivos, criterios, responsables, frecuencia y evidencias; revisión del equipo antes de integrar en main. La ejecución de auditorías y revisiones del entorno objetivo queda pendiente.
