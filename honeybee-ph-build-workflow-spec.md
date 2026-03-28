# Honeybee-PH: Build & Deployment Workflow Spec

**Date:** 2026-03-28
**Purpose:** Document the current state of all repos, their build/deploy pipelines, dependency relationships, and manual steps — as a foundation for simplification.

---

## 1. Repository Overview

There are **6 repositories** in the honeybee-ph ecosystem, falling into three tiers:

| Repo | Type | Location | PyPI Package | Versioning |
|------|------|----------|-------------|------------|
| `PH_units` | Python library | `00_PH_Tools/PH_units` | `PH-units` (v1.5.28) | semantic-release (auto) |
| `honeybee_ph` | Python library | `00_PH_Tools/honeybee_ph` | `honeybee-ph` (v1.32.0) | semantic-release (auto) |
| `PHX` | Python library | `00_PH_Tools/PHX` | `phx` (v1.55.1) | semantic-release (auto) |
| `honeybee_ref` | Python library | `00_PH_Tools/honeybee_ref` | `honeybee-ref` (v0.2.01) | manual (pyproject.toml) |
| `PH_GH_Component_IO` | GH utility lib | `00_PH_Tools/PH_GH_Component_IO` | — (GitHub download) | manual (pyproject.toml) |
| `honeybee_grasshopper_ph` | GH components | `00_PH_Tools/honeybee_grasshopper_ph` | — (not on PyPI) | manual (`_component_info_.py`) |
| `honeybee_grasshopper_ph_plus` | GH components | `00_PH_Tools/honeybee_grasshopper_ph_plus` | — (not on PyPI) | manual (`_component_info_.py`) |

---

## 2. Dependency Graph

```
PH_units  (no internal deps)
    ↑
honeybee_ph  (depends on: PH_units, honeybee-core, honeybee-energy)
    ↑
PHX  (depends on: honeybee_ph, PH_units, honeybee-core, honeybee-energy, pydantic, xlwings, lxml)

honeybee_ref  (depends on: honeybee-energy)

PH_GH_Component_IO  (standalone GH utility, no internal deps)

honeybee_grasshopper_ph  (depends on: honeybee_ph, PHX, PH_units, PH_GH_Component_IO, honeybee-core, honeybee-energy, ladybug-rhino)
honeybee_grasshopper_ph_plus  (depends on: honeybee_ph, PHX, PH_units, PH_GH_Component_IO, honeybee-core, honeybee-energy, ladybug-rhino)
```

**Key observation:** There is a clear dependency chain: `PH_units → honeybee_ph → PHX`, and the two Grasshopper repos depend on all three. `honeybee_ref` is relatively independent.

---

## 3. Tier 1: Python Libraries (PyPI packages)

### 3.1 Common Build Setup (PH_units, honeybee_ph, PHX)

All three share an essentially identical build/deploy pipeline:

**Build system:** Old-style `setup.py` + `setup.cfg` + `setuptools_scm`
- `setup.py` uses `use_scm_version=True` (version from git tags)
- `setup.cfg` contains package metadata, `[semantic_release]` section pointing to `__init__.py:__version__`
- `pyproject.toml` contains only tool config (pytest, coverage, black, ruff) — NOT build config
- `MANIFEST.in` for sdist inclusion/exclusion rules
- `deploy.sh` runs `python setup.py sdist bdist_wheel && twine upload`

**CI/CD (GitHub Actions — `ci.yaml`):**
1. **Test job:** checkout → setup Python 3.10.14 → install deps → `pytest tests/`
2. **Deploy job** (main branch only, owner=ph-tools):
   - Setup Python 3.10.14 + Node.js 22.2.0
   - `npm install @semantic-release/exec`
   - `npx semantic-release@^23.1.1` (dry-run to get version, then real run)
   - semantic-release calls `deploy.sh ${nextRelease.version}`
   - Environment secrets: `GITHUB_TOKEN`, `PYPI_USERNAME`, `PYPI_PASSWORD`

**Semantic release config (`.releaserc.json`):**
```json
{
  "branches": [{"name": "main", "prerelease": false}],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/github",
    ["@semantic-release/exec", {"publishCmd": "bash deploy.sh ${nextRelease.version}"}]
  ]
}
```

**Version flow:** Conventional commit → semantic-release determines bump → creates git tag → `deploy.sh` builds & uploads to PyPI → GitHub Release created.

### 3.2 honeybee_ref (the outlier)

This repo has already been partially modernized:
- Uses `pyproject.toml` as the **primary build config** (not setup.py)
- Version is a **static string** in `pyproject.toml`: `version = "0.2.01"`
- **No semantic-release** — version bumped manually
- CI triggers on **Release publication** (not on push to main)
- Uses `python -m build` (modern) instead of `python setup.py sdist bdist_wheel`
- Uses **OIDC trusted publishing** to PyPI (no username/password secrets needed)
- Separate `tests.yaml` workflow for running tests on all pushes

---

## 4. Tier 2: Grasshopper Component Repos

### 4.1 honeybee_grasshopper_ph

**Structure:**
- `honeybee_grasshopper_ph/src/` — 95 Python source files (GHPython component code)
- `honeybee_grasshopper_ph/user_objects/` — 106 compiled `.ghuser` files
- `honeybee_ph_rhino/` — Worker classes and Rhino-specific IO (104+ files)
- `honeybee_ph_rhino/_component_info_.py` — Central component registry with `RELEASE_VERSION = "Honeybee-PH v1.17.03"`

**Version management:** Manual edit of `RELEASE_VERSION` string in `_component_info_.py`.

**Component packaging workflow (manual, run from inside Grasshopper):**
1. Open Grasshopper
2. Run `__HBPH__Util_Update_GHCompos.py` utility script
3. Script loads all HBPH UserObjects from Grasshopper's app directory
4. Extracts Python code → saves to `src/*.py`
5. Copies `.ghuser` files → saves to `user_objects/*.ghuser`
6. Paths are **hardcoded** to Ed's machine (`/Users/em/...`)

**CI/CD:** Only a Hugo docs deployment workflow (`hugo.yml`). **No test or release automation.**

**Installer:** `hbph_installer.ghx` (76 KB) — a Grasshopper file users open to install everything. Contains hardcoded version numbers that must be manually updated.

### 4.2 honeybee_grasshopper_ph_plus

**Structure:** Similar pattern to `honeybee_grasshopper_ph`:
- 54 component `.py` source files + 54 `.ghuser` files
- `honeybee_ph_plus_rhino/_component_info_.py` with `RELEASE_VERSION = "Honeybee-PH+ v1.06.03"`

**CI/CD:** **None.** No GitHub Actions workflows at all.

**Version management:** Manual edit of `RELEASE_VERSION` in `_component_info_.py`.

---

## 5. Tier 3: The Installer

**File:** `honeybee_grasshopper_ph/hbph_installer.ghx`

This Grasshopper file is the user-facing installation mechanism. When a user opens and runs it, it:
1. `pip install`s all required Python packages (honeybee-ph, PHX, PH-units, honeybee-ref) into the **ladybug-tools Python interpreter** (not the standard Rhino interpreter)
2. Downloads `.ghuser` component files from GitHub
3. Copies `.ghuser` files into the appropriate Rhino/Grasshopper UserObjects directory

**Manual update required:** Every time a library version changes, the installer file must be manually updated with the new version numbers.

---

## 6. Current Release Workflow (End-to-End)

Here is the full sequence of manual steps Ed must perform to release an update:

### Step 1: Update a Python library
1. Make code changes in e.g. `PHX`
2. Commit with conventional message (`feat:`, `fix:`, etc.)
3. Push to `main`
4. **Wait** for GitHub Actions to run semantic-release
5. **Wait** for PyPI upload to succeed
6. **Verify** new version is live on PyPI

### Step 2: Update downstream dependencies (if needed)
7. If `honeybee_ph` changed, update `PHX/requirements.txt` with new version
8. If `PH_units` changed, update both `honeybee_ph/requirements.txt` and `PHX/requirements.txt`
9. Commit, push, wait for each downstream repo's CI/CD to complete

### Step 3: Update Grasshopper components
10. If component behavior changed, edit components in Grasshopper
11. Run `__HBPH__Util_Update_GHCompos.py` from inside Grasshopper to export `.ghuser` and `.py` files
12. Manually edit `RELEASE_VERSION` in `_component_info_.py`
13. Commit and push to GitHub
14. Create a GitHub **Release** manually

### Step 4: Update the installer
15. Open `hbph_installer.ghx` in Grasshopper
16. Manually update version numbers for all changed packages
17. Commit and push

**Total manual steps for a typical cross-cutting change: 15–17 steps, with multiple wait-and-verify cycles.**

---

## 7. Identified Pain Points

### Build system inconsistencies
- Three repos use old-style `setup.py` + `setup.cfg`; one uses modern `pyproject.toml`
- `deploy.sh` uses deprecated `python setup.py sdist bdist_wheel` (setuptools warns about this)
- `twine upload` with username/password vs. OIDC trusted publishing (honeybee_ref)
- Python 2.7 still listed in classifiers (misleading — these run on 3.10+)

### Version management fragmentation
- PyPI libs: semantic-release (auto) from conventional commits
- honeybee_ref: manual version in pyproject.toml
- Grasshopper repos: manual version in `_component_info_.py`
- Installer: manual version numbers embedded in `.ghx` file

### Manual coordination overhead
- Cascading dependency updates must be done repo-by-repo
- No way to atomically release a coordinated update across all repos
- Easy to forget a step or get versions out of sync
- The installer is a particularly fragile manual bottleneck

### Missing automation
- Grasshopper repos have no CI/CD for testing or releases
- No automated validation that version numbers are consistent across repos
- No automated way to trigger downstream rebuilds when an upstream dep changes
- Component export utility has hardcoded paths

### Deployment complexity
- Node.js is required in CI solely for semantic-release (a JavaScript tool)
- Each repo independently installs semantic-release on every CI run
- The `deploy.sh` pattern is duplicated across three repos identically

---

## 8. What's Working Well

- The **facade/worker architecture** in the Grasshopper repos (separation of GH UI from business logic) is solid and enables independent testing
- **semantic-release** on the PyPI libraries does successfully automate version bumps and releases
- The **dependency chain** is clean and well-defined (no circular deps)
- **honeybee_ref** already demonstrates a modernized approach (pyproject.toml, OIDC publishing, `python -m build`)
- Test coverage requirements (100% on honeybee_ph and PHX) enforce quality

---

## 9. Design Decisions (Agreed)

Before detailing the proposal, here are the decisions made during discussion:

1. **Versioning approach:** `bump-my-version` with hybrid trigger
   - Direct push to main → auto-bumps **patch**
   - PR merge with `bump:minor` or `bump:major` label → bumps accordingly
   - PR merge with no label → defaults to **patch**
   - No more Node.js / npm semantic-release in CI

2. **Build system:** Modernize all repos to `pyproject.toml` (following the `honeybee_ref` pattern)
   - Remove `setup.py`, `setup.cfg`, `deploy.sh`, `.releaserc.json`, `MANIFEST.in`
   - Use `python -m build` for packaging
   - Use **OIDC trusted publishing** to PyPI (no more username/password secrets)

3. **Installer format:** Use `.ghx` (XML) so version numbers can be updated programmatically

4. **Release orchestrator:** A manually-triggered GitHub Action in `honeybee_grasshopper_ph` that syncs all downstream versions and creates the user-facing release

5. **Python 2.7 compatibility:** Must be maintained in library code (for Rhino/GH IronPython runtime) but build tooling targets Python 3.10+

6. **`honeybee_grasshopper_ph_plus`:** Align its CI/CD with `honeybee_grasshopper_ph`

---

## 10. Proposed Architecture

### 10.1 Per-Repo CI/CD: PyPI Libraries (PH_units, honeybee_ph, PHX, honeybee_ref)

All four libraries will follow the same standardized pattern:

#### Files to ADD in each repo:

**`pyproject.toml`** (replaces setup.py + setup.cfg as the single source of truth):
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "honeybee-ph"  # (repo-specific)
version = "1.32.0"    # (repo-specific — managed by bump-my-version)
description = "Plugin for Honeybee to enable Passive House modeling."
readme = "README.md"
license = "GPL-3.0-or-later"
requires-python = ">=2.7"
authors = [{name = "PH-Tools", email = "phtools@bldgtyp.com"}]
dependencies = [
    "honeybee-core>=1.64.9",
    "honeybee-energy>=1.116.103",
    "PH-units>=1.5.26",
]

[project.optional-dependencies]
dev = [
    "black",
    "coverage",
    "pytest",
    "pytest-cov",
    "ruff",
]

[tool.setuptools.packages.find]
include = ["honeybee_ph*", "honeybee_energy_ph*", "honeybee_ph_standards*",
           "honeybee_ph_utils*", "honeybee_phhvac*"]
exclude = ["tests*", "docs*", "diagrams*"]

[tool.bump-my-version]
current_version = "1.32.0"
commit = true
tag = true
tag_name = "v{new_version}"

[[tool.bump-my-version.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

# ... existing tool config (pytest, coverage, black, ruff) stays here ...
```

**`.github/workflows/ci.yml`** (replaces current ci.yaml):
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: write  # needed for bump-my-version to push tags

jobs:
  test:
    name: Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - run: pip install '.[dev]'
      - run: python -m pytest tests/

  bump-and-release:
    name: Bump version and publish
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: pypi          # GitHub environment with OIDC trust
    permissions:
      contents: write          # push version commit + tag
      id-token: write          # OIDC token for PyPI
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - run: pip install bump-my-version build

      # Determine bump level from PR labels (if merged PR) or default to patch
      - name: Determine version bump
        id: bump_level
        uses: actions/github-script@v7
        with:
          script: |
            // Check if this push is a merged PR
            const commits = context.payload.commits || [];
            const mergeCommit = commits.find(c => c.message.startsWith('Merge pull request'));
            if (mergeCommit) {
              // Extract PR number and check labels
              const match = mergeCommit.message.match(/#(\d+)/);
              if (match) {
                const pr = await github.rest.pulls.get({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  pull_number: parseInt(match[1])
                });
                const labels = pr.data.labels.map(l => l.name);
                if (labels.includes('bump:major')) return core.setOutput('level', 'major');
                if (labels.includes('bump:minor')) return core.setOutput('level', 'minor');
              }
            }
            core.setOutput('level', 'patch');

      - name: Bump version
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          bump-my-version bump ${{ steps.bump_level.outputs.level }}

      - name: Push version commit and tag
        run: git push --follow-tags

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # No credentials needed — uses OIDC trusted publishing
```

#### Files to REMOVE from each repo:
- `setup.py`
- `setup.cfg`
- `deploy.sh`
- `.releaserc.json`
- `MANIFEST.in` (setuptools reads includes/excludes from pyproject.toml)

#### One-time setup per repo:
- Configure **OIDC trusted publishing** on PyPI (no secrets to manage)
- Create a `pypi` GitHub environment (for the OIDC trust)
- Create GitHub labels: `bump:minor`, `bump:major`

---

### 10.2 Grasshopper Component Repos (honeybee_grasshopper_ph, honeybee_grasshopper_ph_plus)

These repos don't publish to PyPI, but they DO need:

**`.github/workflows/tests.yml`** — Run tests on all pushes:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - run: |
          pip install -r requirements.txt
          pip install -r dev-requirements.txt
      - run: python -m pytest tests/
```

Version management for these repos is handled by the **orchestrator** (see 10.3 below), not by individual pushes. The `_component_info_.py` version gets updated as part of the release orchestration.

---

### 10.3 Release Orchestrator (in `honeybee_grasshopper_ph`)

This is the key new piece. A manually-triggered GitHub Action that coordinates a full user-facing release.

**`.github/workflows/release.yml`:**
```yaml
name: Release Honeybee-PH

on:
  workflow_dispatch:
    inputs:
      bump_level:
        description: "Version bump level for Grasshopper components"
        required: true
        type: choice
        options:
          - patch
          - minor
          - major
      ph_plus_bump_level:
        description: "Version bump for GH-PH-Plus (if changed)"
        required: false
        type: choice
        options:
          - patch
          - minor
          - major
          - skip
        default: skip

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install tools
        run: pip install bump-my-version requests

      - name: Fetch latest PyPI versions
        id: versions
        run: |
          python -c "
          import requests, json
          pkgs = {
              'honeybee-ph': 'honeybee_ph',
              'PHX': 'phx',
              'PH-units': 'ph_units',
              'honeybee-ref': 'honeybee_ref',
          }
          versions = {}
          for display_name, pypi_name in pkgs.items():
              resp = requests.get(f'https://pypi.org/pypi/{pypi_name}/json')
              versions[display_name] = resp.json()['info']['version']
              print(f'{display_name}: {versions[display_name]}')
          # Write to GitHub output
          with open('$GITHUB_OUTPUT', 'a') as f:
              for k, v in versions.items():
                  safe_key = k.replace('-', '_')
                  f.write(f'{safe_key}={v}\n')
          "

      - name: Update requirements.txt with latest versions
        run: |
          python scripts/update_requirements.py \
            --honeybee-ph=${{ steps.versions.outputs.honeybee_ph }} \
            --phx=${{ steps.versions.outputs.PHX }} \
            --ph-units=${{ steps.versions.outputs.PH_units }} \
            --honeybee-ref=${{ steps.versions.outputs.honeybee_ref }}

      - name: Bump _component_info_.py version
        run: |
          bump-my-version bump ${{ inputs.bump_level }}

      - name: Update installer .ghx with current versions
        run: |
          python scripts/update_installer_ghx.py \
            --honeybee-ph=${{ steps.versions.outputs.honeybee_ph }} \
            --phx=${{ steps.versions.outputs.PHX }} \
            --ph-units=${{ steps.versions.outputs.PH_units }} \
            --honeybee-ref=${{ steps.versions.outputs.honeybee_ref }}

      - name: Commit and tag
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "release: Honeybee-PH $(bump-my-version show current_version)"
          git push --follow-tags

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: v${{ steps.bump_level.outputs.new_version }}
          generate_release_notes: true

      # Optionally trigger honeybee_grasshopper_ph_plus release
      - name: Trigger PH-Plus release
        if: inputs.ph_plus_bump_level != 'skip'
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.PH_TOOLS_PAT }}
          repository: PH-Tools/honeybee_grasshopper_ph_plus
          event-type: release
          client-payload: '{"bump_level": "${{ inputs.ph_plus_bump_level }}"}'
```

#### Supporting scripts to create (in `honeybee_grasshopper_ph/scripts/`):

1. **`scripts/update_requirements.py`** — Updates version pins in `requirements.txt`
2. **`scripts/update_installer_ghx.py`** — Parses the `.ghx` XML and updates version strings
3. **`scripts/update_component_info.py`** — (optional, if bump-my-version can't handle the custom format in `_component_info_.py`)

---

### 10.4 Summary: New Release Workflow (End-to-End)

Here is the simplified release process:

#### For a library-only change (e.g., bug fix in PHX):
1. Push fix to `PHX/main` (or merge PR)
2. CI auto-bumps patch, deploys to PyPI → **done** (1 step for you)

#### For a cross-cutting feature:
1. Push/merge library changes (each repo auto-bumps and deploys independently)
2. Push Grasshopper component changes (commit `.ghuser` + worker code)
3. Go to `honeybee_grasshopper_ph` → Actions → "Release Honeybee-PH" → pick bump level → Run
4. Orchestrator auto-updates all versions, installer, creates GitHub Release → **done**

**Total manual steps: 3–4** (down from 15–17), with no version numbers to edit by hand.

---

### 10.5 Migration Plan

The migration can be done incrementally, repo by repo:

| Phase | Repos | Changes |
|-------|-------|---------|
| **Phase 1** | `PH_units` | Modernize to pyproject.toml, bump-my-version, OIDC publishing. Smallest repo, lowest risk. Validates the new pattern. |
| **Phase 2** | `honeybee_ph` | Same modernization. Update dependency on PH_units. |
| **Phase 3** | `PHX` | Same modernization. Update dependencies on honeybee_ph + PH_units. |
| **Phase 4** | `honeybee_ref` | Already mostly modern. Add bump-my-version, align CI with the standard pattern. |
| **Phase 5** | `honeybee_grasshopper_ph` | Add tests workflow, create orchestrator action + supporting scripts, add bump-my-version for `_component_info_.py`. |
| **Phase 6** | `honeybee_grasshopper_ph_plus` | Add tests workflow, add repository-dispatch receiver for orchestrator. |

Each phase is independently deployable. If Phase 1 works well, the remaining phases are largely copy-paste with repo-specific tweaks.

---

### 10.6 Files Changed Per Repo (Checklist)

**Note:** The TOML config section is `[tool.bumpversion]` (not `[tool.bump-my-version]`).
The CLI command is still `bump-my-version bump ...`.

#### Each PyPI library repo (PH_units, honeybee_ph, PHX, honeybee_ref):
- [x] Consolidate `setup.py` + `setup.cfg` → `pyproject.toml` (with `[tool.bumpversion]` config)
- [x] Add `.github/workflows/ci.yml` (new standardized workflow)
- [ ] Delete old files: `setup.py`, `setup.cfg`, `deploy.sh`, `.releaserc.json`, `MANIFEST.in`, `.github/workflows/ci.yaml`
- [ ] Configure OIDC trusted publishing on PyPI
- [ ] Create `pypi` GitHub environment
- [ ] Create `bump:minor` and `bump:major` labels

#### honeybee_grasshopper_ph:
- [x] Add `[tool.bumpversion]` config in `pyproject.toml` (targeting `_component_info_.py`)
- [x] Add `.github/workflows/tests.yml`
- [x] Add `.github/workflows/release.yml` (orchestrator)
- [x] Add `scripts/update_requirements.py`
- [x] Add `scripts/update_installer_ghx.py`
- [x] Add `WORKFLOW.md` (comprehensive workflow documentation)

#### honeybee_grasshopper_ph_plus:
- [x] Add `[tool.bumpversion]` config in `pyproject.toml` (targeting `_component_info_.py`)
- [x] Add `.github/workflows/tests.yml`
- [x] Add `.github/workflows/release.yml` (manual dispatch + repository_dispatch)

---

## 11. Implementation Status

All code changes have been implemented locally (2026-03-28). Before going live:

### Remaining manual steps (per repo):

| Step | Where | Notes |
|------|-------|-------|
| Delete `setup.py`, `setup.cfg`, `deploy.sh`, `.releaserc.json`, `MANIFEST.in` | PH_units, honeybee_ph, PHX | Only after verifying new CI works |
| Delete `.github/workflows/ci.yaml` | PH_units, honeybee_ph, PHX | Replaced by `ci.yml` |
| Delete `.github/workflows/ci.yaml`, `tests.yaml` | honeybee_ref | Replaced by `ci.yml` |
| Configure OIDC trusted publishing | PyPI (each package) | One-time setup per package |
| Create `pypi` GitHub environment | Each PyPI repo's Settings | One-time setup per repo |
| Create `bump:minor`, `bump:major` labels | Each PyPI repo | One-time setup per repo |

### Recommended rollout order:
1. Start with `PH_units` — push changes, verify CI works end-to-end
2. Then `honeybee_ph`, `PHX`, `honeybee_ref`
3. Finally `honeybee_grasshopper_ph` and `honeybee_grasshopper_ph_plus`
