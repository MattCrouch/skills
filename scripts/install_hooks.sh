#!/usr/bin/env bash
# Run this once after cloning to enable the auto-regenerating pre-commit hook.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
chmod +x "$REPO_ROOT/.githooks/pre-commit"
git -C "$REPO_ROOT" config core.hooksPath .githooks

echo "Hooks installed. marketplace.json and READMEs will now regenerate on every commit."
