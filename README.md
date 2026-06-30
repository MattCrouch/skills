# My skills

Personal agent skills, shared across machines and projects.

## Install via Claude Code (marketplace)

```bash
/plugin marketplace add your-github-username/skills
/plugin install <skill-name>@matt-skills
```

## Install manually

```bash
git clone https://github.com/your-github-username/skills.git
cp -r skills/skills/engineering/<skill-name> ~/.claude/skills/
```

## Use in Cursor

Cursor has no global skills directory yet — copy or symlink per project:

```bash
cp -r skills/skills/engineering/<skill-name> .cursor/skills/
```
