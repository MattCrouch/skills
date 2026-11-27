#!/usr/bin/env bash
# Gather PR metadata and branch diff for the review-pr skill.
# Run from the repository under review.
# Optional: REVIEW_PR_BASE=main ./scripts/gather.sh

PR_JSON="$(gh pr view --json baseRefName,title,body,url,headRefName,additions,deletions,changedFiles,files,statusCheckRollup,reviewDecision,latestReviews,state,isDraft 2>/dev/null || true)"

if [ -n "${REVIEW_PR_BASE:-}" ]; then
  BASE="$REVIEW_PR_BASE"
else
  BASE="$(printf '%s' "$PR_JSON" | jq -r '.baseRefName // empty' 2>/dev/null)"
  BASE="${BASE:-$(
    git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' \
    || { git rev-parse --verify origin/master >/dev/null 2>&1 && echo master; } \
    || { git rev-parse --verify origin/main >/dev/null 2>&1 && echo main; } \
    || echo master
  )}"
fi

echo "branch: $(git rev-parse --abbrev-ref HEAD)"

if [ -n "$PR_JSON" ] && [ "$PR_JSON" != "null" ] && printf '%s' "$PR_JSON" | jq -e . >/dev/null 2>&1; then
  printf '%s' "$PR_JSON" | jq -r '
    "PR: \(.title)",
    .url,
    (if .body != "" then "\n\(.body)\n" else "" end),
    "base: \(.baseRefName) <- head: \(.headRefName) (\(.state)\(if .isDraft then ", draft" else "" end))",
    "stats: \(.changedFiles) files (+\(.additions)/-\(.deletions))",
    "",
    "files:",
    (.files[]? | "  \(.path) (+\(.additions)/-\(.deletions))"),
    "",
    "ci:",
    (
      [.statusCheckRollup[]? |
        if .__typename == "CheckRun" then
          (if .status != "COMPLETED" then "\(.name): \(.status)"
           elif (.conclusion == "SUCCESS" or .conclusion == "SKIPPED" or .conclusion == "NEUTRAL") then empty
           else "\(.name): \(.conclusion)" end)
        elif .__typename == "StatusContext" then
          (if (.state == "SUCCESS" or .state == "EXPECTED") then empty else "\(.context): \(.state)" end)
        else empty end
      ] | if length == 0 then "  all passing" else .[] | "  \(.)" end
    ),
    "",
    "review decision: \(.reviewDecision // "none")",
    (.latestReviews[]? | select(.state != "APPROVED" and .state != "DISMISSED") | "  \(.author.login): \(.state)\(if .body != "" then " — " + (.body | gsub("\n"; " ") | .[0:120]) else "" end)")
  '
else
  echo "no open PR for this branch"
fi

git rev-parse --verify "origin/${BASE}" >/dev/null 2>&1 \
  || { echo "error: origin/${BASE} not found — fetch or check base branch"; exit 1; }

# Lockfiles, snapshots, and generated/minified output are noisy and rarely
# worth reviewing line by line. They still appear in the stat above the diff.
EXCLUDES=(
  ':(exclude,glob)**/package-lock.json'
  ':(exclude,glob)**/pnpm-lock.yaml'
  ':(exclude,glob)**/yarn.lock'
  ':(exclude,glob)**/*.lock'
  ':(exclude,glob)**/*.snap'
  ':(exclude,glob)**/*.min.*'
  ':(exclude,glob)**/*.map'
)
MAX_DIFF_LINES="${REVIEW_PR_MAX_DIFF_LINES:-1500}"

git log --oneline "origin/${BASE}..HEAD"
git diff --stat "origin/${BASE}...HEAD"

DIFF_LINES="$(git diff "origin/${BASE}...HEAD" -- . "${EXCLUDES[@]}" | wc -l | tr -d ' ')"
if [ "$DIFF_LINES" -gt "$MAX_DIFF_LINES" ]; then
  echo ""
  echo "diff omitted: ${DIFF_LINES} lines (cap ${MAX_DIFF_LINES})."
  echo "Diff the highest-risk paths individually: git diff \"origin/${BASE}...HEAD\" -- <path>"
else
  echo ""
  echo "diff (lockfiles, snapshots, minified and map files excluded):"
  git diff "origin/${BASE}...HEAD" -- . "${EXCLUDES[@]}"
fi
