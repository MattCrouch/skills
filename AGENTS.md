# Matt's Skills

Skills are organised into bucket folders under `skills/`:

- `engineering/` — Daily code work
- `personal/` - Ad-hoc, non-code for personal use

Every skill, in either bucket, must have a reference in the top-level `README.md`, an entry in `.claude-plugin/marketplace.json`, and its own `.claude-plugin/plugin.json` manifest. Run `python3 scripts/generate_marketplace.py` to regenerate all of these from each skill's `SKILL.md` frontmatter.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
