# My skills

Personal agent skills shared across machines and projects.

## Installation

### Claude Code

```bash
/plugin marketplace add your-github-username/skills
/plugin install <skill-name>@matt-skills
```

## Cursor

```bash
cp -r skills/engineering/<skill-name> .cursor/skills/
```

## Skills

### Engineering

- [review-pr](skills/engineering/review-pr/SKILL.md) — Reviews the current branch like a PR — intent, approach, and actionable feedback. Use when reviewing PRs or branches, a PR URL or number, summarizing changes, or seeking feedback before opening or merging.

### Learning

- [reading-digest](skills/learning/reading-digest/SKILL.md) — Digest material the user explicitly wants processed — summarize an article or document into key takeaways, check the user's stated understanding against the source, or connect it to earlier material. Use only when the user asks for a summary, digest, takeaways, or a check of their understanding of something they've read. Do not trigger just because a URL or document appears in the message — a bare link with little or no request is not enough, as links are often shared for other reasons (debugging, reference, context for another task).
