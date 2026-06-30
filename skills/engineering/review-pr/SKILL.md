---
name: review-pr
description: Reviews the current branch like a PR — intent, approach, and actionable feedback. Use when reviewing PRs or branches, a PR URL or number, summarizing changes, or seeking feedback before opening or merging.
disable-model-invocation: true
---

# Review PR

Answer these questions, then render the answer using the output format below:

> Walk me through this PR. What's it trying to accomplish, and what's the approach?
>
> What would you flag before merge? Any improvements worth suggesting?

Review-only — do not change code unless the user asks.

## Review target

Default: review the **current branch** against its merge base. If the user names a specific PR or branch, resolve and check it out first — then run the fast path.

Examples: `github.com/.../pull/123`, `review PR #456`, `review feature/foo`.

1. Resolve the PR link, PR number, or branch name to the PR head branch or named branch (`gh pr checkout`, `gh pr view --json headRefName`, etc.).
2. If that branch is already checked out, continue.
3. If a different branch is checked out, switch to the target branch.
4. If Git refuses (local changes would be overwritten, conflicts, or other blockers), explain the blocker and ask whether to stash. Stash only after the user confirms, then retry the switch.
5. Run the gather script only after the correct branch is checked out locally.

If the user names a **base branch**, run gather with `REVIEW_PR_BASE=<branch>`. If they ask to review **uncommitted or staged changes only**, use `git diff` or `git diff --cached` instead of the branch diff — mention scope in the review header.

## Fast path (always start here)

Unless the user says **thorough review**, always begin with the fast path — then apply [adaptive depth](#adaptive-depth) if warranted.

1. Run [scripts/gather.sh](scripts/gather.sh) from the **repo under review** (one round-trip). Resolve the path from this skill's directory — e.g. replace `/SKILL.md` with `/scripts/gather.sh` in the skill's `fullPath`. Execute the script; do not copy or rewrite it. **Use shell permissions that allow GitHub API access** (`required_permissions: ["all"]` or `["full_network"]`) — without this, `gh` fails silently and the base branch falls back incorrectly.

   ```bash
   bash "<skill-dir>/scripts/gather.sh"
   ```

   If the user names a **base branch**, pass `REVIEW_PR_BASE=<branch>`.

2. Use PR metadata from `gh` when available — title/body for intent, file list for scope, CI and review decision for merge readiness. Compare any test plan in the PR body against what the diff actually covers.
3. Read the diff output. Open changed source files only when a hunk is unclear or you need surrounding context. Do not read unchanged files.
4. Do not re-read `AGENTS.md` — workspace rules already apply.
5. Apply [severity and risk rubrics](reference.md#severity-rubric) from `reference.md`. Cap findings: up to 5 blocking, 5 suggestions, 3 nice-to-haves. Omit empty sections.
6. Use file paths in findings. Add line numbers only for blocking issues.

**PR context from `gh`**: When present, factor into the review:

- **Failing or pending CI** → note in Summary; treat failures as merge blockers unless clearly unrelated/flaky (say why).
- **`CHANGES_REQUESTED` or open review comments** → note in Summary as "Needs discussion" or incorporate into findings if still valid against the current diff.
- **Test plan in PR body** → compare checkboxes/steps to test files and behaviors in the diff; feed gaps into [Test plan gaps](#output-format).
- **No open PR** → branch-only review; omit CI/review rows from Summary.

**Base branch**: `gather.sh` uses the open PR's `baseRefName` when `gh` succeeds, otherwise detects from `origin/HEAD`, then `origin/master` or `origin/main`. Override with `REVIEW_PR_BASE`.

**Uncommitted changes**: Mention separately if `git status --short` shows any (run only when needed).

**Empty diff**: Say so in one sentence and stop.

**Large PRs**: Summarize by area from the stat, then read only the highest-risk hunks (logic, API, auth, data mutations). Skip re-reading large test-only diffs unless production code changed. If full `git diff` output is truncated, diff per path: `git diff "origin/${BASE}...HEAD" -- packages/foo/`.

## Adaptive depth

After the fast-path gather and initial diff read, escalate to thorough-mode steps when **any** of these apply:

- More than ~15 files or ~500 lines changed
- Touches auth, payments, data mutations, or shared infrastructure
- Production logic changed without corresponding test changes
- A potential blocking issue needs surrounding context to validate

When escalating:

1. Tell the user you are going deeper and why (one sentence).
2. Apply the thorough-mode steps below for the affected files only — not necessarily the whole PR.
3. Include the Test plan gaps section in the output.

If none of the triggers apply, stay on the fast path.

## Thorough mode

Apply when the user says **thorough review**, or when [adaptive depth](#adaptive-depth) triggers:

- Read every changed file in full, not just diff hunks (or only the affected high-risk files when escalating adaptively)
- Include line numbers on all findings
- Include the Test plan gaps section
- Apply the thorough checklist and [project conventions](reference.md#project-conventions) in [reference.md](reference.md)

## Output format

```markdown
# PR Review: [branch name]

[One sentence: what this PR does and whether the approach looks sound overall.]

## What it's trying to accomplish

[2–4 sentences. State the problem, the intended outcome, and who/what is affected. Ground this in the PR description, commit messages, and diff — not speculation.]

## Approach

[How the change is implemented: key files, patterns, data flow, API/GraphQL changes, feature flags, etc. Note meaningful trade-offs if visible in the code.]

## What's working well

[1–3 bullets on genuine strengths — clear structure, good tests, sensible abstractions, focused scope. Omit section if nothing notable; do not pad with praise.]

## Review findings

### Must address before merge

[Blocking issues only. Omit section if none.]

| Severity    | Location           | Finding                        |
| ----------- | ------------------ | ------------------------------ |
| 🔴 Critical | `path/to/file.tsx` | [Specific, actionable finding] |

### Suggestions

[Non-blocking improvements. Omit section if none.]

| Severity      | Location           | Finding                        |
| ------------- | ------------------ | ------------------------------ |
| 🟡 Suggestion | `path/to/file.tsx` | [Specific, actionable finding] |

### Improvements worth considering

[Optional polish. Omit section if none.]

- [Improvement with brief rationale]

## Test plan gaps

[Include after adaptive escalation, in thorough mode, when risk is Medium/High, or when changed behavior clearly lacks test coverage.]

## Summary

|                     |                                                                         |
| ------------------- | ----------------------------------------------------------------------- |
| **Commits**         | N                                                                       |
| **Files changed**   | N (+/− lines)                                                           |
| **CI**              | All passing / N failing — [check names; omit if no open PR]             |
| **PR reviews**      | Approved / Changes requested / Review required — [omit if no open PR]   |
| **Risk**            | Low / Medium / High — [one-line reason; see rubric](reference.md#risk-rubric) |
| **Merge readiness** | Ready / Needs changes / Needs discussion — [see rubric](reference.md#merge-readiness) |
| **Review depth**    | Fast / Adaptive (escalated) / Thorough — [one-line reason if escalated] |
```

## Rules

- **Be specific**: Every finding needs a file reference and a concrete fix or question.
- **Separate intent from critique**: "What it's trying to accomplish" and "Approach" are descriptive; "Review findings" is evaluative. "What's working well" is optional and separate from both.
- **Skip nitpicks** unless they repeat a pattern or violate project conventions.
