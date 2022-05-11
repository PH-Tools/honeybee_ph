from pathlib import Path
import pytest
from honeybee import model
from PHX.from_HBJSON import read_HBJSON_file


def hb_rooms_are_equal(hb_room_1, hb_room_2):
    assert hb_room_1.identifier == hb_room_2.identifier
    assert hb_room_1.display_name == hb_room_2.display_name
    assert hb_room_1.multiplier == hb_room_2.multiplier
    assert hb_room_1.story == hb_room_2.story
    assert hb_room_1.indoor_furniture == hb_room_2.indoor_furniture
    assert hb_room_1.indoor_shades == hb_room_2.indoor_shades
    assert hb_room_1.outdoor_shades == hb_room_2.outdoor_shades
    assert hb_room_1.geometry == hb_room_2.geometry
    assert hb_room_1.center == hb_room_2.center
    assert hb_room_1.volume == hb_room_2.volume
    assert hb_room_1.floor_area == hb_room_2.floor_area
    assert hb_room_1.exposed_area == hb_room_2.exposed_area
    assert hb_room_1.exterior_wall_area == hb_room_2.exterior_wall_area
    assert hb_room_1.exterior_aperture_area == hb_room_2.exterior_aperture_area
    assert hb_room_1.exterior_wall_aperture_area == hb_room_2.exterior_wall_aperture_area
    assert hb_room_1.exterior_skylight_aperture_area == hb_room_2.exterior_skylight_aperture_area
    assert hb_room_1.average_floor_height == hb_room_2.average_floor_height
    assert hb_room_1.user_data == hb_room_2.user_data
    for face1, face2 in zip(sorted(hb_room_1.faces, key=lambda f: f.identifier), sorted(hb_room_2.faces, key=lambda f: f.identifier)):
        assert face1.identifier == face2.identifier
        assert face1.display_name == face2.display_name
        assert face1.type == face2.type
        #assert face1.boundary_condition == face2.boundary_condition
        #assert face1.apertures == face2.apertures
        assert face1.doors == face2.doors
        #assert face1.sub_faces == face2.sub_faces
        assert face1.indoor_shades == face2.indoor_shades
        assert face1.outdoor_shades == face2.outdoor_shades
        #assert face1.parent == face2.parent
        assert face1.has_parent == face2.has_parent
        assert face1.has_sub_faces == face2.has_sub_faces
        assert face1.can_be_ground == face2.can_be_ground
        assert face1.geometry == face2.geometry
        assert face1.punched_geometry == face2.punched_geometry
        assert face1.vertices == face2.vertices
        assert face1.punched_vertices == face2.punched_vertices
        assert face1.upper_left_vertices == face2.upper_left_vertices
        assert face1.normal == face2.normal
        assert face1.center == face2.center
        assert face1.area == face2.area
        assert face1.perimeter == face2.perimeter
        assert face1.aperture_area == face2.aperture_area
        assert face1.aperture_ratio == face2.aperture_ratio
        assert face1.user_data == face2.user_data
    return True


@pytest.mark.parametrize("filename,results",
                         [
                             ('Default_Model_Single_Zone.hbjson', None),
                             ('Default_Room_Single_Zone_with_Apertures.hbjson', None),
                             ('Default_Room_Single_Zone_with_Shades.hbjson', None),
                         ])
def test_read_default_single_zone_model_no_conversion(filename, results):
    file_path = Path('tests', '_source_hbjson', filename)

    d1 = read_HBJSON_file.read_hb_json_from_file(file_path)
    m1 = read_HBJSON_file.convert_hbjson_dict_to_hb_model(d1)

    d2 = m1.to_dict()
    m2 = read_HBJSON_file.convert_hbjson_dict_to_hb_model(d2)

    assert m1.identifier == m2.identifier
    assert m1.display_name == m2.display_name
    assert m1.units == m2.units
    assert m1.tolerance == m2.tolerance
    assert m1.angle_tolerance == m2.angle_tolerance
    for room1, room2 in zip(sorted(m1.rooms), sorted(m2.rooms)):
        assert hb_rooms_are_equal(room1, room2)
