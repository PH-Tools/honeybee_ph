# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH 'Space' and Related Sub-object Classes (FloorSegments, etc)."""

from copy import copy
from math import radians

try:
    pass
except:
    pass  # IronPython

try:
    from ladybug_geometry.geometry3d.face import Face3D as LBFace3D
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee import room
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_ph import _base
    from honeybee_ph.properties.space import SpaceProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


class SpaceFloorSegment(_base._Base):
    def __init__(self):
        super(SpaceFloorSegment, self).__init__()
        self.geometry = None  # type: Optional[LBFace3D]
        self.weighting_factor = 1.0
        self.net_area_factor = 1.0

        # -- Reference Point Note: Usually this is just the center, although for
        # -- more complex shaped like 'L' and 'U' it cannot just be the center.
        # -- In those cases, it should be a point 'on' the surface, as near to the
        # -- center as possible. This point is used for testing hosting of the
        # -- SpaceFloorSegment 'inside' an HB-Room.
        self.reference_point = None  # type: Optional[Point3D]

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

    @property
    def net_floor_area(self):
        # type: () -> float
        """The net area of the floor segment"""
        return self.floor_area * self.net_area_factor

    @property
    def weighted_net_floor_area(self):
        # type: () -> float
        """The net area of the floor segment weighted by any reduction factors (iFCA, TFA)"""
        return self.floor_area * self.net_area_factor * self.weighting_factor

    def to_dict(self, include_mesh=False, *args, **kwargs):
        # type: (bool, list, dict) -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)
        d["weighting_factor"] = self.weighting_factor
        d["net_area_factor"] = self.net_area_factor

        # -- serialize the properties as well, in case they are needed by the user
        # -- outside the 3D model (ie: in a web-API, etc..)
        d["floor_area"] = self.floor_area
        d["weighted_floor_area"] = self.weighted_floor_area
        d["net_floor_area"] = self.net_floor_area
        d["weighted_net_floor_area"] = self.weighted_net_floor_area

        if self.reference_point:
            d["reference_point"] = self.reference_point.to_dict()

        d["geometry"] = None
        if include_mesh and self.geometry:
            geom_dict = self.geometry.to_dict()  # type: dict[str, Any]
            geom_dict["mesh"] = self.geometry.triangulated_mesh3d.to_dict()
            d["geometry"] = geom_dict
        elif self.geometry:
            d["geometry"] = self.geometry.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> SpaceFloorSegment
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]
        new_obj.weighting_factor = _input_dict.get("weighting_factor", 1.0)
        new_obj.net_area_factor = _input_dict.get("net_area_factor", 1.0)

        geom_dict = _input_dict.get("geometry", None)
        if geom_dict:
            new_obj.geometry = LBFace3D.from_dict(geom_dict)

        ref_pt_dict = _input_dict.get("reference_point", None)
        if ref_pt_dict:
            new_obj.reference_point = Point3D.from_dict(ref_pt_dict)

        return new_obj

    def __copy__(self):
        # type: () -> SpaceFloorSegment
        new_obj = SpaceFloorSegment()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data

        if self.geometry is not None:
            new_obj.geometry = self.duplicate_geometry()

        if self.reference_point is not None:
            new_obj.reference_point = self.reference_point.duplicate()

        new_obj.weighting_factor = self.weighting_factor
        new_obj.net_area_factor = self.net_area_factor

        return new_obj

    def duplicate(self):
        # type: () -> SpaceFloorSegment
        return self.__copy__()

    def duplicate_geometry(self):
        # type: () -> LBFace3D
        try:
            return self.geometry.duplicate()  # type: ignore
        except AttributeError as e:
            msg = "\n\tSpaceFloorSegment {} has no geometry? " "Cannot duplicate it.".format(self)
            raise AttributeError(msg, e)

    def move(self, moving_vec3D):
        # type: (Vector3D) -> SpaceFloorSegment
        """Move the SpaceFloorSegment along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        Returns:
            A new SpaceFloorSegment object with the move applied.
        """
        dup_floor_seg = self.duplicate()
        if self.geometry:
            dup_floor_seg.geometry = self.geometry.move(moving_vec3D)
        if self.reference_point:
            dup_floor_seg.reference_point = self.reference_point.move(moving_vec3D)
        return dup_floor_seg

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> SpaceFloorSegment
        """Rotate the SpaceFloorSegment by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new SpaceFloorSegment object with the rotation applied.
        """
        dup_floor_seg = self.duplicate()
        if self.geometry:
            dup_floor_seg.geometry = self.geometry.rotate(axis_vec3D, radians(angle_degrees), origin_pt3D)
        if self.reference_point is not None:
            new_pt = Point3D.from_array(self.reference_point.rotate(axis_vec3D, radians(angle_degrees), origin_pt3D))
            dup_floor_seg.reference_point = new_pt
        return dup_floor_seg

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> SpaceFloorSegment
        """Rotate the SpaceFloorSegment counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new SpaceFloorSegment object with the rotation applied.
        """
        dup_floor_seg = self.duplicate()
        if self.geometry:
            dup_floor_seg.geometry = self.geometry.rotate_xy(radians(angle_degrees), origin_pt3D)
        if self.reference_point:
            new_pt = Point3D.from_array(self.reference_point.rotate_xy(radians(angle_degrees), origin_pt3D))
            dup_floor_seg.reference_point = new_pt
        return dup_floor_seg

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> SpaceFloorSegment
        """Reflected the SpaceFloorSegment across a plane with the input normal vector and origin_pt3D.

        Args:
            normal_vec3D: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin_pt3D: A Point3D representing the origin_pt3D from which to reflect.
        Returns:
            A new SpaceFloorSegment object with the reflection applied.
        """
        dup_floor_seg = self.duplicate()
        if self.geometry:
            dup_floor_seg.geometry = self.geometry.reflect(normal_vec3D, origin_pt3D)
        if self.reference_point:
            new_pt = Point3D.from_array(self.reference_point.reflect(normal_vec3D, origin_pt3D))
            dup_floor_seg.reference_point = new_pt
        return dup_floor_seg

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> SpaceFloorSegment
        """Scale the SpaceFloorSegment by a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        Returns:
            A new SpaceFloorSegment object with the scaling applied.
        """
        dup_floor_seg = self.duplicate()
        if self.geometry:
            dup_floor_seg.geometry = self.geometry.scale(scale_factor, origin_pt3D)
        if self.reference_point:
            new_pt = Point3D.from_array(self.reference_point.scale(scale_factor, origin_pt3D))
            dup_floor_seg.reference_point = new_pt
        return dup_floor_seg

    def __str__(self):
        return "{}(weighting_factor={!r}, geometry={!r}, reference_point={!r}, net_area_factor={!r})".format(
            self.__class__.__name__,
            self.weighting_factor,
            self.geometry,
            self.reference_point,
            self.net_area_factor,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class SpaceFloor(_base._Base):
    def __init__(self):
        super(SpaceFloor, self).__init__()
        self._floor_segments = list()  # type: List[SpaceFloorSegment]
        self.geometry = None  # type: Optional[LBFace3D]

    @property
    def reference_points(self):
        # type() -> list[Point3D]
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

    @property
    def net_floor_area(self):
        # type: () ->  float
        """The total net floor area of all floor segments"""
        return sum((seg.net_floor_area for seg in self.floor_segments))

    @property
    def weighted_net_floor_area(self):
        # type: () ->  float
        """The total net floor area of all floor segments, weighted by any reduction factors (iFCA, TFA)"""
        return sum((seg.weighted_net_floor_area for seg in self.floor_segments))

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

    def __copy__(self, _include_floor_segments=True):
        # type: (bool) -> SpaceFloor
        new_floor = SpaceFloor()

        new_floor.identifier = self.identifier
        new_floor.display_name = self.display_name
        new_floor.user_data = self.user_data
        if self.geometry:
            new_floor.geometry = copy(self.geometry)

        if _include_floor_segments:
            for seg in self.floor_segments:
                new_floor.add_floor_segment(seg.duplicate())

        return new_floor

    def duplicate(self, _include_floor_segments=True):
        # type: (bool) -> SpaceFloor
        return self.__copy__(_include_floor_segments)

    def duplicate_geometry(self):
        # type: () -> LBFace3D
        if self.geometry is not None:
            return copy(self.geometry)
        else:
            msg = "\n\tSpaceFloorSegment {} has to .geometry? Cannot duplicate.".format(self)
            raise AttributeError(msg)

    def to_dict(self, include_mesh=False, *args, **kwargs):
        # type: (bool, list, dict) -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)
        d["floor_segments"] = [seg.to_dict(include_mesh) for seg in self.floor_segments]

        d["geometry"] = None
        if include_mesh and self.geometry:
            geom_dict = self.geometry.to_dict()  # type: dict[str, Any]
            geom_dict["mesh"] = self.geometry.triangulated_mesh3d.to_dict()
            d["geometry"] = geom_dict
        elif self.geometry:
            d["geometry"] = self.geometry.to_dict()

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
            new_obj.geometry = LBFace3D.from_dict(geom_dict)

        flr_seg_dicts = _input_dict.get("floor_segments", [])
        for seg_dict in flr_seg_dicts:
            new_obj.add_floor_segment(SpaceFloorSegment.from_dict(seg_dict))

        return new_obj

    def move(self, moving_vec3D):
        # type: (Vector3D) -> SpaceFloor
        """Move the SpaceFloor along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        Returns:
            A new SpaceFloor object with the move applied.
        """
        dup_floor = self.duplicate(_include_floor_segments=False)
        if self.geometry:
            dup_floor.geometry = self.geometry.move(moving_vec3D)
        for seg in self.floor_segments:
            dup_floor.add_floor_segment(seg.move(moving_vec3D))
        return dup_floor

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> SpaceFloor
        """Rotate the SpaceFloor by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new SpaceFloor object with the rotation applied.
        """
        dup_floor = self.duplicate(_include_floor_segments=False)
        if self.geometry:
            dup_floor.geometry = self.geometry.rotate(axis_vec3D, radians(angle_degrees), origin_pt3D)
        for seg in self.floor_segments:
            dup_floor.add_floor_segment(seg.rotate(axis_vec3D, angle_degrees, origin_pt3D))
        return dup_floor

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> SpaceFloor
        """Rotate the SpaceFloor counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new SpaceFloor object with the rotation applied.
        """
        dup_floor = self.duplicate(_include_floor_segments=False)
        if self.geometry:
            dup_floor.geometry = self.geometry.rotate_xy(radians(angle_degrees), origin_pt3D)
        for seg in self.floor_segments:
            dup_floor.add_floor_segment(seg.rotate_xy(angle_degrees, origin_pt3D))
        return dup_floor

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> SpaceFloor
        """Reflected the SpaceFloor across a plane with the input normal vector and origin_pt3D.

        Args:
            normal_vec3D: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin_pt3D: A Point3D representing the origin_pt3D from which to reflect.
        Returns:
            A new SpaceFloor object with the reflection applied.
        """
        dup_floor = self.duplicate(_include_floor_segments=False)
        if self.geometry:
            dup_floor.geometry = self.geometry.reflect(normal_vec3D, origin_pt3D)
        for seg in self.floor_segments:
            dup_floor.add_floor_segment(seg.reflect(normal_vec3D, origin_pt3D))
        return dup_floor

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> SpaceFloor
        """Scale the SpaceFloor by a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        Returns:
            A new SpaceFloor object with the scaling applied.
        """
        dup_floor = self.duplicate(_include_floor_segments=False)
        if self.geometry:
            dup_floor.geometry = self.geometry.scale(scale_factor, origin_pt3D)
        for seg in self.floor_segments:
            dup_floor.add_floor_segment(seg.scale(scale_factor, origin_pt3D))
        return dup_floor

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
        self.geometry = []  # type: List[LBFace3D]

    @property
    def net_volume(self):
        # type: () -> float
        """The Interior Net Volume (Vn50)."""
        return self.net_floor_area * self.avg_ceiling_height

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
    def net_floor_area(self):
        # type: () -> float
        """The total net floor area of all floor segments in the Volume"""
        return self.floor.net_floor_area

    @property
    def weighted_net_floor_area(self):
        # type: () -> float
        """The total net floor area of all floor segments in the Volume, weighted by any reduction factors (iFCA, TFA)"""
        return self.floor.weighted_net_floor_area

    @property
    def reference_points(self):
        # type() -> list[Point3D]
        """Returns the Volume's FloorSegment reference points (center)."""
        return self.floor.reference_points

    @property
    def floor_segment_surfaces(self):
        # type: () -> List[Optional[LBFace3D]]
        return [flr_seg.geometry for flr_seg in self.floor.floor_segments]

    @property
    def floor_segments(self):
        # type: () -> List[SpaceFloorSegment]
        return self.floor.floor_segments

    def clear_volume_geometry(self):
        # type: () -> None
        """Delete all the geometry from the SpaceVolume."""
        self.geometry = []

    def __copy__(self, _include_floor=True):
        # type: (bool) -> SpaceVolume
        new_volume = SpaceVolume()

        new_volume.identifier = self.identifier
        new_volume.display_name = self.display_name
        new_volume.user_data = self.user_data
        new_volume.avg_ceiling_height = self.avg_ceiling_height

        if _include_floor:
            new_volume.floor = self.floor.duplicate()

        if self.geometry:
            new_volume.geometry = [copy(geo) for geo in self.geometry]

        return new_volume

    def duplicate(self, _include_floor=True):
        # type: (bool) -> SpaceVolume
        return self.__copy__(_include_floor)

    def to_dict(self, include_mesh=False, *args, **kwargs):
        # type: (bool, list, dict) -> Dict[str, Any]
        d = {}  # type: dict[str, Any]

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)

        d["avg_ceiling_height"] = self.avg_ceiling_height
        d["floor"] = self.floor.to_dict(include_mesh)
        d["geometry"] = []
        for geom in self.geometry:
            g_dict = geom.to_dict()  # type: dict[str, Any]
            if include_mesh:
                g_dict["mesh"] = geom.triangulated_mesh3d.to_dict()
            d["geometry"].append(g_dict)

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
            new_obj.geometry.append(LBFace3D.from_dict(geom_dict))

        return new_obj

    def move(self, moving_vec3D):
        # type: (Vector3D) -> SpaceVolume
        """Move the SpaceVolume along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        Returns:
            A new SpaceVolume object with the move applied.
        """
        dup_volume = self.duplicate(_include_floor=False)
        dup_volume.geometry = [f.move(moving_vec3D) for f in self.geometry]
        dup_volume.floor = self.floor.move(moving_vec3D)
        return dup_volume

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> SpaceVolume
        """Rotate the SpaceVolume by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new SpaceVolume object with the rotation applied.
        """
        dup_volume = self.duplicate(_include_floor=False)
        dup_volume.geometry = [f.rotate(axis_vec3D, radians(angle_degrees), origin_pt3D) for f in self.geometry]
        dup_volume.floor = self.floor.rotate(axis_vec3D, angle_degrees, origin_pt3D)
        return dup_volume

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> SpaceVolume
        """Rotate the SpaceVolume counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new SpaceVolume object with the rotation applied.
        """
        dup_volume = self.duplicate(_include_floor=False)
        dup_volume.geometry = [f.rotate_xy(radians(angle_degrees), origin_pt3D) for f in self.geometry]
        dup_volume.floor = self.floor.rotate_xy(angle_degrees, origin_pt3D)
        return dup_volume

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> SpaceVolume
        """Reflected the SpaceVolume across a plane with the input normal vector and origin_pt3D.

        Args:
            normal_vec3D: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin_pt3D: A Point3D representing the origin_pt3D from which to reflect.
        Returns:
            A new SpaceVolume object with the reflection applied.
        """
        dup_volume = self.duplicate(_include_floor=False)
        dup_volume.geometry = [f.reflect(normal_vec3D, origin_pt3D) for f in self.geometry]
        dup_volume.floor = self.floor.reflect(normal_vec3D, origin_pt3D)
        return dup_volume

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> SpaceVolume
        """Scale the SpaceVolume by a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        Returns:
            A new SpaceVolume object with the scaling applied.
        """
        dup_volume = self.duplicate(_include_floor=False)
        dup_volume.geometry = [f.scale(scale_factor, origin_pt3D) for f in self.geometry]
        dup_volume.avg_ceiling_height = self.avg_ceiling_height * scale_factor
        dup_volume.floor = self.floor.scale(scale_factor, origin_pt3D)
        return dup_volume

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Space(_base._Base):
    def __init__(self, _host=None):
        # type: (Optional[room.Room]) -> None
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
        """The total interior net volume of all Volumes in the Space."""
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
    def net_floor_area(self):
        # type: () -> float
        """The total net floor area of all floor segments in the Space"""
        return sum((vol.net_floor_area for vol in self.volumes))

    @property
    def weighted_net_floor_area(self):
        # type: () -> float
        """The total net floor area of all floor segments in the Space, weighted by any reduction factors (iFCA, TFA)"""
        return sum((vol.weighted_net_floor_area for vol in self.volumes))

    @property
    def average_floor_weighting_factor(self):
        # type: () -> float
        """Returns the average weighting factor (TFA/iCFA) for the Space's floor-segments."""
        return self.weighted_floor_area / self.floor_area

    @property
    def average_floor_net_area_factor(self):
        # type: () -> float
        """Returns the average net area factor for the Space's floor-segments."""
        return self.net_floor_area / self.floor_area

    @property
    def reference_points(self):
        # type: () -> list[Point3D]
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
        # type: () -> List[List[Optional[LBFace3D]]]
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

    def clear_volumes(self):
        # type: () -> None
        """Delete all the Volumes from the Space."""
        self._volumes = []

    def __copy__(self, _host=None, _include_volumes=True):
        # type: (Any, bool) -> Space
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
        new_space.properties._duplicate_extension_attr(self.properties)
        if _include_volumes:
            new_space.add_new_volumes([vol.duplicate() for vol in self.volumes])

        return new_space

    def duplicate(self, _host=None, _include_volumes=True):
        # type: (Any, bool) -> Space
        return self.__copy__(_host, _include_volumes)

    def to_dict(self, include_mesh=False, *args, **kwargs):
        # type: (bool, list, dict) -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["quantity"] = self.quantity
        d["wufi_type"] = self.wufi_type
        d["name"] = self.name
        d["number"] = self.number
        d["volumes"] = [vol.to_dict(include_mesh) for vol in self.volumes]
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
        new_obj.add_new_volumes([SpaceVolume.from_dict(d) for d in _input_dict["volumes"]])
        new_obj.properties = SpaceProperties.from_dict(_input_dict["properties"], _host=new_obj)
        new_obj.properties._load_extension_attr_from_dict(_input_dict["properties"])
        return new_obj

    def move(self, moving_vec3D):
        # type: (Vector3D) -> Space
        """Move the Space and its Volumes along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        Returns:
            A new Space object with the move applied.
        """
        dup_space = self.duplicate(self.host, _include_volumes=False)
        dup_space.add_new_volumes([vol.move(moving_vec3D) for vol in self.volumes])
        dup_space.properties.move(moving_vec3D)
        return dup_space

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> Space
        """Rotate the Space and its Volumes by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new Space object with the rotation applied.
        """
        dup_space = self.duplicate(self.host, _include_volumes=False)
        dup_space.add_new_volumes([vol.rotate(axis_vec3D, angle_degrees, origin_pt3D) for vol in self.volumes])
        dup_space.properties.rotate(axis_vec3D, angle_degrees, origin_pt3D)
        return dup_space

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> Space
        """Rotate the Space and its Volumes counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        Returns:
            A new Space object with the rotation applied.
        """
        dup_space = self.duplicate(self.host, _include_volumes=False)
        dup_space.add_new_volumes([vol.rotate_xy(angle_degrees, origin_pt3D) for vol in self.volumes])
        dup_space.properties.rotate_xy(angle_degrees, origin_pt3D)
        return dup_space

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> Space
        """Reflected the Space and its Volumes across a plane with the input normal vector and origin_pt3D.

        Args:
            normal_vec3D: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin_pt3D: A Point3D representing the origin_pt3D from which to reflect.
        Returns:
            A new Space object with the reflection applied.
        """
        dup_space = self.duplicate(self.host, _include_volumes=False)
        dup_space.add_new_volumes([vol.reflect(normal_vec3D, origin_pt3D) for vol in self.volumes])
        dup_space.properties.reflect(normal_vec3D)
        return dup_space

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> Space
        """Scale the Space and its Volumes by a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        Returns:
            A new Space object with the scaling applied.
        """
        dup_space = self.duplicate(self.host, _include_volumes=False)
        dup_space.add_new_volumes([volume.scale(scale_factor, origin_pt3D) for volume in self.volumes])
        dup_space.properties.scale(scale_factor, origin_pt3D)
        return dup_space

    def __str__(self):
        return "{}(name={!r}, number={!r}, volumes={!r})".format(
            self.__class__.__name__, self.name, self.number, self.volumes
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
