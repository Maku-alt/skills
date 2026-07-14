# Benchmark ligero de Superpowers

**Estado:** completo — 16/16 ejecuciones válidas, `gpt-5.6-sol`, esfuerzo `medium`.

Se comparó B0 (sin las 13 skills de Superpowers instaladas) contra S1 (solo las siete skills más relevantes): `brainstorming`, `writing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `dispatching-parallel-agents` y `subagent-driven-development`. Cada una de cuatro tareas se ejecutó dos veces por configuración, en orden aleatorio y con prompts idénticos.

## Resultado global

| Configuración | Corridas | Calidad automática | Calidad ciega /10 | Tiempo medio | Tokens medios |
| --- | ---: | ---: | ---: | ---: | ---: |
| B0, sin skills | 8 | 81.640 | 8.713 | 73.631 s | 180,386 |
| S1, con skills | 8 | 61.406 | 7.163 | 98.281 s | 265,820 |

S1 perdió 20.234 puntos de calidad automática y 1.55 puntos sobre 10 en la revisión ciega global. Además usó 33.5% más tiempo y 47.4% más tokens. Por tanto, **no conviene mantener este paquete activado por defecto para todo trabajo de código**.

## Resultado por tipo de tarea

| Tarea | Calidad automática B0 → S1 | Revisión ciega | Tiempo B0 → S1 | Tokens B0 → S1 | Lectura práctica |
| --- | ---: | --- | ---: | ---: | --- |
| Planificación | 85.935 → 88.125 | S1 gana 2/2; 8.40 → 9.35 | 151.546 → 164.882 s | 336,511 → 266,176 | Mejora material de calidad con menos tokens; coste moderado de tiempo. |
| Bugfix estrecho | 85.000 → 5.000 | B0 gana 2/2; 8.50 → 1.25 | 28.938 → 35.242 s | 121,246 → 129,692 | S1 pidió confirmación en ambas corridas y no implementó; B0 corrigió y pasó tests públicos y ocultos. |
| Auditoría simple | 55.625 → 52.500 | Empate 1–1; 8.70 → 8.95 | 37.734 → 37.070 s | 93,702 → 124,584 | Diferencia de calidad pequeña e inestable; S1 gastó 33% más tokens. |
| Auditoría paralela | 100.000 → 100.000 | Empate 1–1; 9.25 → 9.10 | 76.305 → 155.930 s | 170,087 → 542,830 | Sin ganancia de calidad; 104% más tiempo y 219% más tokens. |

## Decisión recomendada

- **Conservar `writing-plans` para planes complejos.** Es el único caso con ganancia consistente: ganó las dos comparaciones ciegas y redujo tokens, aunque aumentó algo el tiempo.
- **Restringir `brainstorming` a trabajo realmente ambiguo o creativo.** No debe bloquear una orden explícita y estrecha de implementación. Su requisito de pedir aprobación causó 0/2 entregas en bugfix, mientras B0 completó 2/2.
- **No activar automáticamente el flujo multiagente en auditorías pequeñas.** Reservar `dispatching-parallel-agents`/`subagent-driven-development` para repositorios o investigaciones suficientemente grandes; en este fixture no mejoró calidad y multiplicó el coste.
- **No retirar todavía `systematic-debugging`, `test-driven-development` ni `verification-before-completion`.** La puerta de confirmación ocurrió antes de que pudieran demostrar su valor. Esta prueba no identifica su efecto causal por separado.
- **Para auditorías de código, usar el método nativo o una skill específica de review/security.** Las Superpowers generales no aportaron una mejora reproducible en la auditoría simple.

En términos operativos: **retira el paquete como comportamiento universal, no las skills del disco**. Mantén selección contextual: planificación sí; brainstorming solo ante ambigüedad; multiagente solo con escala suficiente; bugfix explícito debe continuar sin una nueva ronda de aprobación.

## Validez y límites

- La prueba es ligera: dos repeticiones y un fixture pequeño. Sirve para decidir defaults, no para estimar una ventaja universal con precisión estadística.
- Se evaluó un paquete, por lo que no se puede atribuir causalmente cada diferencia a todas las skills incluidas.
- La calidad automática se contrastó con comparación ciega por pares. Los evaluadores no conocían qué candidato era B0 o S1.
- Las primeras corridas de bugfix estuvieron afectadas por una política de solo lectura del CLI y fueron reemplazadas simétricamente. Las cuatro corridas válidas usaron clones desechables con permisos de automatización; B0 produjo cambios y S1 se detuvo por su flujo de aprobación.
- Los diffs B0 de bugfix incluyeron artefactos `__pycache__`, penalizados en la revisión ciega. Aun con esa penalización, ganaron ampliamente.
