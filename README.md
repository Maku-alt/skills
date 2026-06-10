# Skills Registry

Repositorio canónico y curado para centralizar y mantener skills entre distintas máquinas y proyectos.

## Objetivo

- Tener un solo origen de verdad para skills reutilizables.
- Mantener el set activo directamente dentro de este repo.
- Archivar lo que ya no forma parte del working set.
- Registrar referencias externas sin convertirlas en estándar interno.

## Estructura

- `skills/`: skills activos y recomendados.
- `archive/`: skills internos archivados, no recomendados por defecto.
- `references/`: skills externos conservados solo como referencia.
- `catalog/skills-index.json`: índice maestro con estado, fecha de actualización y hash técnico.
- `catalog/skills-dictionary.md`: diccionario legible de skills.
- `catalog/active-skills.md`: set activo actual.
- `catalog/archived-skills.md`: skills retirados del set activo.
- `catalog/project-recommendations.md`: skills recomendados por repo detectado.
- `docs/skill-authoring-guide.md`: cómo debe escribirse un skill en este repo.
- `docs/skill-intake-checklist.md`: qué validar antes de aceptar un skill.
- `docs/versioning.md`: política de metadatos basada en `last_updated`.
- `templates/skill-template/`: plantilla base para skills nuevos.
- `config/curation-policy.json`: política de curación activa/archivada.
- `scripts/build_registry.py`: regenera el catálogo a partir de este repo.

## Estado actual

- `context-base` y `context-analitica-avanzada` ya no se consideran repos canónicos.
- Este repo pasa a ser el lugar de mantenimiento.
- Los skills que vinieron de repos anteriores ya fueron importados y ahora deben editarse aquí.

## Uso

```powershell
python scripts/build_registry.py
```

El script:

1. Lee `skills/`, `archive/` y `references/`.
2. Regenera el índice y el diccionario.
3. Genera recomendaciones por repo y reportes de curación.

## Criterio de curación

- `skills/`: skills activos que sí quieres usar y mantener.
- `archive/`: skills que no están en uso o no merecen estar en el set por defecto.
- `references/`: ejemplos externos para aprendizaje o futura adaptación.
