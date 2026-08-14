# PRD — `Space.from_room()` default-space factory (upstreamed from GH)

**Status:** Implementing · Phase 03 complete; Phase 04 next · 2026-08-14
**Author:** Ed May + Claude
**Kind:** Feature / cross-repo refactor — **this repo is primary**, ships
first. Companion: `honeybee_grasshopper_ph/planning/archive/space-from-room-factory/`.

---

## WHAT

An SDK-level factory in honeybee-ph that builds a complete, default PH
`Space` (floor segments → floor → volume → space) from a Honeybee `Room`,
with **no Rhino dependency**:

```python
from honeybee_ph.space import Space

space = Space.from_room(hb_room, avg_ceiling_height=2.5)
hb_room.properties.ph.add_new_space(space)
```

The public home is fixed as the `Space.from_room` classmethod; do not add a
parallel `make_spaces` orchestration API.

Behavior contract (matches today's GH component semantics,
`space_create_from_hb_rooms.py`):

1. **Floor segments:** one `SpaceFloorSegment` per Floor-type face of the
   room, `geometry` = the face's `Face3D`, `reference_point` = its center.
   Room with no floor faces → clear exception naming the room.
2. **Floor:** v1 creates one `SpaceFloor` per source floor face and preserves
   one `SpaceFloorSegment` inside it. This matches the existing lower-level GH
   `build_floors_from_segments(..., _merge_segments=False)` behavior, preserves
   source identity, and avoids making topology repair part of the factory.
   Coplanar/touching floor merging is a later explicit option, not an
   implementation-time choice.
3. **Volume:** create one `SpaceVolume` per floor and extrude by the ceiling
   height using
   `ladybug_geometry.geometry3d.polyface.Polyface3D.from_offset_face(face, height)`
   (verified present — same mechanism `honeybee.Room.from_box` uses) in place
   of the GH pipeline's `IGH.extrude_Face3D_WorldZ`. Set
   `avg_ceiling_height` from the required argument.
4. **Space:** name defaults to `"{room.display_name}_default_space"`,
   volume(s) attached via `add_new_volumes`.
5. **Units follow the Room geometry.** A standalone Honeybee `Room` has no
   units or parent-Model reference, so this factory cannot safely infer or
   convert units. `avg_ceiling_height` is required and uses the same coordinate
   units as `room.geometry`; the resulting `SpaceVolume.avg_ceiling_height`
   uses those model units as well. The factory performs no conversion. The GH
   wrapper preserves its user-facing 2.5 m default by converting 2.5 m into
   Rhino document/model units before calling the factory. A meter-based Python
   caller passes `2.5` explicitly.
6. **Host contract:** the returned `Space.host` is the Honeybee `Room`. This
   matches the `Space` public docstring/type contract and `Space.from_dict(...,
   _host=room)` behavior. The current GH component's use of `RoomPhProperties`
   is historical behavior to correct in its companion refactor, not an
   alternate public host type.
7. **Non-mutating:** the factory builds and returns the `Space`; attaching it
   to the room (`add_new_space`) and any `room.duplicate()` semantics remain
   the caller's / GH wrapper's job.
8. **Geometry validity:** `avg_ceiling_height` must be a finite value greater
   than zero. V1 supports horizontal Honeybee Floor faces. Honeybee solid
   Rooms normally wind floor faces outward with a `-Z` normal, so the factory
   normalizes an extrusion-only copy to `+Z` while preserving the source face
   on the segment/floor. It raises a clear room/face-specific error for
   geometry it cannot extrude vertically without changing the source floor
   area, and must not silently extrude a sloped floor along the wrong vector.
9. **Area defaults:** each generated segment starts at weighting factor `1.0`
   and uses its geometric area unless the existing model contract defines a
   different explicit default. The docstring must state that callers still own
   final TFA/iCFA reductions.

### Constraints

- IronPython 2.7-compatible syntax + comment-style type hints (this code will
  be imported inside Rhino once the GH wrapper re-points to it).
- Imports limited to `ladybug_geometry`, `honeybee`, and honeybee-ph's own
  modules — no `honeybee_ph_rhino`, no `ladybug_rhino`, no `ph_units`.
- pytest: factory on a `Room.from_box` room (segment/floor/volume/space
  structure, areas, volume, height), a multi-floor-face room with one preserved
  volume per face, invalid height, unsupported sloped floor, the no-floor error,
  correct Honeybee Room host, weighted-floor-area flows through to
  `properties.ph` as expected, and dict round-trip of a room carrying a
  factory-built space. Include meter- and foot-scaled fixtures proving that the
  caller-supplied height is interpreted in Room coordinate units.
- Reference implementations to port from (read before writing):
  - `honeybee_grasshopper_ph/honeybee_ph_rhino/gh_compo_io/space_create_from_hb_rooms.py`
    (the orchestration, ~130 lines)
  - `honeybee_grasshopper_ph/honeybee_ph_rhino/make_spaces/{make_floor_segment,make_floor,make_volume,make_space}.py`
  - `~/Desktop/ph-modeler/backend/app/calculation.py` `_add_default_ph_space()`
    (the minimal CPython-only re-derivation this feature exists to delete)

## WHY

Building a *default* space from a room is pure model logic — floor faces in,
Space out — yet today it lives only in `honeybee_ph_rhino`, threaded through
the Rhino interface object (`IGH`) for extrusion and merging. Consequences:

1. **Every non-Rhino consumer re-derives it by hand.** The ph-modeler web-app
   POC (2026-08) had to hand-assemble `SpaceFloorSegment → SpaceFloor →
   SpaceVolume → Space` from face geometry — the single largest block of
   custom glue in that app — just to make a default shoebox solvable by
   OpenPH. PH-Navigator and any future script/web front-end face the same
   tax. The geometry operations the GH code delegates to Rhino
   (`extrude_Face3D_WorldZ`, `merge_Face3D`) have pure ladybug-geometry
   equivalents (`Polyface3D.from_offset_face`, `Face3D.join_coplanar_faces`),
   so the Rhino coupling is historical, not necessary.
2. **Two implementations already disagree in the small.** The POC version
   passes the host type documented by `Space`, while the GH component passes
   `RoomPhProperties`; multi-floor-face handling also differs. One upstream
   factory with tests makes the contract real.
3. **Right layer.** honeybee-ph owns the `Space` model; the SDK that defines
   a structure should be able to construct a sensible default of it. The GH
   library keeps what is genuinely Rhino's: document-unit conversion, IGH
   error routing, user geometry input — as a thin wrapper over the upstream
   factory (see companion refactor doc).
