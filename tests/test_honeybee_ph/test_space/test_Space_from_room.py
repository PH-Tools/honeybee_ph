import math
import json
from fractions import Fraction

import pytest
from honeybee.face import Face
from honeybee.facetype import Floor, Wall
from honeybee.model import Model
from honeybee.room import Room
from ladybug_geometry.geometry3d import Face3D, Point3D

from honeybee_ph import space


def _floor_face(identifier, x_offset=0.0, reverse=False):
    points = [
        Point3D(x_offset, 0, 0),
        Point3D(x_offset + 2, 0, 0),
        Point3D(x_offset + 2, 3, 0),
        Point3D(x_offset, 3, 0),
    ]
    if reverse:
        points.reverse()
    return Face(identifier, Face3D(points), Floor())


def test_from_room_builds_default_space_in_room_units():
    hb_room = Room.from_box("MeterRoom", width=5, depth=4, height=3)
    source_floor = hb_room.floors[0]

    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)

    assert ph_space.host is hb_room
    assert ph_space.name == "MeterRoom_default_space"
    assert hb_room.properties.ph.spaces == []
    assert len(ph_space.volumes) == 1
    assert len(ph_space.floor_segments) == 1

    volume = ph_space.volumes[0]
    floor = volume.floor
    segment = floor.floor_segments[0]
    assert segment.geometry is source_floor.geometry
    assert floor.geometry is source_floor.geometry
    assert segment.reference_point == source_floor.geometry.center
    assert segment.weighting_factor == 1.0
    assert segment.net_area_factor == 1.0
    assert ph_space.floor_area == pytest.approx(20.0)
    assert ph_space.weighted_floor_area == pytest.approx(20.0)
    assert ph_space.net_floor_area == pytest.approx(20.0)
    assert ph_space.net_volume == pytest.approx(50.0)
    assert volume.avg_ceiling_height == pytest.approx(2.5)
    assert min(face.min.z for face in volume.geometry) == pytest.approx(0.0)
    assert max(face.max.z for face in volume.geometry) == pytest.approx(2.5)


def test_from_room_interprets_height_in_foot_scaled_coordinates():
    hb_room = Room.from_box("FootRoom", width=16, depth=12, height=10)

    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=8.2)

    assert ph_space.floor_area == pytest.approx(192.0)
    assert ph_space.avg_clear_height == pytest.approx(8.2)
    assert ph_space.net_volume == pytest.approx(1574.4)
    assert max(face.max.z for face in ph_space.volumes[0].geometry) == pytest.approx(8.2)


def test_from_room_normalizes_real_numeric_height_for_geometry_kernel():
    hb_room = Room.from_box("FractionHeightRoom")

    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=Fraction(5, 2))

    assert ph_space.avg_clear_height == 2.5
    assert ph_space.volumes[0].avg_ceiling_height == 2.5


def test_from_room_preserves_multiple_floor_faces_and_source_order():
    first_floor = _floor_face("SplitRoom_Floor_1", reverse=True)
    second_floor = _floor_face("SplitRoom_Floor_2", x_offset=3)
    hb_room = Room("SplitRoom", [first_floor, second_floor])

    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)

    assert len(ph_space.volumes) == 2
    assert [volume.floor.geometry for volume in ph_space.volumes] == [
        first_floor.geometry,
        second_floor.geometry,
    ]
    assert [segment.geometry for segment in ph_space.floor_segments] == [
        first_floor.geometry,
        second_floor.geometry,
    ]
    assert ph_space.floor_area == pytest.approx(12.0)
    assert ph_space.net_volume == pytest.approx(30.0)
    for volume in ph_space.volumes:
        assert min(face.min.z for face in volume.geometry) == pytest.approx(0.0)
        assert max(face.max.z for face in volume.geometry) == pytest.approx(2.5)


def test_from_room_rejects_room_without_floor_faces():
    hb_room = Room.from_box("NoFloorRoom")
    hb_room.floors[0].type = Wall()

    with pytest.raises(ValueError, match="NoFloorRoom.*no Floor faces"):
        space.Space.from_room(hb_room, avg_ceiling_height=2.5)


@pytest.mark.parametrize(
    "height",
    [0, -1, math.nan, math.inf, -math.inf, True, False, "2.5", None],
    ids=["zero", "negative", "nan", "positive-infinity", "negative-infinity", "true", "false", "text", "none"],
)
def test_from_room_rejects_invalid_height(height):
    hb_room = Room.from_box("InvalidHeightRoom")

    with pytest.raises(ValueError, match="avg_ceiling_height.*finite number greater than zero"):
        space.Space.from_room(hb_room, avg_ceiling_height=height)

    assert hb_room.properties.ph.spaces == []


def test_from_room_rejects_non_room_host():
    with pytest.raises(TypeError, match="hb_room.*Honeybee Room"):
        space.Space.from_room(object(), avg_ceiling_height=2.5)


def test_from_room_rejects_sloped_floor_with_room_and_face_context():
    sloped_geometry = Face3D(
        [
            Point3D(0, 0, 0),
            Point3D(2, 0, 0),
            Point3D(2, 3, 1),
            Point3D(0, 3, 1),
        ]
    )
    floor_face = Face("SlopedRoom_Floor", sloped_geometry, Floor())
    hb_room = Room("SlopedRoom", [floor_face])

    with pytest.raises(ValueError, match="SlopedRoom.*SlopedRoom_Floor.*horizontal"):
        space.Space.from_room(hb_room, avg_ceiling_height=2.5)

    assert hb_room.properties.ph.spaces == []


def test_from_room_rejects_mixed_valid_and_sloped_floors_without_mutation():
    valid_floor = _floor_face("MixedRoom_Floor_1")
    sloped_floor = Face(
        "MixedRoom_Floor_2",
        Face3D(
            [
                Point3D(3, 0, 0),
                Point3D(5, 0, 0),
                Point3D(5, 3, 1),
                Point3D(3, 3, 1),
            ]
        ),
        Floor(),
    )
    hb_room = Room("MixedRoom", [valid_floor, sloped_floor])

    with pytest.raises(ValueError, match="MixedRoom.*MixedRoom_Floor_2.*horizontal"):
        space.Space.from_room(hb_room, avg_ceiling_height=2.5)

    assert hb_room.properties.ph.spaces == []


def test_from_room_wraps_non_extrudable_geometry_error(monkeypatch):
    hb_room = Room.from_box("NonExtrudableRoom")
    source_floor = hb_room.floors[0]

    def fail_extrusion(face, height):
        raise ValueError("geometry kernel failed")

    monkeypatch.setattr(space.Polyface3D, "from_offset_face", fail_extrusion)

    with pytest.raises(
        ValueError,
        match="NonExtrudableRoom.*{}.*could not be extruded".format(source_floor.identifier),
    ):
        space.Space.from_room(hb_room, avg_ceiling_height=2.5)

    assert hb_room.properties.ph.spaces == []


def test_factory_space_attachment_flows_through_room_properties():
    hb_room = Room.from_box("AttachedRoom", width=5, depth=4, height=3)
    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)
    ph_space.floor_segments[0].weighting_factor = 0.75

    hb_room.properties.ph.add_new_space(ph_space)

    assert hb_room.properties.ph.spaces == [ph_space]
    assert hb_room.properties.ph.total_space_floor_area == pytest.approx(20.0)
    assert hb_room.properties.ph.spaces[0].weighted_floor_area == pytest.approx(15.0)


def test_room_duplicate_rebinds_factory_space_host_and_children():
    hb_room = Room.from_box("DuplicateRoom")
    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)
    hb_room.properties.ph.add_new_space(ph_space)

    duplicated_room = hb_room.duplicate()
    duplicated_space = duplicated_room.properties.ph.spaces[0]

    assert duplicated_space.host is duplicated_room
    assert duplicated_space.host is not hb_room
    assert duplicated_space.to_dict() == ph_space.to_dict()
    assert duplicated_space.volumes[0] is not ph_space.volumes[0]
    assert duplicated_space.volumes[0].floor is not ph_space.volumes[0].floor
    assert duplicated_space.floor_segments[0] is not ph_space.floor_segments[0]
    assert duplicated_space.floor_segments[0].geometry is not ph_space.floor_segments[0].geometry
    assert duplicated_space.volumes[0].geometry[0] is not ph_space.volumes[0].geometry[0]


def test_factory_space_dict_roundtrip_preserves_room_host_contract():
    hb_room = Room.from_box("SpaceDictRoom")
    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)

    restored_space = space.Space.from_dict(ph_space.to_dict(), _host=hb_room)

    assert restored_space.host is hb_room
    assert restored_space.to_dict() == ph_space.to_dict()


def test_room_hbjson_roundtrip_preserves_factory_space_and_host():
    hb_room = Room.from_box("RoomRoundtrip")
    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)
    hb_room.properties.ph.add_new_space(ph_space)

    restored_room = Room.from_dict(json.loads(json.dumps(hb_room.to_dict())))
    restored_space = restored_room.properties.ph.spaces[0]

    assert restored_space.host is restored_room
    assert restored_space.to_dict() == ph_space.to_dict()


def test_model_hbjson_roundtrip_preserves_factory_space_and_host():
    hb_room = Room.from_box("ModelRoundtripRoom")
    ph_space = space.Space.from_room(hb_room, avg_ceiling_height=2.5)
    hb_room.properties.ph.add_new_space(ph_space)
    hb_model = Model("FactoryModel", [hb_room])

    restored_model = Model.from_dict(json.loads(json.dumps(hb_model.to_dict())))
    restored_room = restored_model.rooms[0]
    restored_space = restored_room.properties.ph.spaces[0]

    assert restored_space.host is restored_room
    assert restored_space.to_dict() == ph_space.to_dict()
