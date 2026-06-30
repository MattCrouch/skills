# Reference

Apply severity and risk rubrics on every review. Apply the thorough checklist when the user requests **thorough review** or [adaptive depth](SKILL.md#adaptive-depth) triggers.

## Severity rubric

| Level               | Use when                                                         | Examples                                                                                                         |
| ------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 🔴 **Critical**     | Must fix before merge — correctness, security, or data integrity | Auth bypass, data loss/corruption, wrong default for existing users, broken API contract, production outage risk |
| 🟡 **Suggestion**   | Worth fixing — quality, maintainability, or missing coverage     | Unclear naming, missing edge-case handling, weak test for changed behavior, unnecessary complexity               |
| 🟢 **Nice-to-have** | Optional polish                                                  | Minor duplication, small refactor, style inconsistency that doesn't match a repeated pattern                     |

Every finding needs a file reference and a concrete fix or question. Do not inflate severity — if unsure between Critical and Suggestion, choose Suggestion and explain the uncertainty.

## Risk rubric

| Risk       | Use when                                                                                                                          |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Low**    | Docs, config-only, isolated UI copy, tests-only, or changes with clear coverage and limited blast radius                          |
| **Medium** | Behavior changes with reasonable tests, new endpoints/features behind flags, or moderate refactor with tests                      |
| **High**   | Auth, payments, migrations, shared infrastructure, data mutations, or production logic changed without corresponding test changes |

## Merge readiness

| Status               | Use when                                                                                       |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| **Ready**            | No Critical findings; approach matches intent; tests/CI look adequate for the risk level       |
| **Needs changes**    | One or more Critical findings, or Medium/High risk with clear test or logic gaps               |
| **Needs discussion** | Architectural trade-offs, ambiguous requirements, or conflicting approaches — not a simple fix |

## Thorough review checklist

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
