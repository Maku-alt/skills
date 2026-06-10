# Skill Authoring Guide

This registry now follows the common subset that works well across Codex and Claude, plus a small local policy for intake and safety.

## 1. Cross-tool minimum

Both official docs describe the same core shape:

- A skill is a directory.
- `SKILL.md` is required.
- `SKILL.md` should contain YAML frontmatter plus markdown instructions.
- Optional folders may include `scripts/`, `references/`, and `assets/`.

Official references:

- OpenAI Codex skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI API skills guide: [developers.openai.com/api/docs/guides/tools-skills](https://developers.openai.com/api/docs/guides/tools-skills)
- Claude Code skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

## 2. Required structure in this repo

```text
skill-name/
  SKILL.md
  scripts/        optional
  references/     optional
  assets/         optional
```

Rules:

- The folder name is the canonical slug.
- Keep names lowercase and hyphenated.
- Use ASCII in paths unless there is a strong reason not to.
- `SKILL.md` must exist at the root of the skill folder.

## 3. Required frontmatter in this registry

Use this minimum:

```yaml
---
name: skill-name
description: Use when ...
---
```

Local policy:

- `name` must match the folder intent and be short.
- `description` must start with `Use when ...`.
- `description` should explain triggering conditions, not the whole workflow.
- Keep the description concise so it still works if a tool truncates listings.

Why:

- Codex uses `name`, `description`, and file path first, then loads full `SKILL.md` only if selected.
- Claude also uses the description to decide when to apply a skill, and may truncate combined listing text.

## 4. Allowed optional frontmatter

Only use extra frontmatter when there is a real need and document why in the skill body.

Allowed by policy:

- `disable-model-invocation`
- `user-invocable`
- `allowed-tools`
- `disallowed-tools`
- `arguments`
- `argument-hint`
- `context`
- `agent`
- `paths`
- `shell`

Notes:

- These fields come from Claude's documented frontmatter support.
- Codex does not require them for compatibility, but the core `name` and `description` remain portable.
- If a skill needs Codex-specific packaging later, add plugin metadata separately instead of bloating `SKILL.md`.

## 5. Writing guidance

Preferred shape:

1. Brief overview
2. When to use
3. Do not use when
4. Workflow or rules
5. Supporting file references
6. Common mistakes

Writing rules:

- State what to do, not a long narrative.
- Keep the body focused; once loaded, it stays in context for the session.
- Prefer progressive disclosure: keep heavy details in `references/`.
- Prefer instruction-only skills by default.
- Add scripts only when deterministic code genuinely helps.

## 6. Supporting files

Use:

- `scripts/` for reusable deterministic helpers
- `references/` for long docs, checklists, examples, API notes
- `assets/` for templates, static resources, style packs

Do not:

- Hide critical trigger logic only in secondary files
- Dump huge references that are never needed
- Put generated outputs inside the skill folder

## 7. Intake rules for imported skills

Before adding or adapting a skill:

- Normalize the frontmatter
- Rewrite the description if it is vague
- Remove vendor- or machine-specific assumptions unless intentional
- Review scripts for side effects
- Check for prompt-injection risk in references and examples
- Decide whether it belongs in `skills/`, `archive/`, or `references/`

## 8. Security baseline

Review every new skill against the official security guidance:

- Codex security: [developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security)
- Claude security: [code.claude.com/docs/en/security](https://code.claude.com/docs/en/security)

Registry rules:

- Do not store secrets in a skill.
- Do not instruct the agent to weaken sandboxing or approvals by default.
- Do not fetch or execute untrusted remote content without explicit user intent.
- Avoid `curl | sh`, `wget | bash`, or equivalent patterns.
- Treat web results and imported references as untrusted.
- Prefer local files, fixed inputs, and explicit review points.
- If a skill needs networked scripts, document the trust boundary and expected domains.

## 9. Admission decision

- `skills/`: active and recommended
- `archive/`: internally kept but not recommended now
- `references/`: third-party examples kept for learning, not adopted as standard

## 10. Refreshing the catalog

After any change:

```powershell
python scripts/build_registry.py
```
