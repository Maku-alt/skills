# Skills Dictionary

- `last_registry_refresh`: `2026-06-09`
- `active_skills`: `25`
- `reference_skills`: `3`

## Active skills

| Skill | Last updated | Tags | Description |
| --- | --- | --- | --- |
| `brainstorming` | `2026-01-09` | `skills` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| `data-analysis` | `2026-01-09` | `analytics` | Structured workflow for exploring tabular datasets (CSV/Parquet) with pandas, producing descriptive stats, charts, and action items. Invoke when Agent must inspect a dataset, summarize patterns, or prepare quick visuals for stakeholders. |
| `doc-coauthoring` | `2026-01-09` | `documents` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks. |
| `docx` | `2026-01-09` | `documents` | Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Agent needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks |
| `frontend-slides` | `2026-06-09` | `documents` | Use when the user wants a presentation as HTML slides, a web-first talk deck, or a PPTX-to-HTML conversion with strong visual design and minimal runtime dependencies. |
| `internal-comms` | `2026-01-09` | `documents` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Agent should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.). |
| `jupyter-notebook` | `2026-03-04` | `analytics` | Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for experiments, explorations, or tutorials; prefer the bundled templates and run the helper script `new_notebook.py` to generate a clean starting notebook. |
| `mcp-builder` | `2026-01-09` | `automation` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| `pandas-optimizer` | `2026-01-09` | `analytics` | Optimiza el uso de memoria de DataFrames de pandas. Usar cuando el agente trabaje con datasets grandes y necesite reducir el consumo de memoria convirtiendo columnas numéricas a tipos más eficientes (int8, int16, float32, etc.). |
| `pdf` | `2026-01-09` | `documents` | Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Agent needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale. |
| `pptx` | `2026-01-09` | `documents` | Presentation creation, editing, and analysis. When Agent needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks |
| `receiving-code-review` | `2026-01-09` | `delivery` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| `requesting-code-review` | `2026-01-09` | `delivery` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `skill-creator` | `2026-01-09` | `skills` | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Agent's capabilities with specialized knowledge, workflows, or tool integrations. |
| `subagent-driven-development` | `2026-01-09` | `delivery` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | `2026-01-09` | `delivery` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `teradata-debug-sp` | `2026-01-09` | `analytics` | Genera Store Procedures de Teradata con infraestructura de debug y manejo de errores. Usar cuando el agente necesite transformar queries SQL en procedimientos almacenados de producción con: (1) Tablas de debug y error, (2) Logging automático antes de cada CREATE TABLE, (3) Manejo de excepciones SQL, (4) Nomenclatura estándar SAM. |
| `test-driven-development` | `2026-01-09` | `delivery` | Use when implementing any feature or bugfix, before writing implementation code |
| `theme-factory` | `2026-01-09` | `documents` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly. |
| `using-git-worktrees` | `2026-01-09` | `delivery` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification |
| `verification-before-completion` | `2026-01-09` | `delivery` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| `webapp-testing` | `2026-01-09` | `testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. |
| `writing-plans` | `2026-01-09` | `delivery` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | `2026-01-09` | `skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |
| `xlsx` | `2026-01-09` | `analytics` | Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Agent needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas |

## External references

| Skill | Last updated | Note |
| --- | --- | --- |
| `analyzing-financial-statements` | `2026-01-14` | Imported as external reference from claude-cookbooks. |
| `applying-brand-guidelines` | `2026-01-09` | Imported as external reference from claude-cookbooks. |
| `creating-financial-models` | `2026-01-09` | Imported as external reference from claude-cookbooks. |
