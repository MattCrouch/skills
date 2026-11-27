# Reference

Apply severity and risk rubrics and the agent-written code checks on every review. The thorough checklist and project conventions live in [thorough.md](thorough.md); read it only when the user requests **thorough review** or [adaptive depth](SKILL.md#adaptive-depth) triggers.

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

## Agent-written code checks

Mistakes agents often make. Most show up in the diff without opening other files:

- [ ] Tests weakened to pass — assertions loosened, cases deleted, or tests skipped (`.skip`, `xit`, `@skip`)
- [ ] Lint or type suppressions added to get green, rather than fixing the cause
- [ ] Debug logging, TODOs, or commented-out code left behind
- [ ] Files, refactors, or renames beyond what the change needs
- [ ] Calls to functions, props, or APIs not defined in the diff — check they exist before flagging
- [ ] New helpers that duplicate a utility already in the codebase
