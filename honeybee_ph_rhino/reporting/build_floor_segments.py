# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for getting / sorting all the Honeybee-Model TFA Floor Surfaces."""

try:
    from typing import Tuple, List, Dict, Optional, Callable
except ImportError:
    pass  # Python 2.7

try:
    from System import Object
    from System.Drawing import Color
except ImportError:
    pass  # Outside .NET

try:
    from Rhino.DocObjects import ObjectAttributes
    from Rhino.Geometry import Brep, Point3d, Vector3d, Line
except ImportError:
    pass  # Outside Rhino

from collections import defaultdict, OrderedDict

from honeybee import model, room, facetype
from ladybug_rhino.fromgeometry import from_face3d, from_point3d

from honeybee_ph_rhino import gh_io
from honeybee_ph import space
from honeybee_ph_rhino.reporting.annotations import TextAnnotation


class ClippingPlaneLocation(object):
    """Temporary object to store Clipping Plane location and direction data."""

    def __init__(self, _origin, _normal):
        # type: (Point3d, Vector3d) -> None
        self.origin = _origin
        self.normal = _normal

    def __str__(self):
        return '{}(origin={}, normal={})'.format(self.__class__.__name__, self.origin, self.normal)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


# -----------------------------------------------------------------------------
# -- Styles
def color_by_TFA(_flr_seg, _space):
    # type: (space.SpaceFloorSegment, space.Space) -> Color
    """Return a System.Drawing.Color based on the TFA Weighting factor of the SpaceFloorSegment."""

    if _flr_seg.weighting_factor > 0.6:
        return Color.FromArgb(255, 252, 252, 139)  # Yellow
    elif 0.5 < _flr_seg.weighting_factor <= 0.6:
        return Color.FromArgb(255, 227, 201, 168)  # Brown
    elif 0.3 < _flr_seg.weighting_factor <= 0.5:
        return Color.FromArgb(255, 213, 247, 143)  # Green
    elif 0.0 < _flr_seg.weighting_factor <= 0.3:
        return Color.FromArgb(255, 173, 247, 223)  # Blue
    else:
        return Color.FromArgb(255, 252, 182, 252)  # Purple


def color_by_Vent(_flr_seg, _space):
    # type: (space.SpaceFloorSegment, space.Space) -> Color
    """Return a System.Drawing.Color based on the Ventilation Air Flow Rate of the Space"""

    if _space.properties.ph._v_sup > 0 and _space.properties.ph._v_eta > 0:
        return Color.FromArgb(255, 234, 192, 240)  # Balanced
    elif _space.properties.ph._v_sup > 0:
        return Color.FromArgb(255, 183, 227, 238)  # Supply Only
    elif _space.properties.ph._v_eta > 0:
        return Color.FromArgb(255, 246, 170, 154)  # Extract Only
    else:
        return Color.FromArgb(255, 235, 235, 235)  # No Vent Flow


def text_by_TFA(_space):
    """Return the space data in a formatted block."""

    txt = [
        'ZONE: {}'.format(_space.host.display_name),
        'NAME: {}'.format(_space.full_name),
        'GROSS AREA: {:.01f} m2'.format(_space.floor_area),
        'WEIGHTED AREA: {:.01f} m2'.format(_space.weighted_floor_area),
        'Vn50: {:.01f} m3'.format(_space.net_volume),
        'CLG HEIGHT: {:.01f} m'.format(_space.avg_clear_height),
    ]

    return "\n".join(txt)


def text_by_Vent(_space):
    """Return the space data in a formatted block."""

    txt = [
        'ZONE: {}'.format(_space.host.display_name),
        'NAME: {}'.format(_space.full_name),
        'GROSS AREA: {:.01f} m2'.format(_space.floor_area),
        'SUP: {:.0f} m3/hr'.format(_space.properties.ph._v_sup * 3600),
        'ETA: {:.0f} m3/hr'.format(_space.properties.ph._v_eta * 3600),
        'TRAN: {:.0f} m3/hr'.format(_space.properties.ph._v_tran * 3600),
    ]

    return "\n".join(txt)


# -----------------------------------------------------------------------------


def _get_hbph_spaces(_hb_room_group):
    # type: (List[room.Room]) -> List[space.Space]
    """Return a sorted list of all the HBPH-Spaces in a list of HB-Rooms."""

    spaces = {}
    for room in _hb_room_group:
        for space in room.properties.ph.spaces:
            spaces[space.display_name] = space

    return sorted(list(spaces.values()), key=lambda sp: sp.display_name)


def _sort_rooms_by_z_location(_hb_model):
    # type: (model.Model) -> Dict[str, List[room.Room]]
    """Return a Dict with the HB-Rooms grouped by their floor's Z-height."""

    rooms_by_z_height = defaultdict(list)
    for hb_room in _hb_model.rooms:
        flr_srfcs = [f for f in hb_room.faces if (isinstance(f.type, facetype.Floor))]
        floor_srfcs_min_z = round(min(hb_face.min.z for hb_face in flr_srfcs), 3)
        rooms_by_z_height[str(floor_srfcs_min_z)].append(hb_room)

    # -- Sort the room groups by their Key (which is their Z-dist)
    sorted_rooms_grouped_by_story = OrderedDict()
    for k in sorted(rooms_by_z_height.keys(), key=lambda k: float(k)):
        sorted_rooms_grouped_by_story[k] = rooms_by_z_height[k]

    return sorted_rooms_grouped_by_story


def _group_hb_rooms_by_story(_hb_model):
    # type: (model.Model) -> Dict[str, List[room.Room]]
    """Return a Dict with the HB-Rooms grouped by their 'Story'.

    If the HB-Story data is not applied, will attempt to sort the HB-Rooms based
    on their Z-height instead.
    """

    # -- If the model is missing 'Story' data, sort by floor Z-location
    if not all(hb_room.story for hb_room in _hb_model.rooms):
        return _sort_rooms_by_z_location(_hb_model)

    # -- If model has Story data, just use that instead.
    rooms_grouped_by_story = defaultdict(list)
    for hb_room in _hb_model.rooms:
        rooms_grouped_by_story[hb_room.story].append(hb_room)

    # -- Sort the room groups by their Key (which is their Story name)
    sorted_rooms_grouped_by_story = OrderedDict()
    for k in sorted(rooms_grouped_by_story.keys()):
        sorted_rooms_grouped_by_story[k] = rooms_grouped_by_story[k]

    return sorted_rooms_grouped_by_story


def _build_rh_attrs(_IGH, _color, _weight=0.5, _draw_order=None):
    # type: (gh_io.IGH, Color, float, Optional[int]) -> ObjectAttributes

    new_attr_obj = _IGH.Rhino.DocObjects.ObjectAttributes()

    new_attr_obj.ObjectColor = _color
    new_attr_obj.PlotColor = _color
    new_attr_obj.ColorSource = _IGH.Rhino.DocObjects.ObjectColorSource.ColorFromObject
    new_attr_obj.PlotColorSource = _IGH.Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject

    new_attr_obj.PlotWeight = _weight
    new_attr_obj.PlotWeightSource = _IGH.Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject

    if _draw_order:
        new_attr_obj.DisplayOrder = _draw_order  # 1 = Front, -1 = Back

    return new_attr_obj


def _get_flr_seg_data(_IGH, _get_color, _space):
    # type: (gh_io.IGH, Callable, space.Space) -> Tuple[List, List]
    """Return a Tuple of Lists with the Geometry and the ObjectAttributes."""

    flr_seg_geom_ = []  # type: List[Optional[Brep]]
    flr_sef_attrs_ = []  # type: List[ObjectAttributes]

    # -- Build the outline curve attr
    crv_attr = _build_rh_attrs(_IGH, Color.FromArgb(255, 40, 40, 40), 0.5)

    for volume in _space.volumes:
        for flr_seg in volume.floor.floor_segments:
            # -- Object Attributes
            rh_attr = _build_rh_attrs(_IGH, _get_color(flr_seg, _space))

            # -- Geometry as Mesh
            brp = from_face3d(flr_seg.geometry)
            msh = _IGH.ghpythonlib_components.MeshColours(brp, rh_attr.ObjectColor)
            flr_seg_geom_.append(msh)
            flr_sef_attrs_.append(rh_attr)

            # -- Boundary Edges
            msh_edges = _IGH.ghpythonlib_components.MeshEdges(msh).naked_edges
            msh_boundary = _IGH.ghpythonlib_components.JoinCurves(
                msh_edges, preserve=False)
            flr_seg_geom_.append(msh_boundary)
            flr_sef_attrs_.append(crv_attr)

    return flr_seg_geom_, flr_sef_attrs_


def _get_clipping_plane_locations(_IGH, _room_group, _offset_up=0.5, _offset_down=0.5):
    # type: (gh_io.IGH, List[room.Room], float, float) -> Tuple[ClippingPlaneLocation, ClippingPlaneLocation]
    """Return a pair of ClippingPlaneLocation objects. One pointing 'up' and the other 'down'.

    These are used to clip the scene local to the floor-plan being printed.
    """

    # -- Find the Min Z-location of the Floor-Faces of the Room-Group
    flr_faces = [f
                 for rm in _room_group
                 for f in rm.faces if (
                     isinstance(f.type, facetype.Floor)
                 )]
    flr_level_z = min(hb_face.min.z for hb_face in flr_faces)

    # --Create the clipping plane location objects up/down from that level.
    upper_clipping_plane = ClippingPlaneLocation(
        _IGH.Rhino.Geometry.Point3d(0, 0, flr_level_z+_offset_up),
        _IGH.Rhino.Geometry.Vector3d(0, 0, -1)
    )
    lower_clipping_plane = ClippingPlaneLocation(
        _IGH.Rhino.Geometry.Point3d(0, 0, flr_level_z-_offset_down),
        _IGH.Rhino.Geometry.Vector3d(0, 0, 1)
    )

    return upper_clipping_plane, lower_clipping_plane


def _find_space_annotation_location(_IGH, _space):
    # type: (gh_io.IGH, space.Space) -> Point3d
    """Returns a single geometric center point of a Space's Volumes."""
    return _IGH.ghpythonlib_components.Average([from_point3d(p) for p in _space.reference_points])


def _get_all_space_floor_segment_center_points(_IGH, space):
    # type: (gh_io.IGH, space.Space) -> List[Point3d]
    """Return a list of all the SpaceFloorSegment center-points in the Space's Volumes."""

    return [
        from_point3d(flr_seg.geometry.center)
        for volume in space.volumes
        for flr_seg in volume.floor.floor_segments
    ]


def _build_annotation_leader_line(_IGH, _pt1, _pt2):
    # type: (gh_io.IGH, Point3d, Point3d) -> Tuple[Line, ObjectAttributes]
    """Return a new LeaderLine and ObjectAttributes"""

    rh_geom = _IGH.Rhino.Geometry.Line(_pt1, _pt2)
    rh_attr = _build_rh_attrs(_IGH, Color.FromArgb(255, 0, 0, 0), 0.05)

    return rh_geom, rh_attr


def _build_annotation_leader_marker(_IGH, _cp, _radius=0.0075):
    # type: (gh_io.IGH, Point3d, float) -> Tuple
    """Return a new 'dot' mesh and ObjectAttributes"""

    rh_attr = _build_rh_attrs(_IGH, Color.FromArgb(255, 0, 0, 0), 0.5, 1)

    c = _IGH.ghpythonlib_components.Circle(_cp, _radius)
    brp = _IGH.ghpythonlib_components.BoundarySurfaces(c)
    rh_geom = _IGH.ghpythonlib_components.MeshColours(brp, rh_attr.ObjectColor)

    return rh_geom, rh_attr


# -----------------------------------------------------------------------------

def create_flr_segment_data(_IGH, _hb_model, _get_color, _create_annotation_text, _units):
    # type: (gh_io.IGH, model.Model, Callable, Callable, str) -> Tuple
    """Create the SpaceFloorSegment geometry, attributes and text-annotations for a Floor Plan view.

    Arguments:
    ----------
        * _IGH (gh_io.IGH): Grasshopper Interface.
        * _hb_model (model.Model): The Honeybee-Model to use as the source.
        * _get_color (Callable): The function which returns the floor-segment color.
        * _create_annotation_text (Callable): The function which returns the annotation text.
        * _units (str): IP or SI units

    Returns:
    --------
        * Tuple[DataTree, DataTree, DataTree, DataTree, DataTree, DataTree]
    """

    # -- Output Trees
    floor_names_ = _IGH.Grasshopper.DataTree[str]()
    clipping_plane_locations_ = _IGH.Grasshopper.DataTree[Object]()
    floor_geom_ = _IGH.Grasshopper.DataTree[Object]()
    floor_attributes_ = _IGH.Grasshopper.DataTree[ObjectAttributes]()
    floor_annotations_ = _IGH.Grasshopper.DataTree[TextAnnotation]()
    pth = _IGH.Grasshopper.Kernel.Data.GH_Path

    if not _hb_model:
        return floor_names_, clipping_plane_locations_, floor_geom_, floor_attributes_, floor_annotations_

    # -- Find the floor levels
    rooms_grouped_by_story = _group_hb_rooms_by_story(_hb_model)
    for i, item in enumerate(rooms_grouped_by_story.items()):
        level_name, hb_rm_group = item
        floor_names_.Add(level_name, pth(i))
        clipping_plane_locations_.AddRange(
            _get_clipping_plane_locations(_IGH, hb_rm_group), pth(i))

        # -- Create space floor Geometry and Annotation
        spaces = _get_hbph_spaces(hb_rm_group)
        for space in spaces:
            #  -- Add the Floor segment geometry
            flr_seg_geom, flr_seg_attrs = _get_flr_seg_data(_IGH, _get_color, space)
            floor_geom_.AddRange(flr_seg_geom, pth(i))
            floor_attributes_.AddRange(flr_seg_attrs, pth(i))

            # -- Add Leader Lines from Annotation to each FloorSegment CenterPoint
            anno_cp = _find_space_annotation_location(_IGH, space)
            flr_seg_cps = _get_all_space_floor_segment_center_points(_IGH, space)
            for flr_cp in flr_seg_cps:
                # -- add the leader line itself
                ldr, ldr_attr = _build_annotation_leader_line(_IGH, anno_cp, flr_cp)
                floor_geom_.Add(ldr, pth(i))
                floor_attributes_.Add(ldr_attr, pth(i))

                # -- add a dot marker at the leader line end point
                marker_geom, marker_attrs = _build_annotation_leader_marker(
                    _IGH, flr_cp, 0.05)
                floor_geom_.Add(marker_geom, pth(i))
                floor_attributes_.Add(marker_attrs, pth(i))

            # -- Add the text Annotation object
            txt_annotation = TextAnnotation(
                _text=_create_annotation_text(space),
                _size=0.02,
                _location=anno_cp,
                _format="{}",
                _justification=4,
                _mask_draw=True,
                _mask_offset=0.02,
                _mask_draw_frame=True,
            )
            floor_annotations_.Add(txt_annotation, pth(i))

    return floor_names_, clipping_plane_locations_, floor_geom_, floor_attributes_, floor_annotations_
