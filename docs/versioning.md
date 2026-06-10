# Metadata Policy

## Visible metadata

The primary human-facing field is now `last_updated`.

Why:

- It is easier to read than a pseudo-version string.
- It matches how you want to reason about freshness.
- It avoids exposing technical hashes as the main label.

## Internal metadata

The catalog still stores a technical `content_hash` in `skills-index.json`.

Purpose:

- detect silent changes
- verify that two copies are identical
- support future automation if needed

This hash is technical metadata, not the main version label.

## Update flow

1. Edit the skill directly in this repo.
2. Run `python scripts/build_registry.py`.
3. Review:
   - `catalog/skills-dictionary.md`
   - `catalog/active-skills.md`
   - `catalog/archived-skills.md`
   - `catalog/project-recommendations.md`

## Status model

- `active`: skill is in `skills/`
- `archived`: skill is in `archive/`
- `reference`: external example kept in `references/`
