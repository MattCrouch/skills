---
name: review-pr
description: Reviews the current branch like a PR — intent, approach, and actionable feedback. Use when reviewing PRs or branches, a PR URL or number, summarizing changes, or seeking feedback before opening or merging.
---

# Review PR

Answer these questions, then render the answer using the output format below:

> Walk me through this PR. What's it trying to accomplish, and what's the approach?
>
> What would you flag before merge? Any improvements worth suggesting?

Review-only — do not change code unless the user asks. Do not delegate to a subagent unless the user explicitly asks for Bugbot or security review.

## Review target

Default: review the **current branch** against its merge base. If the user names a specific PR or branch, resolve and check it out first — then run the fast path.

Examples: `github.com/.../pull/123`, `review PR #456`, `review feature/foo`.

1. Resolve the PR link, PR number, or branch name to the PR head branch or named branch (`gh pr checkout`, `gh pr view --json headRefName`, etc.).
2. If that branch is already checked out, continue.
3. If a different branch is checked out, switch to the target branch.
4. If Git refuses (local changes would be overwritten, conflicts, or other blockers), explain the blocker and ask whether to stash. Stash only after the user confirms, then retry the switch.
5. Run the gather script only after the correct branch is checked out locally.

If the user names a **base branch**, substitute it for `BASE` in the gather script. If they ask to review **uncommitted or staged changes only**, use `git diff` or `git diff --cached` instead of the branch diff — mention scope in the review header.

## Fast path (always start here)

Unless the user says **thorough review**, always begin with the fast path — then apply [adaptive depth](#adaptive-depth) if warranted.

1. Run the gather script below (one round-trip). **Use shell permissions that allow GitHub API access** (`required_permissions: ["all"]` or `["full_network"]`) — without this, `gh` fails silently and the base branch falls back incorrectly.
2. Use PR title/body from `gh` for intent when available — don't re-derive from commits alone.
3. Read the diff output. Open changed source files only when a hunk is unclear or you need surrounding context. Do not read unchanged files.
4. Do not re-read `AGENTS.md` — workspace rules already apply.
5. Apply [severity and risk rubrics](reference.md#severity-rubric) from `reference.md`. Cap findings: up to 5 blocking, 5 suggestions, 3 nice-to-haves. Omit empty sections.
6. Use file paths in findings. Add line numbers only for blocking issues.

```bash
BASE=$(
  gh pr view --json baseRefName -q .baseRefName 2>/dev/null \
  || git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' \
  || { git rev-parse --verify origin/master >/dev/null 2>&1 && echo master; } \
  || { git rev-parse --verify origin/main >/dev/null 2>&1 && echo main; } \
  || echo master
)

echo "branch: $(git rev-parse --abbrev-ref HEAD)"
gh pr view --json title,body,url -q '"PR: \(.title)\n\(.body)\n\(.url)"' 2>/dev/null || true

git rev-parse --verify "origin/${BASE}" >/dev/null 2>&1 \
  || { echo "error: origin/${BASE} not found — fetch or check base branch"; exit 1; }

git log --oneline "origin/${BASE}..HEAD"
git diff --stat "origin/${BASE}...HEAD"
git diff "origin/${BASE}...HEAD"
```

**Base branch**: Use the open PR's `baseRefName` when `gh` succeeds. Otherwise detect from `origin/HEAD`, then `origin/master` or `origin/main`. If the user names a base branch, substitute it for `BASE`.

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
| **Risk**            | Low / Medium / High — [one-line reason; see rubric](reference.md#risk-rubric) |
| **Merge readiness** | Ready / Needs changes / Needs discussion — [see rubric](reference.md#merge-readiness) |
| **Review depth**    | Fast / Adaptive (escalated) / Thorough — [one-line reason if escalated] |
```

## Rules

- **Be specific**: Every finding needs a file reference and a concrete fix or question.
- **Separate intent from critique**: "What it's trying to accomplish" and "Approach" are descriptive; "Review findings" is evaluative.
- **Skip nitpicks** unless they repeat a pattern or violate project conventions.

## Related skills

- Bug-focused review: `review-bugbot`
- Security-focused review: `review-security`
- Getting a PR merge-ready: `babysit`
