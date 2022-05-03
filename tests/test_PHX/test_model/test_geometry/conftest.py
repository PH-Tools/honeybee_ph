import pytest
from typing import Dict
from PHX.model import geometry


# --- Cube, on regular axis ---------------------------------------------------


def phx_polygon_vertical_north_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 10, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 10, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 10, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 10, 6))
    phx_polygon.normal_vector = geometry.PhxVector(0, 1, 0)
    return phx_polygon


def phx_polygon_vertical_east_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(10, 5, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(10, 6, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(10, 6, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(10, 5, 6))
    phx_polygon.normal_vector = geometry.PhxVector(1, 0, 0)
    return phx_polygon


def phx_polygon_vertical_south_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 0, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 0, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 0, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 0, 6))
    phx_polygon.normal_vector = geometry.PhxVector(0, -1, 0)
    return phx_polygon


def phx_polygon_vertical_west_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(0, 5, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(0, 4, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(0, 4, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(0, 5, 6))
    phx_polygon.normal_vector = geometry.PhxVector(-1, 0, 0)
    return phx_polygon


def phx_polygon_horizontal_upward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 5, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 5, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 6, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 6, 10))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, 1)
    return phx_polygon


def phx_polygon_horizontal_downward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 5, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 6, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 6, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 5, 0))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, -1)
    return phx_polygon


# -- Cube, rotated 30° off axis -----------------------------------------------


def phx_polygon_30_rotated_vertical_northeast_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(8.830127, 7.366025, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(8.330127, 8.232051, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(8.330127, 8.232051, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(8.830127, 7.366025, 6))
    phx_polygon.normal_vector = geometry.PhxVector(0.866025, 0.5, 0)
    return phx_polygon


def phx_polygon_30_rotated_vertical_southeast_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(7, 0.535898, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(7.866025, 1.035898, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(7.866025, 1.035898, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(7, 0.535898, 6))
    phx_polygon.normal_vector = geometry.PhxVector(0.5, -0.866025, 0)
    return phx_polygon


def phx_polygon_30_rotated_vertical_southwest_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(0.169873, 2.366025, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(0.669873, 1.5, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(0.669873, 1.5, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(0.169873, 2.366025, 6))
    phx_polygon.normal_vector = geometry.PhxVector(-0.866025, -0.5, 0)
    return phx_polygon


def phx_polygon_30_rotated_vertical_northwest_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(2, 9.196152, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(1.133975, 8.696152, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(1.133975, 8.696152, 6))
    phx_polygon.add_vertix(geometry.PhxVertix(2, 9.196152, 6))
    phx_polygon.normal_vector = geometry.PhxVector(-0.5, 0.866025, 0)
    return phx_polygon


def phx_polygon_30_rotated_horizontal_upward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(4.5, 4.866025, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(5.366025, 5.366025, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(4.866025, 6.232051, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 5.732051, 10))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, 1)
    return phx_polygon


def phx_polygon_30_rotated_horizontal_downward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(4.5, 4.866025, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 5.732051, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(4.866025, 6.232051, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(5.366025, 5.366025, 0))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, -1)
    return phx_polygon


# -- Truncated Square Pyramid (sides sloped, top and bottom horizontal) -------

def phx_polygon_sq_pyramid_vertical_north_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 8.914214, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 9.126425, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 9.126425, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 8.914214, 5))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0.977224, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_vertical_east_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(8.914214, 5, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(9.126425, 5, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(9.126425, 6, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(8.914214, 6, 5))
    phx_polygon.normal_vector = geometry.PhxVector(0.977224, 0, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_vertical_south_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 1.085786, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 0.873575, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 0.873575, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(6, 1.085786, 5))
    phx_polygon.normal_vector = geometry.PhxVector(0, -0.977224, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_vertical_west_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(1.085786, 5, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(0.873575, 5, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(0.873575, 4, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(1.085786, 4, 5))
    phx_polygon.normal_vector = geometry.PhxVector(-0.977224, 0, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_horizontal_upward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 5, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 5, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 4, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 4, 10))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, 1)
    return phx_polygon


def phx_polygon_sq_pyramid_horizontal_downward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(5, 5, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 4, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 4, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(4, 5, 0))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, -1)
    return phx_polygon


def phx_polygon_sq_pyramid_rotated_vertical_northeast_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(7.889808, 6.823132, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(8.073589, 6.929238, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(7.573589, 7.795263, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(7.389808, 7.689158, 5))
    phx_polygon.normal_vector = geometry.PhxVector(0.846301, 0.488612, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_rotated_vertical_southeast_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(6.457107, 1.476217, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(6.563212, 1.292437, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(7.429238, 1.792437, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(7.323132, 1.976217, 5))
    phx_polygon.normal_vector = geometry.PhxVector(0.488612, -0.846301, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_rotated_vertical_southwest_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(1.110192, 2.908919, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(0.926411, 2.802813, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(1.426411, 1.936788, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(1.610192, 2.042893, 5))
    phx_polygon.normal_vector = geometry.PhxVector(-0.846301, -0.488612, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_rotated_vertical_northwest_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(2.542893, 8.255834, 5))
    phx_polygon.add_vertix(geometry.PhxVertix(2.436788, 8.439614, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(1.570762, 7.939614, 4.022776))
    phx_polygon.add_vertix(geometry.PhxVertix(1.676868, 7.755834, 5))
    phx_polygon.normal_vector = geometry.PhxVector(-0.488612, 0.846301, 0.212211)
    return phx_polygon


def phx_polygon_sq_pyramid_rotated_horizontal_upward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(4.5, 4.866025, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(3.633975, 4.366025, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(4.133975, 3.5, 10))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 4.0, 10))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, 1)
    return phx_polygon


def phx_polygon_sq_pyramid_rotated_horizontal_downward_facing() -> geometry.PhxPolygon:
    phx_polygon = geometry.PhxPolygon()
    phx_polygon.add_vertix(geometry.PhxVertix(4.5, 4.866025, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(5, 4.0, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(4.133975, 3.5, 0))
    phx_polygon.add_vertix(geometry.PhxVertix(3.633975, 4.366025, 0))
    phx_polygon.normal_vector = geometry.PhxVector(0, 0, -1)
    return phx_polygon


@pytest.fixture
def phx_polygons() -> Dict[str, Dict[str, geometry.PhxPolygon]]:

    horizontal: Dict[str, geometry.PhxPolygon] = {
        'downward': phx_polygon_horizontal_downward_facing(),
        'upward': phx_polygon_horizontal_upward_facing(),
        'downward_rotated': phx_polygon_30_rotated_horizontal_downward_facing(),
        'upward_rotated': phx_polygon_30_rotated_horizontal_upward_facing(),
    }

    vertical: Dict[str, geometry.PhxPolygon] = {
        "north": phx_polygon_vertical_north_facing(),
        "east": phx_polygon_vertical_east_facing(),
        "south": phx_polygon_vertical_south_facing(),
        "west": phx_polygon_vertical_west_facing(),
        "northeast": phx_polygon_30_rotated_vertical_northeast_facing(),
        "southeast": phx_polygon_30_rotated_vertical_southeast_facing(),
        "southwest": phx_polygon_30_rotated_vertical_southwest_facing(),
        "northwest": phx_polygon_30_rotated_vertical_northwest_facing(),
    }

    sq_pyramid: Dict[str, geometry.PhxPolygon] = {
        "north": phx_polygon_sq_pyramid_vertical_north_facing(),
        "east": phx_polygon_sq_pyramid_vertical_east_facing(),
        "south": phx_polygon_sq_pyramid_vertical_south_facing(),
        "west": phx_polygon_sq_pyramid_vertical_west_facing(),
        "upward": phx_polygon_sq_pyramid_horizontal_upward_facing(),
        "downward": phx_polygon_sq_pyramid_horizontal_downward_facing(),
        "northeast": phx_polygon_sq_pyramid_rotated_vertical_northeast_facing(),
        "southeast": phx_polygon_sq_pyramid_rotated_vertical_southeast_facing(),
        "southwest": phx_polygon_sq_pyramid_rotated_vertical_southwest_facing(),
        "northwest": phx_polygon_sq_pyramid_rotated_vertical_northwest_facing(),
        "upward_rotated": phx_polygon_sq_pyramid_rotated_horizontal_upward_facing(),
        "downward_rotated": phx_polygon_sq_pyramid_rotated_horizontal_downward_facing(),
    }

    return {
        'horizontal': horizontal,
        'vertical': vertical,
        'sq_pyramid': sq_pyramid,
    }
