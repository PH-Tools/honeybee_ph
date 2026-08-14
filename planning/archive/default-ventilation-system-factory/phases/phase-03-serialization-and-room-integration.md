# Phase 03 — Serialization and Room integration

**Status:** Complete · 2026-08-14

## Objective

Prove every local factory state through duplicate, Room properties, model
collection deduplication, and HBJSON without changing attachment semantics.

## Implementation and tests

1. Round-trip zero/one/multiple-duct factory results through
   `to_dict()`/`from_dict()`.
2. Duplicate each result and prove independent ventilator, duct elements,
   segments, geometry, and user data.
3. Attach a factory result explicitly through
   `RoomPhHvacProperties.set_ventilation_system()` and round-trip Room/Model
   HBJSON.
4. Verify Model mechanical-system collection deduplication and Room reference
   reset preserve identifiers and do not collapse distinct systems.
5. Verify Room duplication/transforms preserve system values and do not mutate
   the source.
6. Add legacy dictionaries missing optional newer keys and prove tolerant
   deserialization.

## Exit checks

- Every accepted local state round-trips and duplicates independently.
- No factory attaches itself implicitly.
- Existing valid HBJSON payloads remain byte-shape compatible unless an
  additive key was explicitly accepted in Phase 01.

## Outcome

All zero/one/many-duct states round-trip through system dictionaries, full and
abridged Room properties, and a real HBJSON file. Direct, Room, and transformed
duplicates own independent system, ventilator, duct element, segment, geometry,
and nested metadata graphs. Public two-Room Model round trips prove identical
system identifiers deduplicate to one shared restored object and distinct
identifiers remain distinct.

Model reload now rejects a same-identifier/different-payload ventilation
collision instead of silently keeping the last graph. Required historical
system keys remain required; genuinely optional metadata (`user_data`,
`id_num`) remains tolerant. Transform implementations reuse metadata-only copy
helpers so the stronger geometry-ownership contract does not allocate and
discard intermediate graphs.

Verification before the full phase gate: 115 focused/adjacent tests pass;
Black, Python 2 grammar parsing, and `git diff --check` pass. The full repository
gate passes with 1016 tests and 80% aggregate coverage.
