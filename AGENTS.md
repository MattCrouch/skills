# Matt's Skills

Skills are organised into bucket folders under `skills/`:

- `engineering/` — Daily code work

Personal (non-engineering) skills live in the separate [personal-skills](https://github.com/MattCrouch/personal-skills) repo.

All skills ship as a single plugin (`.claude-plugin/plugin.json` at the repo root, referenced by one entry in `.claude-plugin/marketplace.json`). Every skill must have a reference in the top-level `README.md`. Run `python3 scripts/generate_marketplace.py` to regenerate `plugin.json`, `marketplace.json`, and the READMEs from each skill's `SKILL.md` frontmatter.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
