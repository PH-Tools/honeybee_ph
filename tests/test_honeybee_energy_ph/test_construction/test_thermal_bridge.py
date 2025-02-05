from uuid import uuid4

import pytest
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_energy_ph.construction import thermal_bridge


def test_default_PhThermalBridge():
    geometry = LineSegment3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    assert tb1.length == pytest.approx(1.0)


def test_PhThermalBridge_to_from_dict_roundtrip():
    geometry = LineSegment3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.display_name = "test"
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8
    tb1.user_data["test_key"] = "test_value"

    tb1_dict = tb1.to_dict()
    tb2 = thermal_bridge.PhThermalBridge.from_dict(tb1_dict)
    tb2_dict = tb2.to_dict()

    assert tb1_dict == tb2_dict
    assert tb1 is not tb2
    assert tb1.geometry == tb2.geometry
    assert tb1.group_type == tb2.group_type
    assert tb1.length == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.identifier == tb2.identifier
    assert "test_key" in tb2.user_data
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value


def test_PhThermalBridge_duplicate():
    geometry = LineSegment3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.display_name = "test"
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8
    tb1.user_data["test_key"] = "test_value"

    tb2 = tb1.duplicate()

    assert tb1 is not tb2
    assert tb1.geometry == tb2.geometry
    assert tb1.group_type == tb2.group_type
    assert tb1.length == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value
    assert tb1.identifier == tb2.identifier
    assert "test_key" in tb2.user_data


# ----


def test_PhThermalBridgeType_15_from_int():
    t = thermal_bridge.PhThermalBridgeType(15)
    assert t.number == 15
    assert t.value == "15-AMBIENT"


def test_PhThermalBridgeType_15_from_num_str():
    t = thermal_bridge.PhThermalBridgeType("15")
    assert t.number == 15
    assert t.value == "15-AMBIENT"


def test_PhThermalBridgeType_15_from_full_str():
    t = thermal_bridge.PhThermalBridgeType("15-AMBIENT")
    assert t.number == 15
    assert t.value == "15-AMBIENT"


# ---


def test_move_PhThermalBridge():
    geometry = LineSegment3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8

    tb2 = tb1.move(
        moving_vec3D=Vector3D(1, 1, 0),
    )

    assert tb1 is not tb2
    assert tb1.length == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value


def test_rotate_PhThermalBridge():
    geometry = LineSegment3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8

    tb2 = tb1.rotate(
        axis_vec3D=Vector3D(0, 0, 1),
        angle_degrees=90,
        origin_pt3D=Point3D(0, 0, 0),
    )

    assert tb1 is not tb2
    assert tb1.length == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value


def test_rotate_xy_PhThermalBridge():
    geometry = LineSegment3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8

    tb2 = tb1.rotate_xy(
        angle_degrees=90,
        origin_pt3D=Point3D(0, 0, 0),
    )

    assert tb1 is not tb2
    assert tb1.length == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value


def test_reflect_PhThermalBridge():
    geometry = LineSegment3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8

    tb2 = tb1.reflect(plane=Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0)))

    assert tb1 is not tb2
    assert tb1.length == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value


def test_scale_PhThermalBridge():
    geometry = LineSegment3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
    tb1 = thermal_bridge.PhThermalBridge(str(uuid4()), geometry)
    tb1.quantity = 2
    tb1.group_type = "16-Perimeter"
    tb1.psi_value = 0.2
    tb1.fRsi_value = 0.8

    tb2 = tb1.scale(2)

    assert tb1 is not tb2
    assert tb1.length * 2 == tb2.length
    assert tb1.display_name == tb2.display_name
    assert tb1.quantity == tb2.quantity
    assert tb1.psi_value == tb2.psi_value
    assert tb1.fRsi_value == tb2.fRsi_value
    assert tb1.group_type == tb2.group_type
    assert tb1.group_type.value == tb2.group_type.value
