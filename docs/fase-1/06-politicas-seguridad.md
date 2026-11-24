# Fase 1 — Políticas de seguridad de la información

Versión propuesta: 0.1. Estado: borrador para revisión académica y aprobación prevista por el Consejo. Base: informe v.2, apartados 4.8, 4.9, 4.10, 4.11, 4.12 y Anexo A. No acredita controles implementados ni aprobación institucional.

## Disposiciones comunes

Las siete políticas conservan las categorías del apartado 4.8. Su ámbito obligatorio, una vez aprobadas, comprende P01 (consulta de saldos de cuentas autorizadas) y P02 (transferencias entre cuentas del propio banco) en banca web y móvil, sus datos, personal, proveedores, interfaces y dependencias necesarias. No se extienden a productos bancarios excluidos. Los requisitos a terceros deben incorporarse en acuerdos aplicables. No se presume administración corporativa de dispositivos personales de clientes.

El Consejo aprueba la política general, alcance y recursos; las políticas específicas se aprueban por la autoridad facultada conforme a la delegación formal. El Oficial de Seguridad coordina su comunicación y revisión al menos anual, y tras cambios relevantes, incidentes u obligaciones nuevas. Cada propietario conserva evidencias de cumplimiento conforme a REG-04 y REG-05. Las desviaciones se evalúan según el criterio incumplido y su evidencia; cuando proceda se aplica REG-09. Las excepciones requieren justificación, análisis de riesgo, propietario, medidas compensatorias, vigencia, autoridad facultada y revisión; no pueden dispensar obligaciones legales ni permitir operaciones sin integridad o autorización verificables.

## POL01 — Política general del SGSI

Propietario: Oficial de Seguridad. Aprobación prevista: Consejo.
Finalidad: preservar confidencialidad, integridad y disponibilidad de P01/P02 y orientar el cumplimiento de obligaciones aplicables.
- La dirección debe aprobar y mantener el alcance, la política, las responsabilidades, los recursos y el marco de objetivos de seguridad.
- Debe mantenerse un proceso de evaluación y tratamiento de riesgos, con criterios de aceptación y revisión de exposición residual sustentados en evidencia.
- El personal debe conocer sus obligaciones y reportar incidentes y desviaciones. La política debe estar disponible como información documentada, comunicarse internamente y facilitarse a partes interesadas cuando corresponda.
- La dirección debe promover la mejora continua del SGSI, revisar objetivos, desempeño y necesidades de recursos.
Evidencias: proyecto de acta del Anexo A, alcance, objetivos OBJ01–OBJ07, registros de comunicación y revisión directiva (REG-03/08). Riesgos: transversal. Controles: G01/G02.

## POL02 — Identidades y accesos

Propietario: Seguridad / IAM; TI y Operaciones ejecutan según función.
Finalidad: limitar el acceso a sujetos, cuentas, acciones y recursos autorizados.
- Las identidades de clientes, personal y servicios técnicos deben distinguirse; prohibir el uso compartido de credenciales personales.
- La autenticación debe aplicar MFA conforme a los flujos aprobados y verificación reforzada cuando el riesgo de la operación lo requiera. Vincular la verificación requerida a la orden correspondiente; no tratar una señal sintética como MFA real.
- Aplicar mínimo privilegio, segregación de funciones, acceso temporal cuando proceda y revocación al finalizar la autorización. Revisar permisos al cambiar funciones y periódicamente según criticidad.
- Validar sesión y autorización por recurso en servidor, con restricciones adicionales en el adaptador. No confiar exclusivamente en controles de interfaz.
- Inventariar identidades técnicas; custodiar secretos en mecanismos autorizados, limitar permisos, revisar vigencia y rotar/revocar conforme a la política y al evento.
Evidencias: altas, cambios, bajas, revisiones, decisiones y excepciones IAM; pruebas LAB02/LAB03 reportadas; aceptación integrada pendiente. Riesgos: R01/R02/R07/R08. Controles: C01/C02/C08. Indicadores: IND01/02/07.

## POL03 — Integridad de transacciones

Propietario: Operaciones Digitales; ejecución técnica: Desarrollo e Integraciones.
Finalidad: asegurar que consultas y transferencias correspondan a cuentas autorizadas y estados verificables.
- P01 debe verificar titularidad o permiso sobre la cuenta y presentar saldos vigentes; no mostrar un saldo obsoleto como confirmado.
- P02 debe validar cuenta de origen, destino interno, autorización, monto y reglas aplicables en servidor. No confirmar operaciones rechazadas ni inciertas.
- Mantener referencia persistente y única por orden conforme al diseño de idempotencia; los reintentos no deben crear débitos adicionales. Rechazar reutilización incompatible de la referencia.
- Ante incertidumbre, impedir el reproceso hasta consultar el estado y conciliar los asientos. Operaciones debe documentar el cierre y autorizar la reapertura funcional con evidencia.
- Proteger la durabilidad de asientos confirmados; el objetivo de recuperación de P02 es RPO cero para esos asientos.
Evidencias: casos de autorización, concurrencia, reenvío, conflicto de referencia y conciliación; LAB03–LAB05/LAB07–LAB08 reportadas con alcance local. Riesgos: R02/R03/R08. Controles: C01/C02/C05. Indicadores: IND01/02/03/04d.

## POL04 — Protección de datos y dispositivos

Propietario: Seguridad / TI; propietarios de información validan clasificación y acceso.
Finalidad: evitar exposición no autorizada de datos y recursos de soporte.
- Clasificar información del alcance, limitar su acceso y exportación a necesidades autorizadas, y aplicar cifrado en tránsito y almacenamiento según criticidad y diseño.
- Separar datos de operación y de prueba; emplear datos sintéticos en el laboratorio académico. No incluir credenciales, tokens ni información financiera real en repositorios o evidencias compartidas.
- Exigir configuración segura, bloqueo, cifrado, postura y protección de endpoint de equipos corporativos que accedan a recursos de soporte, según compatibilidad y riesgo. Aplicar MDM y DLP donde corresponda.
- En dispositivos personales de clientes, proteger sesiones, datos y comunicaciones mediante controles del canal; no exigir inscripción en el MDM corporativo por defecto.
- Aplicar conservación y disposición autorizadas conforme a clasificación y obligaciones verificadas por Cumplimiento.
Evidencias: inventario y clasificación, configuración de cifrado, políticas de postura y DLP, decisiones de acceso y pruebas en plataformas compatibles. Riesgos: R06/R07 y exposición de información asociada a R02. Controles: C02/C06/C08. Indicadores: IND01/06/07. Implementación integrada pendiente.

## POL05 — Registros e incidentes

Propietario: Oficial de Seguridad / SOC; Operaciones atiende inconformidades y estados transaccionales.
Finalidad: preservar trazabilidad, detección y respuesta.
- Registrar eventos relevantes de identidad, API y core con marcas temporales coherentes, referencia, decisión y datos mínimos necesarios. Excluir contraseñas, tokens y otros secretos de los registros.
- Proteger bitácoras contra modificación, eliminación y acceso no autorizado; definir conservación, acceso y custodia de evidencia.
- Clasificar alertas e incidentes según impacto, correlacionar registros, notificar a las áreas facultadas, contener y documentar recuperación y cierre.
- Ante transacción incierta o sospecha de fraude, coordinar con Operaciones, preservar evidencia y no confirmar/reprocesar sin las verificaciones de POL03.
- Cumplimiento determina obligaciones de notificación; no se inventan plazos legales. Las comunicaciones externas requieren autoridad y constancia.
Evidencias: LAB06 reportada (regla local), tickets, eventos correlacionados, registros de incidentes y tiempos de respuesta; integración SIEM/XDR pendiente. Riesgos: R05/R08. Controles: C04. Indicadores: IND05/09.

## POL06 — Cambios y vulnerabilidades

Propietario: TI; Seguridad revisa riesgos; Operaciones valida impacto funcional.
Finalidad: prevenir cambios no autorizados y reducir exposición en los recursos de P01/P02.
- Separar ambientes, mantener configuraciones de referencia y control de versiones. Restringir cambios según función y autorización.
- Registrar solicitud, motivo, impacto en activos/riesgos/continuidad, aprobación, pruebas de seguridad y regresión, plan de reversión y resultado.
- Evaluar vulnerabilidades y actualizaciones según exposición, criticidad, riesgo y obligaciones; registrar prioridad, plazo, responsable y verificación del tratamiento. No imponer plazos arbitrarios que contradigan el plan vigente.
- Aplicar cambios de emergencia bajo autorización y registro, con revisión posterior. No exceptuar requisitos esenciales de integridad y autorización.
- Gestionar certificados, claves y secretos según POL02/POL04; verificar configuraciones y rutas tras cambios.
Evidencias: solicitudes, diferencias de configuración/código, pruebas de regresión, hallazgos y revalidación. Riesgos: R01–R08 según impacto del cambio; controles: C01–C08 según activo afectado. Indicador transversal: IND08; indicadores funcionales según cambio.

## POL07 — Proveedores y continuidad

Propietario: TI / Continuidad; Operaciones es propietaria funcional de la recuperación; Riesgos y Cumplimiento revisan dependencias y obligaciones.
Finalidad: mantener disponibilidad y recuperación verificable de P01/P02.
- Identificar servicios de terceros, criticidad, dependencias, responsabilidades compartidas, requisitos de seguridad, SLA, evidencia, continuidad y condiciones de salida antes de contratación y durante su revisión.
- Mantener rutas autorizadas, segmentación y cifrado de la conectividad híbrida; evitar dependencias compartidas no evaluadas en los caminos de recuperación.
- Proteger respaldos y verificar restauración, conmutación, conciliación y capacidad mínima de servicio conforme al BIA. P01: RTO 120 min, RPO 5 min para datos de consulta. P02: RTO 60 min, RPO cero para asientos confirmados. Mantener MTPD y demás condiciones del BIA original.
- Autorizar reapertura funcional únicamente tras verificar acceso, estado, integridad y conciliación; evitar confirmaciones dobles durante fallas y recuperación.
- Revisar infraestructura de centro de datos que soporte P01/P02 (energía, telecomunicaciones, ambiente, protección física y sitio alterno). No declarar certificación TIA-942 ni despliegue Azure sin evidencia.
Evidencias: expediente de proveedor, configuración y dependencias, ejercicios LAB07/LAB08 reportados en prototipo, pruebas representativas y registro de reapertura. Riesgos: R03/R04. Controles: C03/C05/C07. Indicadores: IND04/08.

## Registro propuesto de excepciones y cumplimiento

| ID excepción | Política/disposición | Proceso/activo/riesgo | Justificación e impacto | Medida compensatoria | Propietario | Autoridad y decisión | Inicio/vencimiento | Revisión/evidencia |
|---|---|---|---|---|---|---|---|---|
| EXC__ | | | | | | Pendiente | | |

| ID revisión | Política/disposición | Criterio | Evidencia y entorno | Resultado | Responsable | Acción y plazo |
|---|---|---|---|---|---|---|
| REV__ | | | | No evaluado | | |

Las plantillas no acreditan excepciones autorizadas ni cumplimiento. Remitir hallazgos a REG-09 y aceptación residual a los criterios de 01-objetivos-roles-aceptacion.md.

## Integración y verificación

Sustituir o ampliar la tabla de 4.8 con una síntesis de POL01–POL07; conservar el programa de concientización, enlazar requisitos de apoyo (02/03), objetivos y roles (01) y evaluación (04/05). Mantener las políticas completas en un anexo o expediente documental controlado, sin duplicarlas en el informe. Actualizar el Anexo A para referenciar las políticas propuestas, sin simular su aprobación. La relación con controles es de grupos C01–C08/G01/G02, no una reevaluación de las 93 referencias de la SoA: revisar correspondencia detallada con el Anexo B cuando esté disponible. No modificar BIA, puntuaciones, alcance ni evidencias originales. Cierre: revisión de coherencia y aprobación del equipo antes de integrar en main.
