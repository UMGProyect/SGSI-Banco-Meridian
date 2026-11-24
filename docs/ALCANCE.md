# Delimitación del SGSI

Estado: propuesta documental para revisión, basada en el informe v.2 y la decisión del equipo de reducir el alcance.

## Alcance funcional obligatorio
El SGSI comprende exclusivamente los servicios de banca web y móvil de Banco Meridian, S. A., necesarios para:
- P01: consulta de saldos de cuentas autorizadas.
- P02: transferencias entre cuentas del mismo banco, incluyendo validación, registro, consulta de estado y conciliación.

## Límites y dependencias
Se incluyen portal, aplicación móvil, identidad, API, conectividad híbrida Azure/local, adaptador, funciones delimitadas del core, datos, bitácoras, monitoreo, equipos de soporte y recuperación únicamente en cuanto soporten P01/P02. Los controles MDM/DLP/EDR/XDR, gobierno, continuidad y Data Center se aplican a estos recursos y sus dependencias, no a toda la institución. Los dispositivos de clientes no se presuponen administrados por el banco.

## Exclusiones
Tarjetas, cajeros automáticos, créditos, transferencias interbancarias, operaciones de agencias y demás servicios del core. Las interfaces compartidas se consideran por su impacto sobre P01/P02; excluir un proceso no implica excluir automáticamente sus dependencias críticas.

## Control de cambios
No ampliar el alcance funcional para cubrir requisitos del curso. Relacionar cada nuevo activo, riesgo, control y prueba con P01/P02 o una dependencia necesaria. Cualquier ampliación requiere justificación y aprobación del equipo. Mantener identificadores existentes y distinguir diseño, simulación y evidencia observada.
