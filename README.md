# Skills

Repositorio fuente de verdad para las skills personales que se instalan en Codex.

## Para Que Sirve

- Mantener una base curada y versionada de skills reutilizables.
- Llevar el mismo set de skills entre PCs sin depender de rutas locales.
- Actualizar skills desde fuentes externas de forma controlada.
- Sincronizar el set curado hacia `~/.codex/skills` mediante mirror.

## Modelo De Trabajo

`repos/skills` es la fuente versionada. `~/.codex/skills` es la copia runtime que Codex lee.

El flujo recomendado es:

1. Actualizar o editar en este repo.
2. Validar estructura, rutas, scripts y compatibilidad Codex.
3. Revisar el impacto con `.\sync-to-codex.ps1 -WhatIf`.
4. Ejecutar el sync real solo cuando la poda esperada sea correcta.

No edites `~/.codex/skills` como fuente permanente. Si haces un cambio ahi para probar, traelo de vuelta a este repo antes de conservarlo.

## Que Se Versiona

- `skills/`: skills activos y listos para instalar en Codex.
- `catalog/skills-dictionary.md`: catalogo resumido del set curado.
- `sync-to-codex.ps1`: script de mirror hacia la carpeta runtime de Codex.

Tambien se versionan carpetas internas necesarias para que una skill funcione, como `scripts/`, `references/`, `assets/` y `eval-viewer/` dentro de cada skill.

## Fuentes Upstream

Algunas skills se mantienen como adaptaciones de fuentes externas:

- Anthropic Skills: `pptx`, `docx`, `xlsx`, `pdf`, `frontend-design`, `skill-creator`, `mcp-builder`, `theme-factory`, `webapp-testing`, `doc-coauthoring`, `internal-comms`.
- Impeccable: `impeccable`, instalado con la CLI oficial desde `pbakaus/impeccable` y conservado como build especifico para Codex. La version incorporada es `4.0.2` y se distribuye bajo Apache-2.0.
- Obra Superpowers: retirada del set activo y conservada en `archive/` tras el benchmark ligero de julio de 2026. Consulta `benchmarks/superpowers-light/results/report.md`.
- Skills locales o propias: analytics, Teradata y otras utilidades especificas del entorno.

Cuando se actualiza desde upstream, adapta el lenguaje a Codex antes de sincronizar:

- usar nombres de skills disponibles en este repo, sin prefijos externos innecesarios;
- evitar instrucciones especificas de Claude cuando no apliquen;
- mantener rutas reales de la version instalada;
- validar que los scripts referenciados existan.

Para refrescar Impeccable, instala primero el build global oficial de Codex y luego importa `~/.agents/skills/impeccable` sobre `skills/impeccable`:

```powershell
npx --yes impeccable@latest install -y --providers=codex --scope=global --no-hooks
```

## Sincronizar Con Codex

Vista previa:

```powershell
.\sync-to-codex.ps1 -WhatIf
```

Aplicar mirror:

```powershell
.\sync-to-codex.ps1
```

El destino se resuelve en este orden:

1. parametro `-CodexSkillsPath`;
2. variable `CODEX_HOME\skills`;
3. default `$env:USERPROFILE\.codex\skills`.

Por defecto el script:

- reemplaza en Codex cada skill presente en este repo;
- instala las skills que esten en repo y falten en Codex;
- elimina de Codex las skills que no esten en `skills/`;
- preserva siempre `.system`;
- copia este `README.md` como `README.md` dentro de `~/.codex/skills`.

Para copiar sin borrar extras del destino:

```powershell
.\sync-to-codex.ps1 -NoPrune
```

## Validacion Antes Del Sync

Antes de desplegar:

```powershell
python .\skills\skill-creator\scripts\quick_validate.py .\skills\pptx
python -m compileall -q .\skills\pptx\scripts .\skills\docx\scripts .\skills\xlsx\scripts .\skills\pdf\scripts
git diff --check
.\sync-to-codex.ps1 -WhatIf
```

Para cambios amplios, valida todas las skills tocadas con `quick_validate.py`.

## Diccionario Rapido

El catalogo completo esta en `catalog/skills-dictionary.md`.

| Skill | Categoria | Uso principal |
| --- | --- | --- |
| `pptx` | `documents` | Crear, editar, inspeccionar y renderizar presentaciones PowerPoint. |
| `docx` | `documents` | Crear, editar o revisar documentos Word. |
| `xlsx` | `analytics` | Crear, editar o analizar archivos Excel. |
| `pdf` | `documents` | Extraer, completar o generar PDFs. |
| `frontend-design` | `design` | Guiar interfaces web con alto criterio visual. |
| `impeccable` | `design` | Disenar, auditar y pulir interfaces frontend con flujos especializados y deteccion de antipatrones. |
| `skill-creator` | `skills` | Crear, probar y empaquetar skills nuevas o existentes. |
| `travel-advisor` | `travel` | Auditar expedientes de viaje y coordinar investigacion especializada sin ejecutar compras. |

## Nota

Este repo no busca publicar todas las skills posibles. La intencion es conservar un set curado: lo que no este aqui sera podado de `~/.codex/skills` cuando se ejecute el mirror por defecto.
