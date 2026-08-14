# Phase 01 — Contract and geometry tests

**Status:** Complete · 2026-08-14

## Objective

Encode the complete public/geometry contract before implementing the factory.

## Fixed decisions

- Public API: `Space.from_room(hb_room, avg_ceiling_height)`.
- `avg_ceiling_height` is required, finite, greater than zero, and expressed in
  the same coordinate units as the Room geometry.
- The factory is non-mutating and returns one unattached Space hosted by the
  supplied Honeybee Room.
- One Floor-type source face becomes one segment, one floor, and one volume;
  no v1 merging or topology repair.
- Horizontal Honeybee Floor geometry is supported. Because solid Honeybee
  Rooms wind floor faces outward (`-Z`), the extrusion copy is normalized to
  `+Z`; the source floor geometry is preserved on the PH objects.
- Space name is `"{room.display_name}_default_space"`.

## Tests first

1. `Room.from_box` in meter coordinates: structure, area, height, and volume.
2. Equivalent foot-scaled Room with an explicitly foot-scaled height: prove no
   implicit SI conversion.
3. Multi-floor-face Room: preserve one floor/volume per source face and source
   order.
4. No Floor-type faces: room-specific error.
5. Zero, negative, NaN, positive/negative infinity, bool, and nonnumeric height:
   field-specific validation errors.
6. Sloped or non-extrudable floor: room- and face-specific error; no partial
   Space returned. Degenerate `Face3D` inputs are rejected by Ladybug before
   they can become Honeybee Faces. Both valid floor windings are covered.
7. Host identity, default name, weighting/net-area defaults, and non-mutation.
8. Confirm no Rhino/ladybug_rhino/ph_units import is needed.

## Exit checks

- Expected tests fail only because `Space.from_room` does not exist.
- Unit/geometry behavior contains no unresolved implementation choice.
- The exact supported Ladybug/Honeybee versions expose the required face-type,
  normal/horizontal checks, and `Polyface3D.from_offset_face()` API.

## Evidence

- Pre-implementation: focused failures were all due to the missing
  `Space.from_room()` API/import.
- Post-implementation: 18 focused tests pass.
