# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Thermal Bridge Objects"""

from math import radians

try:
    from typing import Any, Union
except ImportError:
    pass  # IronPython 2.7

try:
    from ladybug_geometry.geometry3d.plane import Plane
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
    from ladybug_geometry.geometry3d.polyline import LineSegment3D, Polyline3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee_energy_ph.construction import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph.construction:\n\t{}".format(e))

try:
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_utils:\n\t{}".format(e))


class PhThermalBridgeType(enumerables.CustomEnum):
    allowed = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "15-Ambient",
        "16-Perimeter",
        "17-FS/BC",
    ]

    def __init__(self, _value=15, _index_offset=0):
        # type: (Union[str, int], int) -> None
        super(PhThermalBridgeType, self).__init__(_value, _index_offset)


class PhThermalBridge(_base._Base):
    """A single PhThermalBridge object"""

    def __init__(self, _identifier, _geometry):
        # type: (Any, Union[Polyline3D, LineSegment3D]) -> None
        super(PhThermalBridge, self).__init__(_identifier)
        self.geometry = _geometry
        self.display_name = "_unnamed_thermal_bridge_"
        self.quantity = 1.0
        self._group_type = PhThermalBridgeType(15)
        self.psi_value = 0.1
        self.fRsi_value = 0.75

    @property
    def length(self):
        # type: () -> float
        return self.geometry.length

    @property
    def group_type(self):
        # type: () -> PhThermalBridgeType
        return self._group_type

    @group_type.setter
    def group_type(self, _in):
        # type: (Union[str, int]) -> None
        self._group_type = PhThermalBridgeType(_in)

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhThermalBridge, self).to_dict()
        d["quantity"] = self.quantity
        d["_group_type"] = self._group_type.to_dict()
        d["psi_value"] = self.psi_value
        d["fRsi_value"] = self.fRsi_value
        d["geometry"] = self.geometry.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhThermalBridge

        # -- Geom might be either type
        try:
            geom = Polyline3D.from_dict(_input_dict["geometry"])
        except:
            try:
                geom = LineSegment3D.from_dict(_input_dict["geometry"])
            except:
                raise Exception(
                    "Thermal Bridge geometry dict: '{}' is not LineSegment3D or Polyline3D?".format(_input_dict["type"])
                )

        new_obj = cls(_input_dict["identifier"], geom)
        new_obj.set_base_attrs_from_dict(_input_dict)
        new_obj.quantity = _input_dict["quantity"]
        new_obj._group_type = PhThermalBridgeType.from_dict(_input_dict["_group_type"])
        new_obj.psi_value = _input_dict["psi_value"]
        new_obj.fRsi_value = _input_dict["fRsi_value"]
        return new_obj

    def duplicate(self):
        # type: () -> PhThermalBridge
        return self.__copy__()

    def __copy__(self):
        # type: () -> PhThermalBridge
        new_obj = self.__class__(self.identifier, self.geometry)
        new_obj.set_base_attrs_from_obj(self)
        new_obj.display_name = self.display_name
        new_obj.quantity = self.quantity
        new_obj.group_type = self.group_type.value
        new_obj.psi_value = self.psi_value
        new_obj.fRsi_value = self.fRsi_value
        return new_obj

    def __str__(self):
        return "{}(geometry={}, length={}, display_name={}, psi_value={:.3f}, fRsi_value={:.3f}, length={:.3f})".format(
            self.__class__.__name__,
            self.geometry,
            self.length,
            self.display_name,
            self.psi_value,
            self.fRsi_value,
            self.length,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhThermalBridge
        """Move the TB-Geometry along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        """
        new_tb = self.duplicate()
        new_tb.geometry = self.geometry.move(moving_vec3D)
        return new_tb

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhThermalBridge
        """Rotate the TB-Geometry by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis representing the axis of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin around which the object will be rotated.
        """
        new_tb = self.duplicate()
        new_tb.geometry = self.geometry.rotate(axis_vec3D, radians(angle_degrees), origin_pt3D)
        return new_tb

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhThermalBridge
        """Rotate the TB-Geometry counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin around which the object will be rotated.
        """
        new_tb = self.duplicate()
        new_tb.geometry = self.geometry.rotate_xy(radians(angle_degrees), origin_pt3D)
        return new_tb

    def reflect(self, plane):
        # type: (Plane) -> PhThermalBridge
        """Reflected the TB-Geometry across a plane.

        Args:
            normal_vec3D: A Plane representing the plane across which to reflect.
        """
        new_tb = self.duplicate()
        new_tb.geometry = self.geometry.reflect(plane.n, plane.o)
        return new_tb

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Point3D | None) -> PhThermalBridge
        """Scale the TB-Geometry by a factor from an origin point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_tb = self.duplicate()
        new_tb.geometry = self.geometry.scale(scale_factor, origin_pt3D)
        return new_tb
