# context/ — canonical repo documentation

Stable, ground-truth documentation for honeybee-ph: what it is, how it is built, and the rules for changing it. Distinct from `planning/` (in-flight working plans) and `docs/` (the public autodoc site published by the ph-docs hub).

`CLAUDE.md` at the repo root is the dispatcher; this folder holds the docs it routes to.

## Index

| Doc | Read when you need… |
|-----|---------------------|
| [`PRD.md`](PRD.md) | Product scope — what this library is for, who uses it, what belongs here and what does not |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | The package/module map, key abstractions, and how data flows through the ecosystem |
| [`TECH_STACK.md`](TECH_STACK.md) | Runtime, dependencies, packaging, testing, CI, and the release process |
| [`CODING_STANDARDS.md`](CODING_STANDARDS.md) | The rules for writing code here — IronPython 2.7 constraints, typing, serialization, testing |
| [`AUTODOC.md`](AUTODOC.md) | Feature spec for the automated API-doc generator that feeds the ph-docs hub |
| [`decisions/`](decisions/) | Numbered decision records — especially decisions *not* to do something |

## Maintenance rule

When an accepted design decision changes how the library works, fold it back into the relevant doc here (and add a `decisions/` record if it closes off an alternative). Keep these docs true; stale canon is worse than none.
