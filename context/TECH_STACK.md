---
DATE: 2026-07-15
STATUS: CANONICAL
---

# honeybee-ph — Tech Stack

## Runtime targets

- **IronPython 2.7** — the Rhino/Grasshopper runtime. Shipping code *must* load and run here. This constrains the language features you may use (see `CODING_STANDARDS.md`).
- **CPython ≥ 3.10** — the pip/PyPI and test/CI environment. `requires-python = ">=3.10"`.

Code is written to the intersection of both.

## Dependencies

Runtime (`pyproject.toml [project] dependencies`):

- `honeybee-core` — base Honeybee objects this package extends.
- `honeybee-energy` — energy objects `honeybee_energy_ph` / `honeybee_phhvac` extend.
- `PH-units` — unit parsing and IP↔SI conversion.

Dev extras (`[project.optional-dependencies] dev`): `black`, `coverage`, `pytest`, `pytest-cov`, plus the Grasshopper/Rhino type stubs (`Grasshopper-stubs`, `Rhino-stubs`, `GH-IO-stubs`, `GH-Util-stubs`).

## Packaging

- Build backend: **setuptools** (`setuptools>=68`, `wheel`).
- Packages discovered via `[tool.setuptools.packages.find]` (the five `honeybee_*` packages; `tests`, `docs`, `diagrams` excluded).
- `honeybee_ph_standards` ships its JSON via `[tool.setuptools.package-data]`.
- Published to PyPI as **`honeybee-ph`**.

## Testing

- **pytest** — `python3 -m pytest`.
- Coverage via `coverage` / `pytest-cov`; **`fail_under = 100`** — 100% coverage is the standard.
- `filterwarnings = ["error", ...]` — warnings are errors in the test suite.
- HTML coverage report → `_coverage_html/` (gitignored).
- Tests live under `tests/`, mirroring the package layout (`test_honeybee_ph/`, `test_honeybee_phhvac/`, etc.).

## Formatting & style

- **Black**, `line-length = 120`.

## Versioning & release

- Managed by **`bump-my-version`** (`[tool.bumpversion]`). Current version lives in `pyproject.toml` → `[project] version`.
- A version bump also rewrites the version pill in `docs/index.md` (see the `[[tool.bumpversion.files]]` entries) — that is why `docs/index.md` carries the version string.
- Tags: `v{version}`. Bump commits use `[skip ci]`.

## CI

- `.github/workflows/ci.yml` — pytest + build.
- `.github/workflows/notify-hub.yml` — notifies the ph-docs hub when docs change (triggers a docs-site rebuild).
- `.github/workflows/notify-schema-repo.yml` — notifies the schema repo.

## Docs

- `docs/` is a **spoke** in the ph-docs Astro hub (docs.passivehousetools.com). API reference is generated from source docstrings at build time; `docs/nav.yml` defines the sidebar. See `docs/.instructions.md`. Do not restructure `docs/` locally.
