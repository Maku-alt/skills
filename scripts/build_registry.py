from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ARCHIVE_DIR = ROOT / "archive"
REFERENCES_DIR = ROOT / "references"
CATALOG_DIR = ROOT / "catalog"
CONFIG_DIR = ROOT / "config"
POLICY_PATH = CONFIG_DIR / "curation-policy.json"
PROJECTS_ROOT = Path(r"C:/Users/Victor/Proyectos/2026")

IGNORE_PARTS = {
    ".git",
    "node_modules",
    ".venv",
    "dist",
    "build",
    "__pycache__",
    ".next",
    ".cache",
}

SKILL_TAGS = {
    "analytics": {"data-analysis", "pandas-optimizer", "xlsx", "teradata-debug-sp", "jupyter-notebook"},
    "documents": {"docx", "pdf", "pptx", "internal-comms", "theme-factory", "doc-coauthoring", "frontend-slides"},
    "delivery": {
        "writing-plans",
        "requesting-code-review",
        "receiving-code-review",
        "verification-before-completion",
        "test-driven-development",
        "systematic-debugging",
        "using-git-worktrees",
        "subagent-driven-development",
    },
    "skills": {"skill-creator", "writing-skills", "brainstorming"},
    "automation": {"mcp-builder"},
    "testing": {"webapp-testing"},
}


@dataclass
class SkillRecord:
    slug: str
    title: str
    description: str
    location: str
    status: str
    last_updated: str
    content_hash: str
    tags: list[str]
    notes: str = ""


def load_policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def parse_frontmatter(skill_dir: Path) -> tuple[str, str]:
    skill_md = skill_dir / "SKILL.md"
    title = skill_dir.name
    description = ""
    if not skill_md.exists():
        return title, description
    for line in skill_md.read_text(encoding="utf-8", errors="ignore").splitlines()[:24]:
        if line.startswith("name:"):
            title = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"')
    return title, description


def hash_tree(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(file_path.relative_to(path)).encode("utf-8"))
        digest.update(file_path.read_bytes())
    return digest.hexdigest()


def latest_modified(path: Path) -> str:
    timestamps = [p.stat().st_mtime for p in path.rglob("*") if p.is_file()]
    if not timestamps:
        timestamps = [path.stat().st_mtime]
    return datetime.fromtimestamp(max(timestamps)).strftime("%Y-%m-%d")


def infer_tags(slug: str) -> list[str]:
    tags = sorted(tag for tag, names in SKILL_TAGS.items() if slug in names)
    return tags or ["general"]


def collect_skill_records(base_dir: Path, status: str, notes_map: dict[str, str]) -> list[SkillRecord]:
    records: list[SkillRecord] = []
    if not base_dir.exists():
        return records
    for skill_dir in sorted(p for p in base_dir.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            continue
        title, description = parse_frontmatter(skill_dir)
        records.append(
            SkillRecord(
                slug=skill_dir.name,
                title=title,
                description=description,
                location=str(skill_dir),
                status=status,
                last_updated=latest_modified(skill_dir),
                content_hash=hash_tree(skill_dir),
                tags=infer_tags(skill_dir.name),
                notes=notes_map.get(skill_dir.name, ""),
            )
        )
    return records


def collect_reference_records() -> list[SkillRecord]:
    records: list[SkillRecord] = []
    if not REFERENCES_DIR.exists():
        return records
    for source_dir in sorted(p for p in REFERENCES_DIR.iterdir() if p.is_dir()):
        for skill_dir in sorted(p for p in source_dir.iterdir() if p.is_dir()):
            if not (skill_dir / "SKILL.md").exists():
                continue
            title, description = parse_frontmatter(skill_dir)
            records.append(
                SkillRecord(
                    slug=skill_dir.name,
                    title=title,
                    description=description,
                    location=str(skill_dir),
                    status="reference",
                    last_updated=latest_modified(skill_dir),
                    content_hash=hash_tree(skill_dir),
                    tags=["reference"],
                    notes=f"Imported as external reference from {source_dir.name}.",
                )
            )
    return records


def project_extension_profile(repo_dir: Path) -> Counter:
    counts: Counter[str] = Counter()
    for path in repo_dir.rglob("*"):
        if any(part in IGNORE_PARTS for part in path.parts):
            continue
        if path.is_file():
            counts[path.suffix.lower() or "[noext]"] += 1
    return counts


def recommend_skills(repo_name: str, counts: Counter) -> list[str]:
    picks = [
        "brainstorming",
        "writing-plans",
        "verification-before-completion",
    ]
    if counts[".py"] or counts[".ipynb"] or counts[".r"] or counts[".ts"] or counts[".js"] or counts[".mjs"]:
        picks += ["systematic-debugging", "test-driven-development", "requesting-code-review"]
    if counts[".csv"] or counts[".xlsx"] or counts[".ipynb"]:
        picks += ["data-analysis", "pandas-optimizer", "xlsx"]
    if counts[".pptx"]:
        picks += ["pptx", "theme-factory", "frontend-slides", "internal-comms"]
    if counts[".docx"]:
        picks += ["docx", "doc-coauthoring"]
    if counts[".pdf"]:
        picks += ["pdf"]
    if counts[".html"] or counts[".ts"] or counts[".js"] or counts[".mjs"]:
        picks += ["webapp-testing"]
    if "analitica" in repo_name or "tesis" in repo_name:
        picks += ["teradata-debug-sp"]
    if counts[".ipynb"]:
        picks += ["jupyter-notebook"]
    if "mcp" in repo_name:
        picks += ["mcp-builder"]
    ordered: list[str] = []
    for skill in picks:
        if skill not in ordered:
            ordered.append(skill)
    return ordered


def build_project_recommendations() -> list[dict]:
    results = []
    for repo_dir in sorted(
        p for p in PROJECTS_ROOT.iterdir() if p.is_dir() and p.name not in {".git", "skills-registry"}
    ):
        counts = project_extension_profile(repo_dir)
        results.append(
            {
                "repo": repo_dir.name,
                "top_files": [{"ext": ext, "count": count} for ext, count in counts.most_common(8)],
                "recommended_skills": recommend_skills(repo_dir.name.lower(), counts),
            }
        )
    return results


def write_index(active: list[SkillRecord], archived: list[SkillRecord], references: list[SkillRecord], recommendations: list[dict]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "active_skill_count": len(active),
        "archived_skill_count": len(archived),
        "reference_skill_count": len(references),
        "skills": [asdict(record) for record in active],
        "archived_skills": [asdict(record) for record in archived],
        "references": [asdict(record) for record in references],
        "project_recommendations": recommendations,
    }
    (CATALOG_DIR / "skills-index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_dictionary(active: list[SkillRecord], references: list[SkillRecord]) -> None:
    lines = [
        "# Skills Dictionary",
        "",
        f"- `last_registry_refresh`: `{datetime.now().strftime('%Y-%m-%d')}`",
        f"- `active_skills`: `{len(active)}`",
        f"- `reference_skills`: `{len(references)}`",
        "",
        "## Active skills",
        "",
        "| Skill | Last updated | Tags | Description |",
        "| --- | --- | --- | --- |",
    ]
    for record in active:
        desc = record.description.replace("\n", " ").strip()
        lines.append(
            f"| `{record.slug}` | `{record.last_updated}` | `{', '.join(record.tags)}` | {desc} |"
        )

    lines += [
        "",
        "## External references",
        "",
        "| Skill | Last updated | Note |",
        "| --- | --- | --- |",
    ]
    for record in references:
        lines.append(
            f"| `{record.slug}` | `{record.last_updated}` | {record.notes} |"
        )

    (CATALOG_DIR / "skills-dictionary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_skill_status(active: list[SkillRecord], archived: list[SkillRecord]) -> None:
    active_lines = [
        "# Active Skills",
        "",
        "Skills currently kept in `skills/` and recommended for day-to-day use.",
        "",
    ]
    for record in active:
        active_lines.append(f"- `{record.slug}`: {record.notes or record.description}")
    active_lines.append("")
    (CATALOG_DIR / "active-skills.md").write_text("\n".join(active_lines), encoding="utf-8")

    archived_lines = [
        "# Archived Skills",
        "",
        "Skills moved to `archive/` because they are not part of the current working set.",
        "",
    ]
    for record in archived:
        archived_lines.append(f"- `{record.slug}`: {record.notes or 'Archived by curation policy.'}")
    archived_lines.append("")
    (CATALOG_DIR / "archived-skills.md").write_text("\n".join(archived_lines), encoding="utf-8")


def write_project_recommendations(recommendations: list[dict]) -> None:
    lines = [
        "# Project Recommendations",
        "",
        "Skills suggested from the current active registry based on the file profile of each repo.",
        "",
    ]
    for item in recommendations:
        top_files = ", ".join(f"`{entry['ext']}`:{entry['count']}" for entry in item["top_files"])
        skills = ", ".join(f"`{skill}`" for skill in item["recommended_skills"])
        lines += [
            f"## {item['repo']}",
            "",
            f"- Top files: {top_files or 'none'}",
            f"- Recommended skills: {skills}",
            "",
        ]
    (CATALOG_DIR / "project-recommendations.md").write_text("\n".join(lines), encoding="utf-8")


def write_curation_report(policy: dict, active: list[SkillRecord], archived: list[SkillRecord]) -> None:
    policy_active = [item["slug"] for item in policy["active_skills"]]
    policy_archived = [item["slug"] for item in policy["archived_skills"]]
    active_found = {record.slug for record in active}
    archived_found = {record.slug for record in archived}
    missing_active = [name for name in policy_active if name not in active_found]
    missing_archived = [name for name in policy_archived if name not in archived_found]

    lines = [
        "# Curation Report",
        "",
        "- Legacy sources such as `context-base` and `context-analitica-avanzada` are no longer treated as canonical.",
        "- Ongoing maintenance should happen directly inside this registry.",
        "",
        f"- Active skills present: `{len(active)}`",
        f"- Archived skills present: `{len(archived)}`",
        "",
        "## Missing active entries from policy",
        "",
    ]
    if missing_active:
        lines.extend(f"- `{name}`" for name in missing_active)
    else:
        lines.append("- None")
    lines += ["", "## Missing archived entries from policy", ""]
    if missing_archived:
        lines.extend(f"- `{name}`" for name in missing_archived)
    else:
        lines.append("- None")
    lines.append("")
    (CATALOG_DIR / "curation-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    policy = load_policy()
    active_notes = {item["slug"]: item["reason"] for item in policy["active_skills"]}
    archived_notes = {item["slug"]: item["reason"] for item in policy["archived_skills"]}

    active = collect_skill_records(SKILLS_DIR, "active", active_notes)
    archived = collect_skill_records(ARCHIVE_DIR, "archived", archived_notes)
    references = collect_reference_records()
    recommendations = build_project_recommendations()

    write_index(active, archived, references, recommendations)
    write_dictionary(active, references)
    write_skill_status(active, archived)
    write_project_recommendations(recommendations)
    write_curation_report(policy, active, archived)

    print(f"Active skills: {len(active)}")
    print(f"Archived skills: {len(archived)}")
    print(f"Reference skills: {len(references)}")


if __name__ == "__main__":
    main()
