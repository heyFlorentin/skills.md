---
alwaysApply: true
scene: git_message
---

# Git Commit Guidelines

## Commit Message Format

```txt
<type>(<scope>): <subject>

<body>

<footer>
```

- **Header** is mandatory. **Scope** is optional.
- No line may exceed **100 characters**.

## Type

MUST be one of:

| Type | Description |
| ------ | ------------- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, missing semicolons, etc. (no code change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or correcting tests |
| `chore` | Build process, tooling, dependencies |
| `perf` | Performance improvement |
| `ci` | CI/CD configuration |

## Subject

- Use **imperative, present tense**: `add` not `added` or `adds`.
- Do NOT capitalize the first letter.
- Do NOT end with a period.

## Body

- Use **imperative, present tense**.
- MUST include the **motivation** for the change.
- MUST contrast with previous behavior where applicable.

## Footer

- Reference issues this commit **Closes**: `Closes #123, #456`.
- **Breaking Changes** MUST start with `BREAKING CHANGE:` followed by a space or two newlines, then the description.

## Revert

If reverting a previous commit, the header MUST be:

```txt
revert: <header of reverted commit>
```

The body MUST contain:

```txt
This reverts commit <hash>.
```

## Examples

**Feature with scope:**

```txt
feat(navigation): add mega-menu component

Implements the mega-menu variant for the navigation component
as specified in ECL v1.15.0 guidelines.

Closes #234
```

**Breaking change:**

```txt
refactor(button): remove deprecated size variants

BREAKING CHANGE: The `small` and `large` size props are removed.
Use `size="sm"` and `size="lg"` instead.

Closes #567
```
