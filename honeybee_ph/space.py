# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH 'Space' and Related Sub-object Classes (FloorSegments, etc)."""

try:
    from typing import Any, Optional, List, Dict, Union
except:
    pass  # IronPython

from copy import copy

try:
    from ladybug_geometry import geometry3d
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee_ph import _base
    from honeybee_ph.properties.space import SpaceProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


class SpaceFloorSegment(_base._Base):
    def __init__(self):
        super(SpaceFloorSegment, self).__init__()
        self.geometry = None  # type: Optional[geometry3d.face.Face3D]
        self.weighting_factor = 1.0

        # -- Reference Point Note: Usually this is just the center, although for
        # -- more complex shaped like 'L' and 'U' it cannot just be the center.
        # -- In those cases, it should be a point 'on' the surface, as near to the
        # -- center as possible. This point is used for testing hosting of the
        # -- SpaceFloorSegment 'inside' an HB-Room.
        self.reference_point = None  # type: Optional[geometry3d.pointvector.Point3D]

    @property
    def weighted_floor_area(self):
        # type: () -> float
        """The floor area of the floor segment weighted by any reduction factors (iFCA, TFA)"""
        if self.geometry:
            return self.geometry.area * self.weighting_factor
        else:
            return 0

    @property
    def floor_area(self):
        # type: () -> float
        """The floor area of the floor segment UN-weighted by any reduction factors (iFCA, TFA)"""
        if self.geometry:
            return self.geometry.area
        else:
            return 0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)

        d["weighting_factor"] = self.weighting_factor
        if self.geometry:
            d["geometry"] = self.geometry.to_dict()
        if self.reference_point:
            d["reference_point"] = self.reference_point.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> SpaceFloorSegment
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        new_obj.weighting_factor = _input_dict.get("weighting_factor", 1.0)

        geom_dict = _input_dict.get("geometry", None)
        if geom_dict:
            new_obj.geometry = geometry3d.Face3D.from_dict(geom_dict)

        ref_pt_dict = _input_dict.get("reference_point", None)
        if ref_pt_dict:
            new_obj.reference_point = geometry3d.Point3D.from_dict(ref_pt_dict)

        return new_obj

    def duplicate(self):
        # type: () -> SpaceFloorSegment
        new_obj = SpaceFloorSegment()
        
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data

        if self.geometry:
            new_obj.geometry = self.duplicate_geometry()

        if self.reference_point:
            new_obj.reference_point = self.reference_point.duplicate()

        new_obj.weighting_factor = self.weighting_factor

        return new_obj

    def duplicate_geometry(self):
        # type: () -> geometry3d.face.Face3D
        try:
            return self.geometry.duplicate()
        except AttributeError as e:
            msg = (
                "\n\tSpaceFloorSegment {} has no geometry? "
                "Cannot duplicate it.".format(self)
            )
            raise AttributeError(msg, e)

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the floor-segment geometry by a specified factor.

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

        if self.geometry:
            self.geometry = self.geometry.scale(factor, origin)

        if self.reference_point:
            self.reference_point = self.reference_point.scale(factor, origin)

    def __str__(self):
        return "{}(weighting_factor={!r}, geometry={!r}, reference_point={!r})".format(
            self.__class__.__name__,
            self.weighting_factor,
            self.geometry,
            self.reference_point,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class SpaceFloor(_base._Base):
    def __init__(self):
        super(SpaceFloor, self).__init__()
        self._floor_segments = list()  # type: List[SpaceFloorSegment]
        self.geometry = None  # type: Optional[geometry3d.face.Face3D]

    @property
    def reference_points(self):
        # type() -> list[geometry3d.Point3D]
        """Returns a list of the Floor's FloorSegment reference points."""
        return [seg.reference_point for seg in self.floor_segments]

    @property
    def weighted_floor_area(self):
        # type: () ->  float
        """The total floor area of all floor segments, weighted by any reduction factors (iFCA, TFA)"""
        return sum((seg.weighted_floor_area for seg in self.floor_segments))

    @property
    def floor_area(self):
        # type: () ->  float
        """The total floor area of all floor segments, UN-weighted by any reduction factors (iFCA, TFA)"""
        return sum((seg.floor_area for seg in self.floor_segments))

    def add_floor_segment(self, _floor_seg):
        # type: (SpaceFloorSegment) -> None
        """Add a new SpaceFloorSegment to the SpaceFloor.

        Arguments:
        ----------
            * _floor_seg (SpaceFloorSegment): The SpaceFloorSegment to add to the SpaceFloor.

        Returns:
        --------
            * None
        """
        if not _floor_seg:
            return
        self._floor_segments.append(_floor_seg)

    def clear_floor_segments(self):
        self._floor_segments = list()

    @property
    def floor_segments(self):
        # type: () -> list[SpaceFloorSegment]
        return self._floor_segments

    def duplicate(self):
        # type: () -> SpaceFloor
        new_floor = SpaceFloor()

        new_floor.identifier = self.identifier
        new_floor.display_name = self.display_name
        new_floor.user_data = self.user_data

        if self.geometry:
            new_floor.geometry = self.geometry.duplicate()
        for seg in self.floor_segments:
            new_floor.add_floor_segment(seg.duplicate())
        return new_floor

    def duplicate_geometry(self):
        # type: () -> geometry3d.face.Face3D
        try:
            return self.geometry.duplicate()
        except AttributeError as e:
            msg = "\n\tSpaceFloorSegment {} has to .geometry? Cannot duplicate.".format(
                self
            )
            raise AttributeError(msg, e)

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)

        d["floor_segments"] = [seg.to_dict() for seg in self.floor_segments]
        d["geometry"] = self.geometry.to_dict() if self.geometry else None

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> SpaceFloor
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        geom_dict = _input_dict.get("geometry", None)
        if geom_dict:
            new_obj.geometry = geometry3d.Face3D.from_dict(geom_dict)

        flr_seg_dicts = _input_dict.get("floor_segments", [])
        for seg_dict in flr_seg_dicts:
            new_obj.add_floor_segment(SpaceFloorSegment.from_dict(seg_dict))

        return new_obj

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the floor and all the geometry of the floor by a specified factor.

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

        if self.geometry:
            self.geometry = self.geometry.scale(factor, origin)

        for segment in self.floor_segments:
            segment.scale(factor, origin)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class SpaceVolume(_base._Base):
    def __init__(self):
        super(SpaceVolume, self).__init__()
        self.avg_ceiling_height = 2.5  # m
        self.floor = SpaceFloor()
        self.geometry = list()  # type: List[geometry3d.face.Face3D]

    @property
    def net_volume(self):
        # type: () -> float
        return self.floor_area * self.avg_ceiling_height

    @property
    def weighted_floor_area(self):
        # type: () -> float
        """The total floor area of all floor segments in the Volume, weighted by any reduction factors (iFCA, TFA)"""
        return self.floor.weighted_floor_area

    @property
    def floor_area(self):
        # type: () -> float
        """The total floor area of all floor segments in the Volume, UN-weighted by any reduction factors (iFCA, TFA)"""
        return self.floor.floor_area

    @property
    def reference_points(self):
        # type() -> list[geometry3d.Point3D]
        """Returns the Volume's FloorSegment reference points (center)."""
        return self.floor.reference_points

    @property
    def floor_segment_surfaces(self):
        # type: () -> List[Optional[geometry3d.face.Face3D]]
        return [flr_seg.geometry for flr_seg in self.floor.floor_segments]

    @property
    def floor_segments(self):
        # type: () -> List[SpaceFloorSegment]
        return self.floor.floor_segments

    def clear_volume_geometry(self):
        # type: () -> None
        """Delete all the geometry from the SpaceVolume."""
        self.geometry = []

    def duplicate(self):
        # type: () -> SpaceVolume
        new_volume = SpaceVolume()

        new_volume.identifier = self.identifier
        new_volume.display_name = self.display_name
        new_volume.user_data = self.user_data

        new_volume.avg_ceiling_height = self.avg_ceiling_height
        new_volume.floor = self.floor.duplicate()
        if self.geometry:
            new_volume.geometry = [geo.duplicate() for geo in self.geometry]
        return new_volume

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)

        d["avg_ceiling_height"] = self.avg_ceiling_height
        d["floor"] = self.floor.to_dict()
        d["geometry"] = [geom.to_dict() for geom in self.geometry]

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> SpaceVolume
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        new_obj.avg_ceiling_height = _input_dict.get("avg_ceiling_height")
        new_obj.floor = SpaceFloor.from_dict(_input_dict.get("floor", {}))

        geom_list = _input_dict.get("geometry", [])
        for geom_dict in geom_list:
            new_obj.geometry.append(geometry3d.Face3D.from_dict(geom_dict))

        return new_obj

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the volume and all the geometry of the volume by a specified factor.

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

        original_geometry = copy(self.geometry)
        self.clear_volume_geometry()
        for srfc in original_geometry:
            self.geometry.append(srfc.scale(factor, origin))

        self.avg_ceiling_height = self.avg_ceiling_height * factor

        self.floor.scale(factor, origin)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Space(_base._Base):
    def __init__(self, _host=None):
        super(Space, self).__init__()
        self.quantity = 1
        self.wufi_type = 99  # -- User-Defined
        self.name = ""
        self.number = ""
        self.host = _host

        self._volumes = list()
        self.properties = SpaceProperties(self)

    @property
    def display_name(self):
        # type: () -> str
        return "{}: {}-{}".format(self.__class__.__name__, self.number, self.name)

    @property
    def full_name(self):
        # type: () -> str
        return "{}-{}".format(self.number, self.name)

    @property
    def net_volume(self):
        # type: () -> float
        return sum([vol.net_volume for vol in self.volumes])

    @property
    def avg_clear_height(self):
        # type: () -> float
        """Returns the average floor-area-weighted height of all the Volumes in the Space"""

        total_weighted_height = 0
        for vol in self.volumes:
            total_weighted_height += vol.floor_area * vol.avg_ceiling_height

        return total_weighted_height / self.floor_area

    @property
    def weighted_floor_area(self):
        # type: () -> float
        """The total floor area of all floor segments in the Space, weighted by any reduction factors (iFCA, TFA)"""
        return sum((vol.weighted_floor_area for vol in self.volumes))

    @property
    def floor_area(self):
        # type: () -> float
        """The total floor area of all floor segments in the Space, UN-weighted by any reduction factors (iFCA, TFA)"""
        return sum((vol.floor_area for vol in self.volumes))

    @property
    def average_floor_weighting_factor(self):
        # type: () -> float
        """Returns the average weighting factor (TFA/iCFA) for the Space's floor-segments."""
        return self.weighted_floor_area / self.floor_area

    @property
    def reference_points(self):
        # type: () -> list[geometry3d.Point3D]
        """Returns a list of the Space's Volume reference Points (center of the floor segments)."""
        pts = []
        for vol in self.volumes:
            pts += vol.reference_points
        return pts

    @property
    def volumes(self):
        # type: () -> List[SpaceVolume]
        return self._volumes

    @property
    def floor_segment_surfaces(self):
        # type: () -> List[List[Optional[geometry3d.face.Face3D]]]
        return [v.floor_segment_surfaces for v in self.volumes]

    @property
    def floor_segments(self):
        # type: () -> List[SpaceFloorSegment]
        return [f for v in self.volumes for f in v.floor_segments]

    def add_new_volumes(self, _new_volumes):
        # type: (Union[SpaceVolume, list[SpaceVolume]]) -> None
        """Add a new SpaceVolume or list of SpaceVolumes to the Space.

        Arguments:
        ----------
            * _new_volumes (list[SpaceVolume]): A list of the SpaceVolumes to add.

        Returns:
        --------
            *  None
        """
        if not isinstance(_new_volumes, (set, tuple, list)):
            _new_volumes = [_new_volumes]

        for new_vol in _new_volumes:
            self._volumes.append(new_vol)

    def duplicate(self, _host=None):
        # type: (Any) -> Space
        new_space = Space()

        new_space.identifier = self.identifier
        new_space.user_data = self.user_data

        if _host:
            new_space.host = _host
        else:
            new_space.host = self.host

        new_space.quantity = self.quantity
        new_space.wufi_type = self.wufi_type
        new_space.name = self.name
        new_space.number = self.number
        new_space.add_new_volumes([vol.duplicate() for vol in self.volumes])
        new_space.properties._duplicate_extension_attr(self.properties)

        return new_space

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["quantity"] = self.quantity
        d["wufi_type"] = self.wufi_type
        d["name"] = self.name
        d["number"] = self.number
        d["volumes"] = [vol.to_dict() for vol in self.volumes]
        d["properties"] = self.properties.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (Dict[str, Any], Any) -> Space
        new_obj = cls(_host)

        new_obj.identifier = _input_dict["identifier"]
        new_obj.user_data = _input_dict["user_data"]

        new_obj.quantity = _input_dict["quantity"]
        new_obj.wufi_type = _input_dict["wufi_type"]
        new_obj.name = _input_dict["name"]
        new_obj.number = _input_dict["number"]
        new_obj.add_new_volumes(
            [SpaceVolume.from_dict(d) for d in _input_dict["volumes"]]
        )
        new_obj.properties = SpaceProperties.from_dict(
            _input_dict["properties"], _host=new_obj
        )
        new_obj.properties._load_extension_attr_from_dict(_input_dict["properties"])
        return new_obj

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the space and all the volumes in the space by a specified factor.

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

        for volume in self.volumes:
            volume.scale(factor, origin)
        self.properties.scale(factor, origin)

    def __str__(self):
        return "{}(name={!r}, number={!r}, volumes={!r})".format(
            self.__class__.__name__, self.name, self.number, self.volumes
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
