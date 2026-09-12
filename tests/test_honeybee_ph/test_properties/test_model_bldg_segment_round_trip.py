from honeybee.model import Model
from honeybee.room import Room
from ladybug_geometry.geometry3d.pointvector import Point3D

import honeybee_ph._extend_honeybee_ph  # noqa: F401  (registers the '.ph' properties)
from honeybee_ph.bldg_segment import BldgSegment


def _model_with_shared_segment():
    """Return a 3-Room Model where Rooms 1 and 2 share one BldgSegment and Room 3 has its own."""
    shared_segment = BldgSegment()
    shared_segment.display_name = "Shared_Segment"

    other_segment = BldgSegment()
    other_segment.display_name = "Other_Segment"

    rooms = []
    for i, segment in enumerate([shared_segment, shared_segment, other_segment]):
        room = Room.from_box("room_{}".format(i), 5, 5, 3, origin=Point3D(i * 10, 0, 0))
        room.properties.ph.ph_bldg_segment = segment  # type: ignore
        rooms.append(room)

    return Model("test_model", rooms=rooms), shared_segment, other_segment


def test_model_to_dict_abridged_writes_the_unique_bldg_segments():
    model, _, _ = _model_with_shared_segment()

    d = model.properties.ph.to_dict(abridged=True)["ph"]  # type: ignore

    assert d["type"] == "ModelPhPropertiesAbridged"
    assert len(d["bldg_segments"]) == 2


def test_model_to_dict_unabridged_writes_the_unique_bldg_segments():
    model, _, _ = _model_with_shared_segment()

    d = model.properties.ph.to_dict(abridged=False)["ph"]  # type: ignore

    assert d["type"] == "ModelPhProperties"
    assert len(d["bldg_segments"]) == 2


def test_bldg_segments_survive_a_full_model_round_trip():
    """Every Room gets its BldgSegment back, and Rooms that shared one still share one."""
    model, shared_segment, other_segment = _model_with_shared_segment()

    new_model = Model.from_dict(model.to_dict())
    new_segments = [rm.properties.ph.ph_bldg_segment for rm in new_model.rooms]  # type: ignore

    assert [seg.identifier for seg in new_segments] == [
        shared_segment.identifier,
        shared_segment.identifier,
        other_segment.identifier,
    ]

    # -- The two Rooms that shared a segment resolve to one object, not two copies
    assert new_segments[0] is new_segments[1]
    assert new_segments[0] is not new_segments[2]
