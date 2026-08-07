---
alwaysApply: false
description: This rule applies to all package operations in this repository: install, add, remove, update, audit, run scripts, and CI/CD pipelines.
---

# PNPM v11 — Primary Package Manager Rule

## 1. Package Manager Enforcement

### 1.1 Core Requirement

- **MUST** use pnpm **v11.x** (latest v11 minor) as the sole package manager. **MUST NOT** use npm, yarn, or bun for any package operation.
- **MUST** declare the package manager in `package.json`:

```json
"packageManager": "pnpm@11.0.0"
```

- **MUST** set `engine-strict=true` in `.npmrc` to enforce the exact package manager:

```ini
engine-strict=true
```

### 1.2 Version Pinning

- **MUST NOT** use `^` or `~` in `dependencies` or `devDependencies`. Pin exact versions only (`"1.2.3"`, not `"^1.2.3"`). This eliminates the `node_modules` differential across maintenance gaps and ensures deterministic installs.
- **MUST** commit `pnpm-lock.yaml` to version control. It is the single source of truth for dependency resolution.
- **MUST** run `pnpm install --frozen-lockfile` in CI/CD and all automated environments. **MUST NOT** allow lockfile mutation outside local development.

### 1.3 CI/CD Integration (GitHub Actions)

- **MUST** use `pnpm/action-setup@v4` with `version: 11` in all GitHub Actions workflows. Example:

```yaml
- uses: pnpm/action-setup@v4
  with:
    version: 11
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: pnpm
```

- **MUST** cache `pnpm store` via the built-in `cache: pnpm` option in `setup-node`. Do not add manual cache steps.
- **MUST** run `pnpm install --frozen-lockfile` as the install step in CI.

---

## 2. Solo-Developer Maintenance Cadence

### 2.1 One-Month-Per-Year Principle

The repository is designed for ~1 active maintenance month per year. All dependency and tooling decisions **MUST** optimize for rapid re-onboarding after extended dormancy (10–11 months).

- **MUST** prefer zero-config tools and convention-over-configuration patterns. A single `pnpm install && pnpm dev` **MUST** be sufficient to start development after any dormancy period.
- **MUST NOT** introduce global tooling dependencies (e.g., globally installed CLI tools, system-level package managers, Docker daemons). All tooling **MUST** be reproducible via `pnpm` alone.
- **MUST** run `pnpm update --latest --interactive` once at the start of each active maintenance window. Review each major version bump individually.

### 2.2 Onboarding & Re-Onboarding Checklist

The following single-command sequence **MUST** be sufficient to resume development:

```bash
pnpm install --frozen-lockfile   # restore exact dependency state
pnpm dev                          # start development server
```

If `--frozen-lockfile` fails due to stale lockfile, the developer **MUST** run:

```bash
pnpm install                      # regenerate lockfile from pinned versions
pnpm update --latest --interactive # selectively update during active window
```

### 2.3 Dependency Health Protocol

- **MUST** run `pnpm audit` once at the start of each active maintenance window. Fix critical and high-severity vulnerabilities before any feature work.
- **MUST** run `pnpm outdated` and review. Batch-safe patches (semver patch-level) can be applied immediately. Minor and major bumps **MUST** be reviewed for breaking changes.
- **MUST** batch all dependency updates into a single commit before feature work begins (e.g., `chore(deps): annual dependency refresh`).

---

## 3. High-Velocity Development Patterns

### 3.1 Scripts & Automation

- **MUST** use pnpm's built-in script runner. **MUST NOT** install task runners (gulp, grunt) unless already an existing project dependency.
- **MUST** define scripts in `package.json` using the `pnpm` prefix for cross-platform consistency:

```json
{
  "scripts": {
    "dev": "pnpm exec wrangler dev",
    "deploy": "pnpm exec wrangler deploy",
    "build": "pnpm exec wrangler deploy --dry-run",
    "typecheck": "pnpm exec tsc --noEmit",
    "lint": "pnpm exec eslint .",
    "fmt": "pnpm exec prettier --write .",
    "fmt:check": "pnpm exec prettier --check .",
    "test": "pnpm exec vitest run",
    "test:watch": "pnpm exec vitest",
    "audit:fix": "pnpm audit --fix",
    "clean": "rm -rf node_modules dist .wrangler",
    "fresh": "pnpm run clean && pnpm install"
  }
}
```

### 3.2 Adding Dependencies

- **MUST** pin exact versions when adding dependencies:

```bash
pnpm add <package> --save-exact
```

- **MUST** add dev-only tooling with `--save-dev` and `--save-exact`:

```bash
pnpm add -D <tool> --save-exact
```

### 3.3 Workspace & Monorepo Readiness

- If the project grows beyond a single package, **MUST** use `pnpm-workspace.yaml` (pnpm workspaces). **MUST NOT** use npm workspaces or yarn workspaces.
- **MUST** use `pnpm` catalogs (`pnpm-workspace.yaml` `catalog` field) for shared dependency versions across workspace packages.

---

## 4. Deployment (Cloudflare Workers via Wrangler)

### 4.1 Wrangler Integration

- **MUST** install `wrangler` as a dev dependency pinned to an exact version:

```bash
pnpm add -D wrangler --save-exact
```

- **MUST** invoke `wrangler` via `pnpm exec wrangler`, never through global `wrangler` or `npx`.
- **MUST NOT** commit `.wrangler` or `dist` directories. Ensure `.gitignore` includes:

```gitignore
.wrangler/
dist/
node_modules/
```

### 4.2 Deploy Script

- The deploy script **MUST** be exactly:

```json
"deploy": "pnpm exec wrangler deploy"
```

- CI/CD (GitHub Actions) **MUST** deploy via `pnpm run deploy` with `CF_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` stored in GitHub Secrets. Reference them as environment variables; **MUST NOT** hardcode credentials.

---

## 5. Version Control Hygiene

### 5.1 What to Commit

| Artifact | Commit? | Rationale |
| --- | --- | --- |
| `pnpm-lock.yaml` | **YES** | Sole source of truth for dependency resolution |
| `package.json` | **YES** | Manifest with exact pinned versions |
| `.npmrc` | **YES** | Ensure engine-strict and any registry config |
| `pnpm-workspace.yaml` | **YES** | If using workspaces |
| `node_modules/` | **NO** | Reproducible via `pnpm install` |
| `.wrangler/` | **NO** | Build artifacts |

### 5.2 .gitignore Additions

```gitignore
# pnpm
node_modules/
.pnpm-store/

# wrangler
.wrangler/
dist/

# env
.env
.env.*
!.env.example
```

---

## 6. Conflict Resolution

- If pnpm is unavailable in any environment, **MUST** install it via `corepack enable && corepack prepare pnpm@11 --activate`. **MUST NOT** install pnpm through npm (`npm i -g pnpm`).
- If lockfile conflicts arise during merge/rebase, **MUST** resolve by regenerating: delete `pnpm-lock.yaml`, run `pnpm install`, and commit the regenerated lockfile.

---

## 7. TRAE IDE-Specific Conventions

- **MUST** run all package management commands through the integrated terminal. Use `pnpm` directly — never invoke `npm` or `yarn`.
- When TRAE suggests a dependency installation, **MUST** respond with the `pnpm add <pkg> --save-exact` equivalent.
- When TRAE is asked to scaffold a new file, **MUST NOT** create files outside the existing project structure unless explicitly approved.
