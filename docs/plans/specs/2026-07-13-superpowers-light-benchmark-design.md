# Diseño del benchmark ligero y robusto de Superpowers

**Fecha:** 2026-07-13

**Estado:** Diseño aprobado para revisión escrita

**Objetivo:** Comprobar con un coste moderado si las Superpowers más aplicables al trabajo diario mejoran a Codex frente a su forma de trabajo base.

## Decisión de alcance

El benchmark completo de 72 ejecuciones se sustituye por una prueba ligera robusta de 16 ejecuciones. La prueba cubre el ciclo de desarrollo completo, con énfasis en revisión de código y coordinación multiagente.

Se evaluarán estas siete skills:

- `brainstorming`
- `writing-plans`
- `systematic-debugging`
- `test-driven-development`
- `verification-before-completion`
- `dispatching-parallel-agents`
- `subagent-driven-development`

Las otras seis adaptaciones de Obra Superpowers quedan fuera de esta primera prueba. No se retirará ni modificará ninguna skill como parte del benchmark.

## Configuraciones comparadas

### B0: Codex base

- No contiene ninguna de las 13 Superpowers.
- Conserva las mismas skills de dominio, herramientas, permisos y límites que la configuración experimental.

### S1: Superpowers seleccionadas

- Contiene únicamente las siete skills listadas arriba.
- No contiene las otras seis Superpowers, para que no influyan accidentalmente.

Ambas configuraciones utilizarán:

- Modelo `gpt-5.6-sol`.
- Razonamiento `medium`.
- El mismo prompt y contexto inicial.
- El mismo commit y worktree limpio.
- El mismo límite de tiempo.
- Un máximo total de cuatro agentes activos.
- Acceso idéntico a herramientas, red y skills no pertenecientes a Superpowers.

La tarea multiagente autorizará explícitamente el uso de subagentes en ambas configuraciones. Así se medirá si las skills mejoran la coordinación, no el simple acceso a la herramienta.

## Matriz de ejecución

Se usarán cuatro tareas y cada combinación se repetirá dos veces desde sesiones y worktrees nuevos.

| Tarea | B0 | S1 | Total |
| --- | ---: | ---: | ---: |
| Diseño y planificación ambigua | 2 | 2 | 4 |
| Diagnóstico y corrección de un bug | 2 | 2 | 4 |
| Auditoría de código | 2 | 2 | 4 |
| Auditoría amplia paralelizable | 2 | 2 | 4 |
| **Total** | **8** | **8** | **16** |

Las ejecuciones se intercalarán en orden aleatorio. Ninguna ejecución podrá leer resultados anteriores, la respuesta de la otra configuración ni los criterios ocultos de evaluación.

## Selección de tareas

Antes de ejecutar se congelarán cuatro tareas reales o fixtures realistas:

1. **Diseño y planificación:** petición deliberadamente ambigua con requisitos verificables y al menos dos decisiones de arquitectura.
2. **Bug:** fallo reproducible con test inicial y causa que exija inspeccionar más de un archivo.
3. **Auditoría:** snapshot con hallazgos conocidos de severidad distinta y al menos un posible falso positivo.
4. **Auditoría paralelizable:** repositorio o cambio con tres áreas independientes que puedan revisarse concurrentemente.

Cada tarea tendrá un commit inmutable, prompt congelado, comando de preparación, comando de verificación y rúbrica oculta. No se usarán errores de sintaxis triviales ni prompts que nombren las skills.

## Evaluación

La calidad será el resultado principal y se puntuará de 0 a 100. Tiempo, tokens y uso de agentes se reportarán por separado.

### Diseño y planificación

- Cobertura de requisitos y restricciones: 35 puntos.
- Decisiones técnicas justificadas: 20 puntos.
- Pasos ejecutables y verificables: 25 puntos.
- Riesgos, dependencias y orden: 15 puntos.
- Claridad: 5 puntos.

### Diagnóstico y corrección

- Tests y criterios de aceptación: 45 puntos.
- Causa raíz y corrección conductual: 20 puntos.
- Ausencia de regresiones y cambios ajenos: 15 puntos.
- Evidencia de verificación: 15 puntos.
- Claridad de entrega: 5 puntos.

### Auditoría de código

- Recall ponderado de hallazgos conocidos: 40 puntos.
- Precisión y ausencia de falsos positivos: 25 puntos.
- Severidad y priorización: 10 puntos.
- Evidencia y remediación accionable: 20 puntos.
- Claridad: 5 puntos.

### Auditoría paralelizable

- Calidad y cobertura de hallazgos: 55 puntos.
- Precisión: 15 puntos.
- División independiente del trabajo: 10 puntos.
- Integración, deduplicación y priorización: 15 puntos.
- Claridad: 5 puntos.

Una regresión crítica, una afirmación falsa de haber ejecutado verificaciones, un cambio destructivo fuera de alcance o la ausencia del entregable limitará el score a un máximo de 49.

## Coste y comportamiento

Por ejecución se capturará:

- Tiempo total.
- Tokens totales disponibles en la telemetría.
- Número de llamadas a herramientas y fallos de herramientas.
- Número de subagentes.
- Tiempo agregado de agentes cuando esté disponible.
- Cantidad de solicitudes de aclaración al usuario.

La latencia y el cómputo agregado se mostrarán por separado para que el paralelismo no parezca gratuito.

## Comparación y reglas de decisión

Los resultados se evaluarán de forma ciega con etiquetas opacas. Para cada tarea se comparará el promedio de las dos repeticiones de S1 contra B0.

- **Conservar el paquete seleccionado:** mejora media de al menos 4 puntos, o reducción de fallos críticos, sin un aumento desproporcionado del coste.
- **Mantener sólo en categorías concretas:** mejora de al menos 5 puntos en una tarea y ausencia de beneficio consistente en las demás.
- **Considerar desactivación por defecto:** diferencia de calidad menor de 4 puntos y aumento de al menos 15% en tiempo o tokens.
- **Considerar simplificación o retirada:** S1 obtiene peor calidad media o introduce más fallos críticos.
- **Inconcluso:** las dos repeticiones de una tarea producen conclusiones opuestas o la diferencia depende de un único resultado extremo.

No se harán ejecuciones de desempate automáticamente. El estado inconcluso se informará como tal.

## Límite de inferencia

Esta prueba mide principalmente el valor del paquete de siete skills y de sus familias por tipo de tarea. Con 16 ejecuciones no puede atribuir causalmente una diferencia a cada skill individual.

Los rastros de activación permitirán identificar:

- Skills que se activaron y parecieron intervenir en el resultado.
- Skills que añadieron pasos o coste sin evidencia visible de beneficio.
- Skills que nunca se activaron y, por tanto, quedan como no evaluadas.

Una skill individual podrá quedar como candidata a retirar, pero no se desinstalará únicamente por esta prueba.

## Entregables

- Tabla de los 16 resultados.
- Comparación de calidad, tiempo, tokens y agentes entre B0 y S1.
- Comparación por las cuatro categorías.
- Ejemplos ciegos de las respuestas producidas.
- Clasificación de cada skill: conservar, condicional, candidata a simplificar, candidata a retirar o no evaluada.
- Recomendación final del conjunto mínimo de Superpowers que merece una prueba posterior o uso habitual.

## Criterio de finalización

La prueba termina después de las 16 ejecuciones y su evaluación ciega. El informe no ejecutará sincronización, poda ni eliminación de skills. Cualquier cambio posterior requerirá aprobación explícita del usuario.
