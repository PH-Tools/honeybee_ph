# Phase 03 — Serialization and Room integration

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

