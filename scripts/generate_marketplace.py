#!/usr/bin/env python3
"""
Scans skills/<bucket>/<skill-name>/SKILL.md for every bucket and regenerates:

  - .claude-plugin/marketplace.json
  - skills/<bucket>/README.md      (one per bucket)
  - README.md                      (top-level "Skills" section)

Every skill, in either bucket, is listed — per AGENTS.md.

Run manually with:   python3 scripts/generate_marketplace.py
Or let the pre-commit hook run it for you (see scripts/install_hooks.sh).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PROMOTED_BUCKETS = ["engineering", "personal"]
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
TOP_README = ROOT / "README.md"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)


def parse_skill_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{path} has no YAML frontmatter (expected --- ... ---)")
    fields = dict(FIELD_RE.findall(match.group(1)))
    if "name" not in fields or "description" not in fields:
        raise ValueError(f"{path} frontmatter must include 'name' and 'description'")
    return {"name": fields["name"].strip(), "description": fields["description"].strip()}


def discover_skills() -> dict:
    """Returns {bucket: [ {name, description, dir_name}, ... ]}"""
    discovered = {}
    for bucket in PROMOTED_BUCKETS:
        bucket_dir = SKILLS_DIR / bucket
        skills = []
        if bucket_dir.exists():
            for skill_dir in sorted(bucket_dir.iterdir()):
                skill_md = skill_dir / "SKILL.md"
                if skill_dir.is_dir() and skill_md.exists():
                    meta = parse_skill_md(skill_md)
                    meta["dir_name"] = skill_dir.name
                    skills.append(meta)
        discovered[bucket] = skills
    return discovered


def write_marketplace_json(discovered: dict):
    plugins = []
    for bucket, skills in discovered.items():
        for skill in skills:
            plugins.append(
                {
                    "name": skill["name"],
                    "description": skill["description"],
                    "source": f"./skills/{bucket}/{skill['dir_name']}",
                }
            )

    existing = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    existing["plugins"] = plugins
    MARKETPLACE_JSON.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")


BUCKET_TITLES = {"engineering": "Engineering", "personal": "Personal"}


def write_bucket_readme(bucket: str, skills: list):
    path = SKILLS_DIR / bucket / "README.md"
    lines = [f"# {BUCKET_TITLES.get(bucket, bucket.title())}\n"]
    bucket_blurb = {
        "engineering": "Skills I use daily for code work.",
        "personal": "Skills tied to my own setup.",
    }
    lines.append(bucket_blurb.get(bucket, "") + "\n")
    lines.append("| Skill | Description |")
    lines.append("|---|---|")
    if skills:
        for skill in skills:
            lines.append(f"| [{skill['name']}]({skill['dir_name']}/SKILL.md) | {skill['description']} |")
    else:
        lines.append("| _(none yet)_ | |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_top_readme(discovered: dict):
    text = TOP_README.read_text(encoding="utf-8")

    section_lines = ["## Skills\n"]
    for bucket in PROMOTED_BUCKETS:
        section_lines.append(f"### {BUCKET_TITLES.get(bucket, bucket.title())}\n")
        skills = discovered[bucket]
        if skills:
            for skill in skills:
                link = f"skills/{bucket}/{skill['dir_name']}/SKILL.md"
                section_lines.append(f"- [{skill['name']}]({link}) — {skill['description']}")
        else:
            section_lines.append("_(none yet)_")
        section_lines.append("")

    new_section = "\n".join(section_lines).rstrip() + "\n"

    if "## Skills" in text:
        text = text[: text.index("## Skills")] + new_section
    else:
        text = text.rstrip() + "\n\n" + new_section

    TOP_README.write_text(text, encoding="utf-8")


def main():
    discovered = discover_skills()
    write_marketplace_json(discovered)
    for bucket, skills in discovered.items():
        write_bucket_readme(bucket, skills)
    write_top_readme(discovered)

    total = sum(len(v) for v in discovered.values())
    print(f"Regenerated marketplace.json and README files — {total} skill(s) indexed.")


if __name__ == "__main__":
    main()
