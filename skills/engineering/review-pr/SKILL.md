---
name: review-pr
description: Reviews the current branch like a PR — intent, approach, and actionable feedback. Use when reviewing PRs or branches, a PR URL or number, summarizing changes, or seeking feedback before opening or merging.
disable-model-invocation: true
---

# Review PR

Reviews the current branch like a PR. The review itself runs in a subagent with its own context, so it stays small however long this conversation is and isn't shaped by what was discussed here. Your job is to set it up, tell the user it has started, and show the result.

## 1. Pick the target

Default: the **current branch** against its merge base. If the user names a PR or branch (`github.com/.../pull/123`, `review PR #456`, `review feature/foo`):

1. Resolve it to the PR head branch or named branch (`gh pr checkout`, `gh pr view --json headRefName`, etc.).
2. If that branch is already checked out, continue. Otherwise switch to it.
3. If Git refuses (local changes would be overwritten, conflicts, or other blockers), explain the blocker and ask whether to stash. Stash only after the user confirms, then retry the switch.

Note any **base branch** the user named, whether they asked for **uncommitted or staged changes only**, and whether they asked for a **thorough review**.

Don't run gather, read the diff, or read `review.md` yourself: the subagent does that.

## 2. Say what's happening

Before launching the subagent, tell the user in one line what is being reviewed and that it runs separately, for example:

> Reviewing `feature/foo` against `main` in a separate context. This usually takes a minute or two.

## 3. Launch the review

Start one subagent (general-purpose) with a short description like `Review feature/foo`. Give it only:

- the repo path, the branch, and any base branch, scope, or thorough flag from step 1
- the path to this skill's [review.md](review.md), with the instruction to follow it and return the finished review as its final message

Don't pass the conversation or your own summary of the changes.

If no subagent tool is available, read [review.md](review.md) and follow it inline.

## 4. Show the review

Show the subagent's review as-is rather than re-summarising it. Review-only: don't change code unless the user asks. If it is a pre-PR review, the user may reply by finding number ("fix 2"); apply those fixes here, re-reading files as needed.
