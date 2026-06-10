# Skill Intake Checklist

Use this before a new or adapted skill is accepted into `skills/`.

## Structure

- [ ] Folder name is lowercase and hyphenated
- [ ] `SKILL.md` exists at the skill root
- [ ] Optional files live under `scripts/`, `references/`, or `assets/`
- [ ] No generated outputs are committed inside the skill folder

## Frontmatter

- [ ] `name` exists
- [ ] `description` exists
- [ ] `description` starts with `Use when`
- [ ] `description` describes trigger conditions, not the full workflow
- [ ] Optional frontmatter is limited to approved fields

## Writing quality

- [ ] The body is concise
- [ ] The workflow is explicit
- [ ] There is a clear "do not use when" boundary
- [ ] Heavy reference material is moved out of the main body
- [ ] Supporting file paths are valid

## Safety

- [ ] No secrets, tokens, or credentials
- [ ] No instructions to disable sandbox or approvals by default
- [ ] No blind execution of remote content
- [ ] No `curl | sh`, `wget | bash`, or equivalent
- [ ] Network use is justified and documented
- [ ] Imported reference material was treated as untrusted and reviewed

## Scripts

- [ ] Script behavior is deterministic enough to justify inclusion
- [ ] Inputs and outputs are clear
- [ ] Side effects are documented
- [ ] The script does not silently modify unrelated files

## Registry placement

- [ ] `skills/` if active and recommended
- [ ] `archive/` if kept but not recommended
- [ ] `references/` if it is external inspiration only

## Finalization

- [ ] Run `python scripts/build_registry.py`
- [ ] Review `catalog/skills-dictionary.md`
- [ ] Review `catalog/active-skills.md` or `catalog/archived-skills.md`
