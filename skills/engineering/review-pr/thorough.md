# Thorough review

Read this only for a **thorough review** or when [adaptive depth](review.md#adaptive-depth) triggers. Apply it on top of the rubrics and agent-written code checks in [reference.md](reference.md).

## Checklist

Generic checks — apply in addition to [project conventions](#project-conventions) when present:

- [ ] Logic handles edge cases (null/empty, loading, error, permissions)
- [ ] Types and API shapes match project patterns — no hand-rolled duplicates of generated or shared types
- [ ] Tests cover new/changed behavior; assertions target observable outcomes, not implementation details
- [ ] No secrets, debug logging left in, or lint/type suppressions without justification
- [ ] UI and styling follow existing project patterns in changed files
- [ ] Change scope is focused — no unrelated drive-by edits

## Project conventions

Before thorough review or when a finding depends on team standards, check the **repo under review** (not the skills repo) for:

- `AGENTS.md`, `CLAUDE.md`, or `.cursor/rules/` — follow these over generic defaults
- `CONTRIBUTING.md` or `docs/` review guidelines
- Obvious stack signals in the diff (e.g. GraphQL codegen, a specific UI library) — match conventions visible in neighboring unchanged code

If project docs conflict with the generic checklist, project docs win.
