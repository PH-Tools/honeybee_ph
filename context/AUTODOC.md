# Feature Spec: Automated API Documentation Generator

**Status**: Proposed  
**Scope**: `ph-docs` hub + spoke docstring conventions (honeybee-ph, PHX, honeybee-REVIVE)  
**Author**: Ed May + Claude  
**Date**: 2026-04-20

---

## 1. Goal

Generate developer-friendly API reference documentation for PH-Tools Python libraries automatically from source code. The output integrates natively with the existing hub-and-spoke Astro documentation site — no parallel build systems, no new dependencies for spoke repos.

### What We Want

- Navigable API reference for the core data model classes
- Public attributes with types and descriptions
- Public methods with signatures and brief descriptions
- Class hierarchy (inheritance)
- Automatic updates when source code changes
- Searchable via Pagefind (existing infrastructure)

### What We Don't Want

- Documenting every private method and internal helper
- Documenting boilerplate (`to_dict`, `from_dict`, `duplicate`, `__copy__`, `__str__`, `__repr__`, `ToString`)
- A separate docs site or build tool (no Sphinx, no MkDocs)
- Any changes to runtime dependencies in spoke repos
- Any Python 3.x-only syntax in spoke source code

---

## 2. Critical Constraint: Python 2.7 / IronPython Compatibility

All three spoke libraries (honeybee-ph, PHX, honeybee-REVIVE) **MUST remain Python 2.7 compatible** because they run inside the IronPython 2.7 interpreter in Rhino/Grasshopper. This means:

- **NO** modern type annotations in function signatures (`def foo(x: int) -> str:`)
- **NO** f-strings, walrus operators, dataclasses, or any Python 3.x syntax
- Type hints are expressed as **mypy `# type:` comments** (PEP 484 type comments)
- The `typing` module is imported inside a `try/except ImportError` block

```python
try:
    from typing import Any, Dict, List, Optional, Union
except ImportError:
    pass  # IronPython 2.7
```

**The generator script itself runs in Python 3.x** (in the hub's CI environment). It parses Python 2.7-compatible source files using Python 3's `ast` module (which accepts 2.7 syntax as a subset) and extracts `# type:` comments via regex.

---

## 3. Architecture Overview

### Where It Runs

The generator runs **in the hub (`ph-docs`)** during the build pipeline, between `fetch_spokes.py` and `pnpm build`:

```
fetch_spokes.py (expanded: clones docs/ AND source packages)
       │
       ▼
generate_api_docs.py (ast-parses source → writes .md into src/content/docs/{lib}/api/)
       │
       ▼
pnpm build (Astro renders all .md including generated api/ pages)
```

### Why the Hub, Not the Spokes

1. **No import needed**: The generator uses `ast.parse()` (static analysis), not `import`. It never executes the source code, so it doesn't need IronPython, honeybee, ladybug, or any runtime dependencies.
2. **Single maintenance point**: One script, one place to fix bugs or adjust formatting.
3. **Instant iteration**: Change the output format → rebuild → see results. No package publishing cycle.
4. **Graceful degradation**: If generation fails for one module, log and skip — same as `fetch_spokes.py` does for spoke failures. The site still builds.
5. **Freshness**: Generated docs are always current because they're rebuilt from latest source on every deploy.

### What Changes in Existing Infrastructure

| Component | Change |
|-----------|--------|
| `libraries.yml` | Add `source_paths` and `autodoc` config per spoke |
| `fetch_spokes.py` | Expand sparse-checkout to include source directories |
| `build.yml` | Add `generate_api_docs.py` step between fetch and build |
| `validate.yml` | Same addition for PR checks |
| Spoke `nav.yml` | Add "API Reference" group (manually authored, points to generated paths) |

### What Does NOT Change

- Spoke source code syntax (remains Python 2.7)
- Spoke CI/CD workflows (no new deps, no new steps)
- Astro components, layouts, or page routing
- The hub's content collection config
- How Pagefind indexes content

---

## 4. Configuration Schema

### `libraries.yml` Additions

```yaml
libraries:
  - id: honeybee-ph
    repo: PH-Tools/honeybee_ph
    label: Honeybee-PH
    docs_path: docs/
    branch: main
    enabled: true
    # ... existing fields ...

    # NEW: Source packages to clone for API doc generation
    source_paths:
      - honeybee_ph
      - honeybee_phhvac

    # NEW: Autodoc configuration
    autodoc:
      enabled: true
      # Modules to exclude entirely (relative to source_paths)
      exclude_modules:
        - "honeybee_ph/cli"
        - "honeybee_ph/properties"
        - "honeybee_phhvac/properties"
      # Filename patterns to exclude
      exclude_patterns:
        - "_*"           # Private modules (except _base.py — see include_patterns)
        - "test_*"
      # Override: include despite matching exclude_patterns
      include_patterns:
        - "_base.py"     # Base classes are public API
      # Methods to never document (boilerplate present on every class)
      skip_methods:
        - "to_dict"
        - "from_dict"
        - "duplicate"
        - "__copy__"
        - "__str__"
        - "__repr__"
        - "__hash__"
        - "ToString"
      # Output directory (relative to assembled docs location)
      output_dir: "api"
```

### Per-Spoke Autodoc Defaults

If `autodoc` is omitted but `source_paths` is present, the generator uses sensible defaults:
- `enabled: true`
- `exclude_patterns: ["_*", "test_*"]`
- `include_patterns: ["_base.py"]`
- `skip_methods: ["to_dict", "from_dict", "duplicate", "__copy__", "__str__", "__repr__", "__hash__", "ToString"]`
- `output_dir: "api"`

---

## 5. Generator Script: `scripts/generate_api_docs.py`

### Input

- `libraries.yml` (for configuration)
- Source files cloned into a temporary location by `fetch_spokes.py`

### Output

- Markdown files written to `src/content/docs/{lib-id}/api/`
- One `.md` file per source module (e.g., `space.md`, `foundations.md`)
- A `_nav_fragment.yml` file listing all generated pages (for manual integration into spoke `nav.yml`)

### Processing Pipeline (per library)

```
1. Read autodoc config from libraries.yml
2. For each source_path:
   a. Walk directory, filter by exclude/include patterns
   b. For each .py file:
      i.   Read raw source text
      ii.  ast.parse() → extract class definitions, method definitions, properties
      iii. Regex scan → extract # type: comments from source lines
      iv.  Merge AST info + type comments + docstrings → structured data
      v.   Filter: skip private methods, skip configured skip_methods
      vi.  Render structured data → markdown
   c. Write .md file to output_dir
3. Write _nav_fragment.yml (list of generated files for reference)
4. Log summary: N modules processed, M classes documented, K skipped
```

### What Gets Extracted Per Class

| Element | Source | Required? |
|---------|--------|-----------|
| Class name | `ast.ClassDef.name` | Yes |
| Module path | File path relative to source_path | Yes |
| Base classes | `ast.ClassDef.bases` | Yes |
| Class docstring | `ast.get_docstring(node)` | No (generates stub if missing) |
| Constructor args | `ast.FunctionDef('__init__').args` | Yes |
| Constructor `# type:` | Regex on `__init__` source lines | If present |
| Instance attributes | Assignments in `__init__` body (`self.x = ...`) | Yes |
| Attribute types | Inline `# type:` comments on assignment lines | If present |
| Attribute docstrings | From class docstring `Attributes:` section | If present |
| Properties | `@property` decorated methods | Yes |
| Property return type | `# type: () -> X` on first line of property body | If present |
| Property docstring | `ast.get_docstring(property_node)` | If present |
| Public methods | Non-`_` prefixed, not in `skip_methods` | Yes |
| Method signature | `ast.FunctionDef.args` (excluding `self`/`cls`) | Yes |
| Method `# type:` | Regex on first line(s) of method body | If present |
| Method docstring | `ast.get_docstring(method_node)` | If present |
| Class methods | `@classmethod` decorated | Yes |
| Static methods | `@staticmethod` decorated | Yes |

### What Gets Skipped

- **Private classes**: Names starting with `_` (except `_Base` classes via `include_patterns`)
- **Private methods**: Names starting with `_` (except `__init__`)
- **Configured skip methods**: `to_dict`, `from_dict`, `duplicate`, etc.
- **Dunder methods**: All `__x__` methods (except `__init__` for argument extraction)
- **Excluded modules**: Entire files matching `exclude_modules` or `exclude_patterns`
- **Nested classes**: Classes defined inside methods (rare, but skip them)
- **Module-level functions**: Only document classes (functions are rarely part of the public API in these libraries)

### Parsing `# type:` Comments

The `# type:` comments follow mypy's Python 2.7 conventions:

```python
# Method type comment (on line after def):
def add_floor_segment(self, segment):
    # type: (SpaceFloorSegment) -> None

# Property type comment:
@property
def weighted_floor_area(self):
    # type: () -> float

# Inline attribute type comment:
self.geometry = None  # type: Optional[LBFace3D]
self.weighting_factor = 1.0  # (no comment = infer float from literal)

# Multi-arg method:
def to_dict(self, include_mesh=False, *args, **kwargs):
    # type: (bool, list, dict) -> Dict[str, Any]
```

**Parsing rules:**

1. For methods/properties: Look for `# type:` on the line immediately following the `def` line (inside the function body, before the docstring or first statement).
2. For attributes: Look for `# type:` at the end of the assignment line.
3. The type comment for methods follows the pattern: `# type: (ArgType1, ArgType2, ...) -> ReturnType`
   - The arg types correspond positionally to the function args **excluding `self`/`cls`**.
   - `*args` and `**kwargs` types are included positionally.
4. If no `# type:` comment exists, the type is "unknown" — the generator should still document the element, just without type info.

### Type Inference from Literals (Fallback)

When no `# type:` comment exists on an attribute, infer from the assigned value:

| Value | Inferred Type |
|-------|---------------|
| `0.0`, `1.0`, `2.5` | `float` |
| `0`, `1`, `2` | `int` |
| `""`, `"string"` | `str` |
| `True`, `False` | `bool` |
| `None` | `Optional[unknown]` |
| `[]` | `List` |
| `{}` | `Dict` |
| `ClassName()` | `ClassName` |

---

## 6. Output Format: Generated Markdown

Each generated `.md` file documents one source module. Here is the target format:

### File: `src/content/docs/honeybee-ph/api/foundations.md`

```markdown
---
title: "foundations"
card_title: API Reference
card_description: "Auto-generated reference for the honeybee-ph public API."
card_index: "99"
---

# foundations

PH Foundation Objects.

**Source**: `honeybee_ph/foundations.py`

---

## PhFoundation

Base class for all foundation types.

**Inherits from**: `_Base`

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `foundation_type` | `PhFoundationType` | The foundation classification. Default: `"5-NONE"`. |

---

## PhHeatedBasement

Heated basement foundation.

**Inherits from**: `PhFoundation`

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `floor_slab_area_m2` | `float` | Floor slab area in square meters. |
| `floor_slab_u_value` | `float` | Floor slab U-value in W/(m²K). |
| `floor_slab_exposed_perimeter_m` | `float` | Exposed perimeter length in meters. |
| `slab_depth_below_grade_m` | `float` | Depth of slab below grade in meters. |
| `basement_wall_u_value` | `float` | Basement wall U-value in W/(m²K). |

---

## PhSlabOnGrade

Slab-on-grade foundation.

**Inherits from**: `PhFoundation`

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `floor_slab_area_m2` | `float` | Floor slab area in square meters. |
| `floor_slab_u_value` | `Optional[float]` | Floor slab U-value. `None` if not set. |
| `floor_slab_exposed_perimeter_m` | `float` | Exposed perimeter length in meters. |
| `perim_insulation_position` | `PhSlabEdgeInsulationPosition` | Edge insulation orientation. |
| `perim_insulation_width_or_depth_m` | `float` | Insulation width or depth in meters. |
| `perim_insulation_thickness_m` | `float` | Insulation thickness in meters. |
| `perim_insulation_conductivity` | `float` | Insulation thermal conductivity in W/(mK). |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `perim_insulation_position` | `PhSlabEdgeInsulationPosition` | Get or set the perimeter insulation position. |

---

## PhFoundationFactory

Factory class to build any PhFoundation from an input dictionary.

### Class Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type_map` | `Dict[str, type]` | Maps foundation type strings to classes. |

---

## Enumerations

### PhFoundationType

**Inherits from**: `CustomEnum`

| Value | Meaning |
|-------|---------|
| `"1-HEATED_BASEMENT"` | Heated basement |
| `"2-UNHEATED_BASEMENT"` | Unheated basement |
| `"3-SLAB_ON_GRADE"` | Slab on grade |
| `"4-VENTED_CRAWLSPACE"` | Vented crawlspace |
| `"5-NONE"` | No foundation modeled |

### PhSlabEdgeInsulationPosition

**Inherits from**: `CustomEnum`

| Value | Meaning |
|-------|---------|
| `"1-UNDEFINED"` | Undefined |
| `"2-HORIZONTAL"` | Horizontal insulation |
| `"3-VERTICAL"` | Vertical insulation |
```

### Format Principles

1. **One file per source module** — keeps pages focused and nav manageable.
2. **Classes as H2** — each class is a major section on the page.
3. **Tables for attributes/properties** — scannable, compact.
4. **Enums get a values table** — shows allowed values and meanings.
5. **No method signature noise** — skip boilerplate methods entirely.
6. **Source path shown** — developers can find the actual code.
7. **Inheritance shown** — developers understand the class hierarchy.
8. **Front-matter on first file only** — for the feature grid card on the library landing page.

### When a Class Has Public Methods (Beyond Boilerplate)

```markdown
## Space

A Passive House Space representing an occupiable floor area.

**Inherits from**: `_Base`

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `geometry` | `Optional[LBFace3D]` | The 3D geometry of the space. |
| `weighting_factor` | `float` | Area weighting factor (iCFA/TFA). Default: `1.0`. |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `weighted_floor_area` | `float` | Floor area weighted by reduction factors. |
| `floor_area` | `float` | Unweighted floor area. |
| `net_floor_area` | `float` | Net area of the floor segment. |

### Methods

#### add_floor_segment(segment)

Add a floor segment to this space.

| Arg | Type | Description |
|-----|------|-------------|
| `segment` | `SpaceFloorSegment` | The floor segment to add. |

**Returns**: `None`
```

---

## 7. Docstring Convention for Spoke Libraries

This section defines the **target docstring format** that spoke libraries should adopt. The generator will work with ANY docstring (including missing ones), but richer docstrings produce better documentation.

### 7.1 Python 2.7 Compatibility Rules

All code in spoke libraries MUST remain Python 2.7 / IronPython compatible:

```python
# YES — type comments (mypy PEP 484 style)
def method(self, arg1, arg2):
    # type: (str, int) -> bool

# YES — inline type comments on attributes
self.name = ""  # type: str

# NO — modern annotations (Python 3.x only, DO NOT USE)
def method(self, arg1: str, arg2: int) -> bool:  # FORBIDDEN
```

### 7.2 Module Docstring

Every module should have a one-line docstring at the top:

```python
# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH Foundation Objects."""
```

This becomes the subtitle on the generated API page.

### 7.3 Class Docstring

```python
class SpaceFloorSegment(_base._Base):
    """A single floor area polygon within a PH Space.

    Represents one contiguous floor region with its own geometry, weighting
    factor (for iCFA/TFA calculations), and net area factor. A Space contains
    one or more SpaceFloorSegments.

    Attributes:
        geometry (Optional[LBFace3D]): The planar 3D geometry of this segment.
            Set to None if geometry has not been assigned.
        weighting_factor (float): Multiplier for iCFA/TFA area calculation.
            Default: 1.0 (no reduction).
        net_area_factor (float): Multiplier for net area calculation.
            Default: 1.0 (full area counts).
        reference_point (Optional[Point3D]): Point used for testing whether
            this segment is 'inside' an HB-Room. Usually the centroid,
            but adjusted for L/U shaped segments.
    """
```

**Rules:**
- **Line 1**: One-sentence summary (what IS this thing?). Imperative/declarative.
- **Lines 2+** (optional): Extended description — when to use it, how it relates to other objects, PH-domain context.
- **`Attributes:` section**: Lists public instance attributes set in `__init__`. Each entry:
  - `name (Type): Description.` — matches Google style.
  - Multi-line descriptions indent 4 extra spaces.
  - Include default values where meaningful.
- The class docstring should NOT document methods or properties (those have their own docstrings).

### 7.4 Property Docstring

```python
@property
def weighted_floor_area(self):
    # type: () -> float
    """Floor area weighted by the iCFA/TFA reduction factor."""
    ...
```

**Rules:**
- One-line docstring is sufficient for most properties.
- The `# type: () -> ReturnType` comment provides the type (generator reads this).
- Only add multi-line docstring if the property's behavior is non-obvious.

### 7.5 Method Docstring

```python
def add_floor_segment(self, segment):
    # type: (SpaceFloorSegment) -> None
    """Add a floor segment to this space.

    The segment must have valid geometry assigned. Segments are stored
    in insertion order.

    Arguments:
    ----------
        * segment (SpaceFloorSegment): The floor segment to add.

    Returns:
    --------
        * None
    """
```

**Rules:**
- **Line 1**: One-sentence summary of what the method does (imperative mood: "Add", "Return", "Calculate").
- **Lines 2+** (optional): Additional context, constraints, side effects.
- **`Arguments:` section**: Required if the method takes arguments beyond `self`/`cls`.
  - Format: `* name (Type): Description.`
  - The `----------` underline and `*` bullets match existing honeybee-ph conventions.
- **`Returns:` section**: Required if return type is non-obvious.
  - Format: `* Type: Description.` or just `* None`
- The `# type:` comment is the **machine-readable** type source. The docstring `(Type)` annotations are the **human-readable** confirmation. Both should agree.

### 7.6 Enum/CustomEnum Docstring

```python
class PhFoundationType(enumerables.CustomEnum):
    """Classification of foundation types for PH certification.

    Values:
        1-HEATED_BASEMENT: Fully conditioned basement.
        2-UNHEATED_BASEMENT: Unconditioned basement below thermal envelope.
        3-SLAB_ON_GRADE: Foundation slab directly on soil.
        4-VENTED_CRAWLSPACE: Ventilated crawlspace below floor.
        5-NONE: No foundation modeled.
    """
    allowed = [...]
```

**Rules:**
- **Line 1**: What this enum represents.
- **`Values:` section**: Lists each allowed value and its meaning.
- The generator reads the `allowed` class attribute directly for the values table, but uses the `Values:` docstring section for human-readable descriptions.

### 7.7 Factory Class Docstring

```python
class PhFoundationFactory(object):
    """Factory class to build PhFoundation objects from dictionaries.

    Uses the `foundation_type_value` key in the input dict to determine
    which subclass to instantiate.

    Type Map:
        1-HEATED_BASEMENT: PhHeatedBasement
        2-UNHEATED_BASEMENT: PhUnheatedBasement
        3-SLAB_ON_GRADE: PhSlabOnGrade
        4-VENTED_CRAWLSPACE: PhVentedCrawlspace
        5-NONE: PhFoundation
    """
```

### 7.8 What NOT to Document

Do **not** add docstrings to:
- `to_dict()` / `from_dict()` / `duplicate()` / `__copy__()` — these are boilerplate and will be explained once in a "Conventions" page.
- `__str__` / `__repr__` / `ToString` — obvious.
- Private methods (`_foo`) — internal implementation.
- Properties that just expose a private attribute with no transformation (the attribute docstring in the class docstring is sufficient).

### 7.9 Existing vs. Target Comparison

| Element | Current State | Target State |
|---------|--------------|--------------|
| Class docstrings | Mostly missing or one-liner | Summary + Attributes section |
| Property docstrings | ~50% have one-liners | All public properties have one-liner |
| Method docstrings | Rare (only a few in properties/) | All public methods have Args/Returns |
| `# type:` comments | ~70% coverage | 100% coverage on public API |
| Enum docstrings | None | Summary + Values section |
| Module docstrings | Present (one-liners) | Present (one-liners) — no change needed |

---

## 8. Build Pipeline Integration

### 8.1 Updated `fetch_spokes.py`

The sparse-checkout command expands to include source paths:

```python
# Current:
sparse_paths = [docs_path]

# Updated:
sparse_paths = [docs_path] + source_paths  # e.g., ["docs/", "honeybee_ph", "honeybee_phhvac"]
```

Source files are cloned into a temporary working directory (NOT into `src/content/docs/`). Only the `docs/` content goes into the content directory. Source stays in the temp clone for the generator to read.

**Key change**: `fetch_spokes.py` must preserve the temp clone directory (or pass its path) so `generate_api_docs.py` can access the source files. Options:
- Write clone paths to `build_manifest.json`
- Use a predictable temp directory structure (e.g., `.cache/spokes/{lib-id}/`)
- Pass as CLI argument

**Recommended**: Use `.cache/spokes/{lib-id}/` (git-ignored) as the working directory for clones. After fetching, the structure is:

```
.cache/spokes/honeybee-ph/
├── docs/           → copied to src/content/docs/honeybee-ph/
├── honeybee_ph/    → read by generate_api_docs.py
└── honeybee_phhvac/ → read by generate_api_docs.py
```

### 8.2 New Script: `scripts/generate_api_docs.py`

Runs after `fetch_spokes.py`, before `pnpm build`:

```bash
python scripts/generate_api_docs.py
```

**Behavior:**
1. Reads `libraries.yml`
2. For each library with `autodoc.enabled: true` (or `source_paths` present):
   - Reads source from `.cache/spokes/{lib-id}/{source_path}/`
   - Generates markdown
   - Writes to `src/content/docs/{lib-id}/{output_dir}/`
3. Writes generation summary to stdout (and optionally to build_manifest)
4. **Always exits 0** — generation failures are logged, not fatal

**Error handling:**
- Missing source directory → log warning, skip library
- Unparseable .py file (syntax error) → log warning, skip file
- Missing `# type:` comment → document without type (show "—" in type column)
- Empty module (no public classes) → skip file, don't generate empty .md

### 8.3 Updated `build.yml`

```yaml
steps:
  - name: Checkout
    uses: actions/checkout@v4

  - name: Setup Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.11'

  - name: Install Python deps
    run: pip install pyyaml

  - name: Fetch spoke docs and source
    run: python scripts/fetch_spokes.py

  - name: Generate API documentation    # NEW
    run: python scripts/generate_api_docs.py

  - name: Build LLM docs
    run: python scripts/build_llm_docs.py

  - name: Build LLM navigation
    run: python scripts/build_llm_nav.py

  - name: Setup Node
    uses: actions/setup-node@v4
    # ... rest of build unchanged
```

### 8.4 Nav Integration

The generator writes API reference pages, but the spoke's `nav.yml` must reference them. Two approaches:

**Option A: Manual nav entries (recommended for now)**

The spoke's `nav.yml` includes a hand-written "API Reference" group pointing to the paths the generator will produce:

```yaml
nav:
  - Overview: index.md
  - User Guide:
    - Getting Started: guide/getting-started.md
  - API Reference:
    - space: api/space.md
    - foundations: api/foundations.md
    - bldg_segment: api/bldg_segment.md
    - hvac/ventilation: api/hvac-ventilation.md
```

**Option B: Auto-generated nav fragment**

The generator writes `_nav_fragment.yml` to the output directory. A merge step (or manual copy) integrates it into the spoke's `nav.yml`. This is more complex and can be added later.

**Recommendation**: Start with Option A. The set of modules to document is stable — it won't change every commit. When a new module is added (rare), manually add the nav entry.

### 8.5 Spoke `nav.yml` Responsibility

The spoke repo's `docs/nav.yml` is the single source of truth for navigation. It must list all API pages that the generator will produce. If a nav entry points to a file the generator didn't produce (e.g., excluded module), the Astro build will fail at static path generation.

**Safety mechanism**: The generator should write a `.generated_files` manifest listing what it produced. The hub build can optionally validate that all `api/*` nav entries have corresponding generated files.

---

## 9. Handling Enumerations (`CustomEnum` subclasses)

Honeybee-ph uses a custom enum pattern (not Python's `enum` module):

```python
class PhFoundationType(enumerables.CustomEnum):
    allowed = [
        "1-HEATED_BASEMENT",
        "2-UNHEATED_BASEMENT",
        "3-SLAB_ON_GRADE",
    ]
```

**Generator behavior:**
1. Detect classes inheriting from `CustomEnum` (or with an `allowed` class attribute that is a list of strings)
2. Extract the `allowed` list values
3. Render as a "Values" table instead of the standard attributes table
4. If the class docstring has a `Values:` section, use those descriptions; otherwise just list the raw values

---

## 10. Handling Inheritance

The generator should resolve base classes to show the inheritance chain:

```markdown
**Inherits from**: `PhFoundation` → `_Base`
```

**Rules:**
- Show the immediate parent(s) only (not the full MRO)
- If the parent is in the same module, link within the page (anchor)
- If the parent is in a different module within the same package, show as `module.ClassName`
- If the parent is external (e.g., `object`, `CustomEnum`), show the name without a link

---

## 11. File Organization

### Generated output structure

```
src/content/docs/honeybee-ph/api/
├── _index.md              # API Reference landing/overview (optional, hand-written)
├── space.md               # honeybee_ph/space.py
├── foundations.md          # honeybee_ph/foundations.py
├── bldg_segment.md        # honeybee_ph/bldg_segment.py
├── site.md                # honeybee_ph/site.py
├── team.md                # honeybee_ph/team.py
├── phi.md                 # honeybee_ph/phi.py
├── phius.md               # honeybee_ph/phius.py
└── hvac/
    ├── ventilation.md     # honeybee_phhvac/ventilation.py (or similar)
    ├── heating.md         # honeybee_phhvac/heating.py
    └── ...
```

### Mapping source paths to output paths

- `honeybee_ph/space.py` → `api/space.md`
- `honeybee_ph/foundations.py` → `api/foundations.md`
- `honeybee_phhvac/ventilation.py` → `api/hvac/ventilation.md` (subdirectory per source package after the first)

**Rule**: The first `source_path` maps directly to `api/`. Additional source paths create subdirectories named after the package (with `honeybee_` prefix stripped for readability, or configurable).

Alternative (simpler): flatten everything into `api/` with prefixed filenames:
- `honeybee_phhvac/ventilation.py` → `api/phhvac-ventilation.md`

The exact mapping should be configurable in `libraries.yml` under `autodoc`.

---

## 12. Graceful Degradation & Error Handling

| Scenario | Behavior |
|----------|----------|
| `source_paths` not configured | Skip autodoc for this library entirely |
| Source directory not found in clone | Log warning, skip this source path |
| `.py` file has syntax error | Log warning with filename, skip file |
| Class has no docstring | Generate entry with class name + "No description available." |
| Method has no `# type:` comment | Show "—" in type column |
| Method has no docstring | List method name and signature only |
| Enum has no `Values:` section in docstring | Show allowed values without descriptions |
| `nav.yml` references a file that wasn't generated | This is a spoke-side error — caught by Astro build, not the generator |
| Generator script crashes entirely | Log error, exit 0 — site builds without API docs |

**Principle**: The generator should produce the best docs it can with whatever it finds. Missing docstrings = degraded output, not build failure. This means spokes can adopt the new docstring convention incrementally — partial coverage still produces partial (but valid) docs.

---

## 13. Scope: What to Document Per Library

### honeybee-ph

**Source paths**: `honeybee_ph`, `honeybee_phhvac`

**Include (honeybee_ph/)**:
- `_base.py` — `_Base` class (foundation of all objects)
- `space.py` — `Space`, `SpaceFloorSegment`
- `bldg_segment.py` — `BldgSegment`, ventilation enums
- `foundations.py` — All foundation types + factory
- `site.py` — Climate data classes
- `team.py` — `ProjectTeam`, `ProjectTeamMember`
- `phi.py` — PHI certification settings
- `phius.py` — Phius certification settings

**Include (honeybee_phhvac/)**:
- `_base.py` — `_PhHVACBase`
- All ventilation equipment classes
- All heating equipment classes
- All cooling/DHW classes
- System-level classes

**Exclude**:
- `honeybee_ph/cli/` — CLI internals
- `honeybee_ph/properties/` — Honeybee extension wiring (internal plumbing)
- `honeybee_phhvac/properties/` — Same
- Any `_internal` or `_util` modules

### PHX (future)

**Source paths**: `PHX`

Focus on the data model classes (`PHX/model/`) and the public conversion API.

### honeybee-REVIVE (future)

**Source paths**: `honeybee_revive`

Focus on the analysis classes and result objects.

---

## 14. Testing & Validation

### Local development workflow

```bash
# Fetch spokes (including source)
python scripts/fetch_spokes.py

# Generate API docs
python scripts/generate_api_docs.py

# Build and preview
pnpm build && pnpm preview
```

### Validation checks (in `validate.yml`)

1. Generator exits 0
2. At least one `.md` file was produced per configured library
3. `pnpm build` succeeds (Astro can resolve all nav entries)

### Debugging

- Generator should support a `--verbose` flag for detailed per-file/per-class logging
- Generator should support `--library honeybee-ph` to process only one library
- Generator should support `--dry-run` to print what would be generated without writing files

---

## 15. Future Enhancements (Out of Scope for v1)

- **Cross-references**: Link type names to their definition pages (e.g., `SpaceFloorSegment` in a type column links to `api/space.md#spaceFloorsegment`)
- **Changelog integration**: Show "Added in v1.2.0" badges from git history
- **Search weighting**: Boost API reference pages in Pagefind results
- **Auto-nav generation**: Fully generate the API Reference section of `nav.yml` instead of manual maintenance
- **Inheritance resolution**: Show inherited attributes/methods from parent classes
- **Usage examples**: Extract code examples from test files that exercise the class

---

## 16. Implementation Sequence

1. **Update `fetch_spokes.py`** — expand sparse-checkout to clone source paths into `.cache/spokes/`
2. **Write `generate_api_docs.py`** — core parser + renderer, tested against `honeybee_ph/foundations.py` as first module
3. **Iterate on output format** — generate for all honeybee-ph modules, review, adjust
4. **Update `libraries.yml`** — add `source_paths` and `autodoc` config for honeybee-ph
5. **Update honeybee-ph `nav.yml`** — add API Reference group with entries for generated pages
6. **Update `build.yml` and `validate.yml`** — add generator step
7. **Deploy and verify** — full pipeline test
8. **Begin spoke docstring upgrades** — incremental, class by class (this is the ongoing work)
9. **Extend to PHX and honeybee-REVIVE** — add config, add nav entries, begin docstring work

---

## 17. Summary for Spoke Library Agents

If you are an agent working on a spoke library (honeybee-ph, PHX, or honeybee-REVIVE), here is what you need to do:

### You have two jobs:

1. **Upgrade docstrings** in the Python source code (the bulk of the work)
2. **Add an "API Reference" group to `docs/nav.yml`** so the generated pages appear in navigation

### You do NOT need to:
- Install any new dependencies
- Change any CI/CD workflows
- Write any build scripts
- Change any Python syntax (everything stays Python 2.7 compatible)

---

### Job 1: Update `docs/nav.yml`

Add an "API Reference" top-level group to your spoke's `docs/nav.yml`. The entries must match the files that the hub generator will produce. Each entry maps a label to a path under `api/`.

**Important**: If `nav.yml` references a file the generator didn't produce, the Astro build will fail. Only list modules that exist and contain at least one public class. When in doubt, leave an entry out — the page will still be searchable, just not in the sidebar.

#### honeybee-ph `nav.yml` entries

Add this group to `docs/nav.yml` (after existing groups):

```yaml
  - API Reference:
    - _base: api/_base.md
    - bldg_segment: api/bldg_segment.md
    - foundations: api/foundations.md
    - phi: api/phi.md
    - phius: api/phius.md
    - site: api/site.md
    - space: api/space.md
    - team: api/team.md
    - ducting: api/hvac/ducting.md
    - heat_pumps: api/hvac/heat_pumps.md
    - heating: api/hvac/heating.md
    - hot_water_devices: api/hvac/hot_water_devices.md
    - hot_water_piping: api/hvac/hot_water_piping.md
    - hot_water_system: api/hvac/hot_water_system.md
    - renewable_devices: api/hvac/renewable_devices.md
    - supportive_device: api/hvac/supportive_device.md
    - ventilation: api/hvac/ventilation.md
```

These paths correspond 1:1 to the source modules the generator processes:
- `api/*.md` → files from `honeybee_ph/` (first `source_path`)
- `api/hvac/*.md` → files from `honeybee_phhvac/` (second `source_path`, common prefix stripped → `hvac/`)

---

### Job 2: Upgrade Docstrings

#### Docstring format to follow:
- **Section 7** of this document defines the exact format
- Use Google-style `Attributes:`, `Arguments:`, `Returns:`, `Values:` sections
- Keep `# type:` comments — add them where missing
- Class docstrings should have a summary line + `Attributes:` section
- Property docstrings should be one-liners
- Method docstrings should have summary + `Arguments:` + `Returns:`
- Enum/CustomEnum classes should have a `Values:` section

#### What to document:
- All public classes (not prefixed with `_`, except `_Base` classes)
- All public properties
- All public methods (not prefixed with `_`)
- Skip: `to_dict`, `from_dict`, `duplicate`, `__copy__`, `__str__`, `__repr__`, `__hash__`, `ToString`

#### Priority order:
1. Core data model classes (the ones developers instantiate and interact with)
2. Enum/CustomEnum classes (developers need to know allowed values)
3. Factory classes
4. HVAC equipment classes
5. Utility/helper classes (lowest priority)

#### Example transformation:

**Before:**
```python
class SpaceFloorSegment(_base._Base):
    def __init__(self):
        super(SpaceFloorSegment, self).__init__()
        self.geometry = None  # type: Optional[LBFace3D]
        self.weighting_factor = 1.0
        self.net_area_factor = 1.0
        self.reference_point = None  # type: Optional[Point3D]
```

**After:**
```python
class SpaceFloorSegment(_base._Base):
    """A single floor area polygon within a PH Space.

    Represents one contiguous floor region with its own geometry, weighting
    factor (for iCFA/TFA calculations), and net area factor. A Space contains
    one or more SpaceFloorSegments.

    Attributes:
        geometry (Optional[LBFace3D]): The planar 3D face geometry of this
            floor segment. None if not yet assigned.
        weighting_factor (float): Multiplier for iCFA/TFA area calculation.
            Default: 1.0 (no reduction).
        net_area_factor (float): Multiplier for net usable area calculation.
            Default: 1.0 (full area counts).
        reference_point (Optional[Point3D]): Point used for spatial containment
            testing (is this segment inside an HB-Room?). Usually the face
            centroid, but adjusted for non-convex shapes (L, U).
    """

    def __init__(self):
        super(SpaceFloorSegment, self).__init__()
        self.geometry = None  # type: Optional[LBFace3D]
        self.weighting_factor = 1.0  # type: float
        self.net_area_factor = 1.0  # type: float
        self.reference_point = None  # type: Optional[Point3D]
```

Note: The `# type:` comments on `weighting_factor` and `net_area_factor` are optional (the generator can infer `float` from the literal), but including them is good practice for consistency.
