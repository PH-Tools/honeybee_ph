# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive House (PH) Properties."""

try:
    from typing import Any, Optional, List
except ImportError:
    pass  # Python2.7

try:
    from ladybug_geometry import geometry3d
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee_ph.bldg_segment import BldgSegment
    from honeybee_ph import space
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


class RoomPhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self._spaces = list()
        self.ph_bldg_segment = BldgSegment()

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

    def duplicate(self, new_host=None, include_spaces=True):
        # type: (Any, bool) -> RoomPhProperties
        _host = new_host or self._host
        new_properties_obj = RoomPhProperties(_host)
        new_properties_obj.id_num = self.id_num

        if include_spaces:
            for sp in self._spaces:
                new_properties_obj._spaces.append(sp.duplicate(_host))

        new_properties_obj.ph_bldg_segment = self.ph_bldg_segment.duplicate()

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "{}: [host: {}]".format(self.__class__.__name__, self.host)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}

        d["spaces"] = [sp.to_dict() for sp in self.spaces]

        if abridged == False:
            d["type"] = "RoomPhProperties"
            d["id_num"] = self.id_num
            d["ph_bldg_segment"] = self.ph_bldg_segment.to_dict()
        else:
            d["type"] = "RoomPhPropertiesAbridged"
            d["ph_bldg_segment_id"] = self.ph_bldg_segment.identifier

        return {"ph": d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> RoomPhProperties
        assert (
            _dict["type"] == "RoomPhProperties"
        ), "Expected RoomPhProperties. Got {}.".format(_dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _dict.get("id_num", 0)

        if "ph_bldg_segment" in _dict.keys():
            new_prop.ph_bldg_segment = BldgSegment.from_dict(
                _dict.get("ph_bldg_segment", {})
            )
        else:
            new_prop.ph_bldg_segment = None

        for sp in (space.Space.from_dict(d, host) for d in _dict.get("spaces", [])):
            new_prop.add_new_space(sp)

        return new_prop

    def apply_properties_from_dict(self, room_prop_dict, bldg_segments):
        # type: (dict[str, Any], dict[str, BldgSegment]) -> None
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

        # -- Set the bldg-segment attributes from the values stored at the 'Model' level
        room_ph_bldg_segment_id = room_prop_dict.get("ph_bldg_segment_id", None)
        if room_ph_bldg_segment_id:
            self.ph_bldg_segment = bldg_segments[room_ph_bldg_segment_id]

        # -- Rebuild the Spaces hosted on the room
        space_dicts = room_prop_dict.get("spaces", [])
        for space_dict in space_dicts:
            self.add_new_space(space.Space.from_dict(space_dict, self.host))

        return None

    def add_new_space(self, _new_space):
        # type: (space.Space) -> None
        """Adds a new PH-Space to the RoomProperties collection."""
        if _new_space:
            self._spaces.append(_new_space)

    def merge_new_space(self, _new_space):
        # type: (space.Space) -> None
        """Try and merge a new Space with the existing Space.

        If there is no existing Space, will set this as the Room's Space.
        """
        try:
            self._spaces[0].add_new_volumes(_new_space.volumes)
        except IndexError:
            self.add_new_space(_new_space)

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the room, and all the spaces in the room by a specified factor.

        Arguments:
        ----------
            * factor (float): The scale factor
            * origin (Optional[geometry3d.Point3D]): default=None, A ladybug_geometry
                Point3D representing the origin from which to scale. If None,
                it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * None
        """

        for space in self.spaces:
            space.scale(factor, origin=None)
