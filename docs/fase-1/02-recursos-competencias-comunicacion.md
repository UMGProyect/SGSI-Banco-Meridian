# Fase 1 — Recursos, competencias, comunicación e información documentada

Estado: propuesta de gestión para revisión académica. No acredita contratación, aprobación presupuestaria, capacitación ejecutada ni operación de herramientas.
Base: informe v.2, apartados 4.1, 4.6, 4.8, 4.9.1, 4.10, 4.12, 4.13 y anexos A–C; propuesta 01-objetivos-roles-aceptacion.md.
Alcance: exclusivamente P01 consulta de saldos de cuentas autorizadas y P02 transferencias internas de la banca web y móvil. No se incluyen otros productos bancarios.

## 1. Recursos (ISO/IEC 27001:2022, 7.1)

La asignación de recursos se deriva del plan de tratamiento vigente. El Oficial de Seguridad consolida las necesidades con TI y Operaciones; el Comité revisa su suficiencia y eleva al Consejo la solicitud de recursos. Se distinguen recursos del escenario objetivo y recursos efectivamente disponibles en el laboratorio.

| ID | Recursos requeridos | Responsable de preparación | Destino | Evidencia de suficiencia / estado inicial |
|---|---|---|---|---|
| REC01 | Personal IAM, identidades sintéticas, directorio y factores de autenticación | Seguridad / IAM | OBJ02; R01, R08; C01 | Matriz de permisos, cobertura de factores y licencias; pendiente de validación integrada |
| REC02 | Desarrollo, Integraciones, QA, API, adaptador y registro transaccional | TI / Operaciones | OBJ01, OBJ03; R02, R03; C02 | Prototipo y pruebas LAB03–LAB05 reportadas; código y registros aún por verificar |
| REC03 | Servicios Azure, conectividad local, rutas alternas, almacenamiento y capacidad de recuperación | TI / Continuidad | OBJ04; R03, R04; C03, C05, C07 | Inventario de recursos, presupuesto y pruebas de falla; despliegue pendiente |
| REC04 | SOC, fuentes de eventos, almacenamiento y reglas de correlación | Seguridad / SOC | OBJ05; R05, R08; C04 | LAB06 reportada; SIEM y fuentes integradas pendientes |
| REC05 | Dispositivos corporativos de prueba, administración y licencias compatibles | TI / Seguridad | OBJ06; R06; C06 | Compatibilidad, licencias y evidencia de inscripción, cumplimiento, DLP y EDR; pendiente |
| REC06 | Identidades de carga de trabajo, repositorio autorizado de secretos, certificados y registros | TI / Seguridad | OBJ07; R07; C01, C08 | Inventario y pruebas de rotación y revocación; pendiente |
| REC07 | Tiempo de Riesgos, Cumplimiento, Auditoría y propietarios; almacenamiento documental autorizado | Oficial de Seguridad | G01/G02; seguimiento de todos los objetivos | Plan aprobado, registros de revisión y auditoría; pendiente |

Antes de comprometer recursos, documentar cantidad/capacidad, licencias, costo estimado en Q o USD, periodo, responsable, dependencia y aprobación. No se asignan montos ni dotaciones inventados. Si un recurso no está disponible, registrar la brecha, su efecto sobre el tratamiento, alternativa, responsable y fecha de revisión. Mantener los plazos D+10, D+30, D+45 y D+60 establecidos en 4.6; cualquier modificación requiere revisión del plan.

## 2. Competencias (7.2) y toma de conciencia (7.3)

El Oficial de Seguridad mantiene una matriz de competencias por función. Cada jefe de área verifica la competencia antes de delegar actividades críticas. La capacitación no se acredita únicamente por asistencia: debe incluir evaluación o ejercicio pertinente.

| ID | Rol existente | Competencia necesaria | Verificación propuesta | Riesgo/control |
|---|---|---|---|---|
| COMP01 | IAM y Seguridad | Autenticación, revocación, privilegios mínimos y gestión de excepciones | Ejecutar casos de acceso permitido, denegado y revocado; conservar resultado | R01/R07/R08; C01 |
| COMP02 | Desarrollo e Integraciones | Autorización por cuenta, idempotencia, TLS y cambios seguros | Revisión de reglas y regresión LAB03–LAB05 | R02/R03; C02/C08 |
| COMP03 | Operaciones Digitales | Conciliación, validación de estado y reapertura | Resolver un caso sintético de orden incierta sin generar un nuevo débito | R03/R08; C02/C05 |
| COMP04 | Redes, Infraestructura y Continuidad | Conectividad híbrida, respaldo, restauración y conmutación | Ejercicio controlado con medición de RTO/RPO y registro de dependencia | R04; C03/C05/C07 |
| COMP05 | SOC | Clasificación, correlación, contención y custodia de evidencia | Correlacionar una alerta con una referencia y documentar su escalamiento | R05/R08; C04 |
| COMP06 | Soporte y Seguridad | Postura del dispositivo, DLP y EDR | Comparar equipo conforme y no conforme y registrar decisión | R06; C06 |
| COMP07 | Riesgos, Cumplimiento y Auditoría | Evaluación de riesgo, obligaciones y revisión independiente según función | Revisar un expediente sintético de tratamiento y sus evidencias | G01/G02 |

Programa propuesto: inducción antes de otorgar acceso a funciones en alcance; refuerzo anual y tras cambios o incidentes relevantes. Temas mínimos: fraude y phishing, credenciales y privilegios, información financiera, reporte de incidentes, consecuencias de incumplir políticas y contribución de cada rol al SGSI. Operaciones comunica a clientes recomendaciones sobre uso seguro de P01/P02, canales oficiales y reporte de operaciones no reconocidas; no se exige inscripción MDM de dispositivos personales de clientes.

Registro mínimo de competencia: rol, competencia requerida, evaluación inicial, brecha, acción formativa, fecha prevista, evidencia de evaluación, resultado, responsable y próxima revisión. Si falta competencia, limitar la autorización o establecer supervisión hasta verificarla. No registrar asistencia ni resultados ficticios como hechos.

## 3. Comunicación (7.4)

| Qué comunicar | Cuándo | Destinatario | Emisor | Canal y registro |
|---|---|---|---|---|
| Alcance, política y responsabilidades | Al aprobarse o cambiar; inducción | Personal involucrado en P01/P02 | Oficial de Seguridad | Repositorio controlado y registro de comunicación |
| Exposición, objetivos y tratamiento | Trimestral; inmediatamente si el riesgo es crítico | Comité; Consejo según atribuciones | Riesgos / Seguridad | Informe y decisión registrada |
| Incidente de fraude, pérdida de trazabilidad o caída | Al detectar, clasificar y escalar según gravedad; sin esperar informe periódico | SOC, Seguridad, TI, Operaciones y Cumplimiento según caso | SOC / Oficial de Seguridad | Ticket, referencias, tiempos, acciones y evidencias |
| Estado de continuidad y reapertura | Durante ejercicio o interrupción, por hitos del plan 4.11 | TI, Continuidad, Operaciones, Seguridad | TI / Operaciones | Registro de recuperación y autorización funcional |
| Cambios en controles o servicios | Antes de ejecutar y al cerrar el cambio | Áreas afectadas y autorizadores | TI / propietario del cambio | Solicitud de cambio, prueba, reversión y cierre |
| Obligaciones externas o incidentes sujetos a notificación | Según obligación aplicable, validada por Cumplimiento | Autoridad o tercero correspondiente | Responsable facultado, coordinado por Cumplimiento | Comunicación oficial, acuse y expediente |
| Indisponibilidad o recomendaciones de seguridad | Cuando proceda; durante incidentes relevantes | Clientes afectados de P01/P02 | Operaciones Digitales | Canales oficiales, texto aprobado y constancia |

La comunicación no debe divulgar credenciales, datos financieros innecesarios ni evidencia restringida. Cumplimiento determina destinatarios, requisitos y plazos regulatorios aplicables; esta matriz no inventa plazos legales. Las comunicaciones externas y sus autorizaciones se conservan como evidencia.

## 4. Información documentada (7.5)

El Oficial de Seguridad mantiene el registro maestro. Cada documento tiene identificador, título, versión, propietario, clasificación, fecha, estado, aprobación cuando corresponda y ubicación. Estados: borrador, en revisión, aprobado/vigente y sustituido. El Word v.2 permanece como línea base; las propuestas de GitHub no constituyen aprobación del banco ficticio.

| Documento o registro | Propietario funcional | Ubicación lógica prevista | Acceso |
|---|---|---|---|
| Alcance, política y acta | Oficial de Seguridad / Consejo | docs/ y Anexo A | Lectura por personal autorizado; aprobación según gobierno |
| Inventario, BIA, riesgos, mapa, tratamiento, OCTAVE y SoA | Riesgos y propietarios respectivos | matrices/ y Anexo B | Escritura restringida; revisión de Riesgos |
| Configuraciones y código de prueba | TI | infraestructura/, src/, tests/ | Desarrollo y revisión autorizados |
| Registros de pruebas y aceptación | TI / Seguridad / Operaciones según control | evidencias/ y Anexo C | Acceso mínimo; registros depurados |
| Incidentes y conciliación | Seguridad / Operaciones | Expediente autorizado (fuera de Git si contiene información sensible) | Acceso por función |
| Continuidad y recuperación | TI / Continuidad | continuidad/ | Responsables de recuperación y revisión |
| Auditorías, revisión directiva y acciones correctivas | Auditoría / Seguridad / Consejo según registro | Expediente autorizado | Independencia y acceso restringido |

Procedimiento:
1. Crear o modificar en una rama de trabajo, indicar motivo, versión y relación con requisito, objetivo, activo, riesgo o control.
2. Revisar exactitud, coherencia con P01/P02, confidencialidad y evidencia. El propietario valida contenido; la autoridad designada aprueba conforme a la matriz RACI.
3. Integrar en main tras revisión de diferencias. Mantener historial de cambios y distinguir versión académica de estado de aprobación institucional.
4. Controlar acceso con mínimo privilegio. No subir credenciales, tokens, llaves privadas, datos de clientes ni estados sensibles de infraestructura. .gitignore es una ayuda, no un mecanismo suficiente de protección.
5. Registrar evidencia con identificador de prueba, versión del código/configuración, fecha y zona horaria, entorno, datos sintéticos, resultado esperado y observado, responsable y ubicación; usar SHA-256 cuando corresponda y verificarlo contra el archivo.
6. Revisar disponibilidad, respaldo, conservación, disposición y requisitos legales. Los plazos se definen por Cumplimiento y propietario según categoría; no eliminar evidencias sujetas a investigación o conservación obligatoria.
7. Identificar documentación externa necesaria, registrar edición/fecha y fuente autorizada, y revisar cambios aplicables al alcance. No reproducir estándares completos sin autorización.

## 5. Instrumentos y criterio de cierre

Plantillas de registros: 03-plantillas-apoyo.md. Incorporar síntesis de este apartado después de los objetivos de 4.9.1; vincular el programa de concientización de 4.8 y los mecanismos de seguimiento de 4.12. Evitar repetir las matrices completas en el cuerpo del informe si se incluyen como anexos controlados.

Cierre de esta actividad documental: verificar que los siete objetivos OBJ01–OBJ07 tienen recursos y responsables, que las competencias y comunicaciones corresponden a P01/P02, y que los registros tienen propietarios, revisión y protección. La ejecución y disponibilidad de recursos se verifican posteriormente. No modificar el alcance, las puntuaciones ni los resultados de laboratorio.
