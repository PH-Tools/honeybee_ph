# 0005 — Set the Repository Coverage Floor to 75 Percent

**Date:** 2026-08-14
**Status:** DECIDED
**Decider:** Ed May

## Context

The repository's configured `fail_under = 100` gate did not match its actual
coverage. The complete 914-test suite passed while aggregate coverage reported
79%, with uncovered lines spread across established modules outside the
`Space.from_room()` feature scope. This mismatch repeatedly turned successful,
focused feature work into a false repository-wide closeout failure.

## Decision

Set the repository-wide coverage floor to 75% in `pyproject.toml` and all
canonical contributor guidance. New and changed behavior must still receive
focused regression tests covering its public, validation, serialization, and
compatibility contracts.

The 75% floor is a minimum gate, not a target for reducing existing coverage.
Feature work must not remove meaningful tests merely because aggregate
coverage remains above the floor.

## Rationale

- The current suite's 79% aggregate coverage clears a truthful enforceable
  floor.
- A stable repository gate should distinguish regressions from unrelated
  historical coverage debt.
- Focused contract tests remain the effective quality requirement for new
  behavior in this published, backward-compatible package.

## What would reopen this

- Aggregate coverage is raised substantially and remains stable enough to
  support a higher enforced floor.
- CI adopts a reliable changed-lines or per-package coverage gate that can
  supplement or replace the aggregate threshold.
