# Thorough review checklist

Apply when the user requests a **thorough review**.

- [ ] Logic handles edge cases (null/empty, loading, error, permissions)
- [ ] Types derived from GraphQL/codegen where applicable — no hand-rolled API shapes
- [ ] Tests cover new/changed behavior; assertions use roles/labels/text, not implementation details
- [ ] No secrets, `console.log`, or eslint-disable suppressions
- [ ] Styling follows project patterns (Emotion + design tokens, no inline styles)
- [ ] Handlers passed to children use `useCallback` where the codebase does
- [ ] Cross-package imports use path aliases, not relative paths across packages
- [ ] Change scope is focused — no unrelated drive-by edits
