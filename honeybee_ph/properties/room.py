# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive House (PH) Properties."""

try:
    from typing import Any, Dict, List, Optional, Union
except ImportError:
    pass  # Python2.7

try:
    from ladybug_geometry.geometry3d.plane import Plane
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee import room
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_ph import space
    from honeybee_ph.bldg_segment import BldgSegment
    from honeybee_ph.foundations import PhFoundation, PhFoundationFactory
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))

try:
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_utils:\n\t{}".format(e))

"""
room.Room
    ├─ properties: RoomProperties
        ├─ energy: RoomEnergyProperties
        ├─ ph: RoomPhProperties
            ├─ spaces: List[space.RoomPhProperties]    
                ├─ properties: SpaceProperties
                    ├─ ph: SpacePhProperties
                    ├─ energy: SpaceEnergyProperties
                    ├─...
        ├─ ph_hvac: RoomPhHvacProperties
        ├─ ...
"""

# -----------------------------------------------------------------------------


class PhSpecificHeatCapacity(enumerables.CustomEnum):
    allowed = [
        "1-LIGHTWEIGHT",
        "2-MIXED",
        "3-MASSIVE",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhSpecificHeatCapacity, self).__init__(_value)


# -----------------------------------------------------------------------------


class RoomPhProperties(object):
    def __init__(self, _host):
        # type: (Optional[room.Room]) -> None
        self._host = _host
        self.id_num = 0
        self._spaces = list()  # type: List[space.Space]
        self.ph_bldg_segment = BldgSegment()
        self._ph_foundations = {}  # type: Dict[str, PhFoundation]
        self.specific_heat_capacity = PhSpecificHeatCapacity("1-LIGHTWEIGHT")

    @property
    def spaces(self):
        # type: () -> List[space.Space]
        return self._spaces

    @property
    def total_space_floor_area(self):
        # type: () -> float
        """The total unweighted floor-area of all spaces hosted by the honeybee-Room."""
        return sum((sp.floor_area for sp in self.spaces))

    @property
    def host(self):
        return self._host

    @property
    def ph_foundations(self):
        # type: () -> List[PhFoundation]
        return list(self._ph_foundations.values())

    def duplicate(self, new_host=None, include_spaces=True):
        # type: (Any, bool) -> RoomPhProperties
        _host = new_host or self._host
        new_obj = RoomPhProperties(_host)
        new_obj.id_num = self.id_num
        new_obj.specific_heat_capacity = PhSpecificHeatCapacity(self.specific_heat_capacity.value)

        if include_spaces:
            for sp in self._spaces:
                new_obj._spaces.append(sp.duplicate(_host))

        new_obj.ph_bldg_segment = self.ph_bldg_segment.duplicate()

        for f in self.ph_foundations:
            new_obj.add_foundation(f.duplicate())

        return new_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "{}: [host: {}]".format(self.__class__.__name__, self.host)

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Any]
        d = {}

        d["spaces"] = [sp.to_dict() for sp in self.spaces]
        d["specific_heat_capacity"] = self.specific_heat_capacity.value

        if abridged == False:
            d["type"] = "RoomPhProperties"
            d["id_num"] = self.id_num
            d["ph_bldg_segment"] = self.ph_bldg_segment.to_dict()
            d["ph_foundations"] = [f.to_dict() for f in self.ph_foundations]
        else:
            d["type"] = "RoomPhPropertiesAbridged"
            d["ph_bldg_segment_id"] = self.ph_bldg_segment.identifier
            d["ph_foundations"] = [f.to_dict() for f in self.ph_foundations]

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], Any) -> RoomPhProperties
        assert _input_dict["type"] == "RoomPhProperties", "Expected RoomPhProperties. Got {}.".format(
            _input_dict["type"]
        )

        new_prop = cls(host)
        new_prop.id_num = _input_dict.get("id_num", 0)
        new_prop.specific_heat_capacity = PhSpecificHeatCapacity(
            _input_dict.get("specific_heat_capacity", new_prop.specific_heat_capacity.value)
        )

        if "ph_bldg_segment" in _input_dict.keys():
            new_prop.ph_bldg_segment = BldgSegment.from_dict(_input_dict.get("ph_bldg_segment", {}))
        else:
            new_prop.ph_bldg_segment = None

        for sp in (space.Space.from_dict(d, host) for d in _input_dict.get("spaces", [])):
            new_prop.add_new_space(sp)

        for f_dict in _input_dict["ph_foundations"]:
            new_prop.add_foundation(PhFoundationFactory.from_dict(f_dict))

        return new_prop

    def apply_properties_from_dict(self, room_prop_dict, bldg_segments):
        # type: (Dict[str, Any], Dict[str, BldgSegment]) -> None
        """Apply properties from a RoomPhPropertiesAbridged dictionary.

        Arguments:
        ----------
            * room_prop_dict (dict): A RoomPhPropertiesAbridged dictionary loaded from
                the room object itself. Unabridged. In Abridged form, this
                dict will just include the 'ph_bldg_segment_id' reference instead of the
                the entire properties data dict.

            * bldg_segments (dict[str: BldgSegment]): A dict of the BldgSegment
                objects found at the Model level. Segment-id is used as the key.

        Returns:
        --------
            * None
        """

        self.specific_heat_capacity = PhSpecificHeatCapacity(
            room_prop_dict.get("specific_heat_capacity", self.specific_heat_capacity.value)
        )

        # -- Set the bldg-segment attributes from the values stored at the 'Model' level
        room_ph_bldg_segment_id = room_prop_dict.get("ph_bldg_segment_id", None)
        if room_ph_bldg_segment_id:
            self.ph_bldg_segment = bldg_segments[room_ph_bldg_segment_id]

        # -- Rebuild the Spaces hosted on the room
        space_dicts = room_prop_dict.get("spaces", [])

        for space_dict in space_dicts:
            self.add_new_space(space.Space.from_dict(space_dict, self.host))

        for f_dict in room_prop_dict["ph_foundations"]:
            self.add_foundation(PhFoundationFactory.from_dict(f_dict))

        return None

    def add_new_space(self, _new_space):
        # type: (space.Space) -> None
        """Adds a new PH-Space to the RoomProperties collection."""
        if _new_space:
            self._spaces.append(_new_space)

    def add_foundation(self, _ph_foundation):
        # type: (PhFoundation) -> None
        if not _ph_foundation:
            return
        self._ph_foundations[_ph_foundation.identifier] = _ph_foundation

    def merge_new_space(self, _new_space):
        # type: (space.Space) -> None
        """Try and merge a new Space with the existing Space.

        If there is no existing Space, will set this as the Room's Space.
        """
        try:
            self._spaces[0].add_new_volumes(_new_space.volumes)
        except IndexError:
            self.add_new_space(_new_space)

    def move(self, moving_vec3D):
        # type: (Vector3D) -> None
        """Move the RoomPhProperties and its Volumes along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        """
        self._spaces = [space.move(moving_vec3D) for space in self.spaces]

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> None
        """Rotate the RoomPhProperties and its Volumes by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        """
        self._spaces = [space.rotate(axis_vec3D, angle_degrees, origin_pt3D) for space in self.spaces]

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> None
        """Rotate the RoomPhProperties and its Volumes counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        """
        self._spaces = [space.rotate_xy(angle_degrees, origin_pt3D) for space in self.spaces]

    def reflect(self, plane):
        # type: (Plane) -> None
        """Reflected the RoomPhProperties and its Volumes across a plane with the input normal vector and origin_pt3D.

        Args:
            plane: A Plane representing the plane across which the object will be reflected.
        """
        self._spaces = [space.reflect(plane.n, plane.o) for space in self.spaces]

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> None
        """Scale the RoomPhProperties and its Volumes by a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        """
        self._spaces = [space.scale(scale_factor, origin_pt3D) for space in self.spaces]

    # TODO: Transform Foundations....
    # TODO: Building Segment (icfa/tfa overrides)....


def get_ph_prop_from_room(_room):
    # type: (room.Room) -> RoomPhProperties
    """Get the RoomPhProperties of a HB-Room object."""
    return getattr(_room.properties, "ph")
