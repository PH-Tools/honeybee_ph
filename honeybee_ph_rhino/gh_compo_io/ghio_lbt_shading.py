# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for Calculating Window shading factors using Ladybug's Incident Radiation solver."""

import math
try:
    from itertools import izip as zip
except:
    pass  # Python3

try:
    from typing import Any, List, Collection, Tuple, Optional
except ImportError:
    pass  # IronPython

try:
    from System import Object
except ImportError:
    pass

try:
    import Rhino.Geometry as rg
except ImportError:
    pass

try:
    from Grasshopper import DataTree
    from Grasshopper.Kernel.Data import GH_Path
except ImportError:
    pass

try:
    from ladybug.viewsphere import view_sphere
    from ladybug.graphic import GraphicContainer
except ImportError as e:
    raise ImportError("\nFailed to import ladybug:\n\t{}".format(e))

try:
    from ladybug_rhino.togeometry import to_joined_gridded_mesh3d
    from ladybug_rhino.fromgeometry import from_mesh3d, from_point3d, from_vector3d
    from ladybug_geometry.geometry3d import Mesh3D
    from ladybug_rhino.fromobjects import legend_objects
    from ladybug_rhino.text import text_objects
    from ladybug_rhino.intersect import intersect_mesh_rays
    from ladybug_rhino.grasshopper import de_objectify_output
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_rhino:\n\t{}".format(e))

from honeybee_ph_rhino.gh_compo_io import ghio_win_shade_surfaces
from honeybee_ph_utils import sky_matrix

# Radiation and Shading Factor Calcs
# -----------------------------------------------------------------------------


def create_shading_mesh(_bldg_shading_breps, _mesh_params):
    # type: (Collection[rg.Brep], rg.MeshingParameters) -> rg.Mesh
    """Return a single new Rhino.Geometry.Mesh built from all the input shading surface Breps."""

    shade_mesh = rg.Mesh()
    for brep in _bldg_shading_breps:
        new_mesh = rg.Mesh.CreateFromBrep(brep, _mesh_params)
        if new_mesh:
            shade_mesh.Append(new_mesh)
        else:
            srfc_name = brep.GetUserStrings().Get("display_name")
            msg = (
                "Error: Something is wrong with surface: {}. \n"
                "Cannot create a mesh properly for some reason. \n"
                "Check that all your geometry is correct with no overlaps or voids \n"
                "and check that the Honeybee surfaces are all being created correctly? \n"
                "If that surface has windows hosted on it, be sure the windows are not \n"
                "overlapping and that they are being generated correctly?".format(
                    srfc_name)
            )
            raise Exception(msg)

    return shade_mesh


def deconstruct_sky_matrix(_sky_mtx):
    # type: (ladybug_rhino.grasshopper.Objectifier) -> Tuple[List[rg.Vector3d], List[float]]
    """Copied from Ladybug 'IncidentRadiation' Component

    Arguments:
    ----------
        * _sky_mtx: A Ladybug Sky Matrix for the season

    Returns:
    --------
        * [Tuple]
            - [0] sky_vecs: (List[rg.Vector3d])
            - [1] total_sky_rad: (list[float])
    """

    mtx = de_objectify_output(_sky_mtx)
    total_sky_rad = [dir_rad + dif_rad for dir_rad, dif_rad in zip(mtx[1], mtx[2])]
    lb_vecs = (
        view_sphere.tregenza_dome_vectors
        if len(total_sky_rad) == 145
        else view_sphere.reinhart_dome_vectors
    )
    if mtx[0][0] != 0:  # there is a north input for sky; rotate vectors
        north_angle = math.radians(mtx[0][0])
        lb_vecs = [vec.rotate_xy(north_angle) for vec in lb_vecs]
    sky_vecs = [from_vector3d(vec) for vec in lb_vecs]

    return (sky_vecs, total_sky_rad)


def build_window_meshes(_window_surface, _grid_size, _mesh_params):
    """Create the Ladybug Mesh3D grided mesh for the window being analyzed

    Arguments:
        _window_surface: (Brep) A single window Brep from the scene
        _grid_size: (float)
        _mesh_params: (Rhino.Geometry.MeshingParameters)
    Returns: (tuple)
        points: (list: Ladybug Point3D) All the analysis points on the window
        normals: (list: Ladybug Normal) All the normals for the analysis points
        window_mesh: (ladybug_geometry.geometry3d.Mesh3D) The window
        window_back_mesh: (ladybug_geometry.geometry3d.Mesh3D) A copy of the window shifted 'back'
        just a little bit (0.1 units). Used when solving the 'unshaded' situation.
    """

    # create the gridded mesh for the window surface
    # ---------------------------------------------------------------------------
    offset_dist = 0.001
    window_mesh = to_joined_gridded_mesh3d([_window_surface], _grid_size, offset_dist)
    window_rh_mesh = from_mesh3d(window_mesh)
    points = [from_point3d(pt) for pt in window_mesh.face_centroids]

    # Create a 'back' for the window
    # ---------------------------------------------------------------------------
    # Mostly this is done so it can be passed to the ladybug_rhino.intersect.intersect_mesh_rays()
    # solver as a surfce which is certain to *not* shade the window at all
    window_back_mesh = None
    for sr in _window_surface.Surfaces:
        window_normal = sr.NormalAt(0.5, 0.5)
        window_normal.Unitize()
        window_normal = window_normal * -1 * 0.1

        window_back = _window_surface.Duplicate()
        window_back.Translate(window_normal)
        window_back_mesh = rg.Mesh.CreateFromBrep(
            window_back, _mesh_params
        )[0]

    normals = [from_vector3d(vec) for vec in window_mesh.face_normals]

    return points, normals, window_mesh, window_back_mesh, window_rh_mesh


def generate_intersection_data(
    _shade_mesh, _win_mesh_back, _points, _sky_vecs, _normals, _cpu_count
):
    """Creates all the Intersection Matrix data for both the Shaded and the UNShaded conditions

    Note that for the 'Unshaded' case you still have to pass the solver *something*, so
    the _win_mesh_back is used for this case. This surface should block out any radiation coming from
    'behind' and also not interfere with the front-side radiation calculation.

    Adapted from Ladybug 'IncidentRadiation' Component

    Arguments:
        _shade_mesh: (Mesh) The context shading joined mesh
        _win_mesh_back: (Mesh) The window surface pushed 'back' a little.
        _points: (_)
        _sky_vecs: (_)
        _normals: (list: Ladybug Normals)
        _parallel: (int | None)
    Returns: (tuple)
        int_matrix_init_shaded: Intersection Matrix for window WITH shading
        int_matrix_init_unshaded: Intersection Matrix for window WITHOUT shading
        angles_s: Shaded
        angles_u: UN-Shaded
    """

    # intersect the rays with the mesh
    # ---------------------------------------------------------------------------
    int_matrix_init_shaded, angles_s = intersect_mesh_rays(
        _shade_mesh, _points, _sky_vecs, _normals, _cpu_count
    )

    int_matrix_init_unshaded, angles_u = intersect_mesh_rays(
        _win_mesh_back, _points, _sky_vecs, _normals, _cpu_count
    )

    return int_matrix_init_shaded, int_matrix_init_unshaded, angles_s, angles_u


def calc_win_radiation(_int_matrix_init, _angles, _total_sky_rad, _window_mesh):
    """Computes total kWh per window based on the int_matrix and sky vec angles

    Arguments:
        _int_matrix_init: (_)
        _angles: (_)
        _total_sky_rad: (_)
        _window_mesh: (ladybug_geometry.geometry3d.Mesh3D)
    Returns: (tuple)
        average_window_kWh: (float) The area-weighted average total kWh radiation
        for the window over the analysis period specified.
    """

    results_kWh = []
    window_face_areas = []
    int_matrix = []

    count = (k for k in range(len(_angles) * 10))  # just a super large counter

    for c, int_vals, angs in zip(count, _int_matrix_init, _angles):
        pt_rel = (ival * math.cos(ang) for ival, ang in zip(int_vals, angs))
        rad_result = sum(r * w for r, w in zip(pt_rel, _total_sky_rad))

        int_matrix.append(pt_rel)
        results_kWh.append(rad_result * _window_mesh.face_areas[c])
        window_face_areas.append(_window_mesh.face_areas[c])

    return results_kWh, window_face_areas


# Legend and Graphics
# -----------------------------------------------------------------------------


def create_graphic_container(_season, _data, _study_mesh, _legend_par):
    """Creates the Ladybug 'Graphic' Object from the result data

    Copied from Ladybug 'IncidentRadiation' Component

    Arguments:
        _season: (str) 'Winter' or 'Summer'. Used in the title.
        _data: (list: float:) A list of the result data to use to color / style the output
        _study_mesh: (ladybug_geometry.geometry3d.Mesh3D) The joined Mesh used in the analysis
        _legend_par: Ladybug Legend Parameters
    Returns: (tuple)
        graphic: (ladybug.graphic.GraphicContainer) The Ladybug Graphic Object
        title: The text title
    """

    graphic = GraphicContainer(_data, _study_mesh.min, _study_mesh.max, _legend_par)
    graphic.legend_parameters.title = "kWh"

    title = text_objects(
        "{} Incident Radiation".format(_season),
        graphic.lower_title_location,
        graphic.legend_parameters.text_height * 1.5,
        graphic.legend_parameters.font,
    )

    return graphic, title


def create_window_mesh(_lb_meshes):
    return Mesh3D.join_meshes(_lb_meshes)


def create_rhino_mesh(_graphic, _lb_mesh):
    """Copied from Ladybug 'IncidentRadiation' Component

    Arguments:
        _graphic: (ladybug.graphic.GraphicContainer) The Ladybug Graphic object
        _lb_mesh: (Ladybug Mesh) A single joined mesh of the entire scene
    Returns: (tuple)
        mesh: (_)
        legend: (_)
    """

    # Create all of the visual outputs

    _lb_mesh.colors = _graphic.value_colors
    mesh = from_mesh3d(_lb_mesh)
    legend = legend_objects(_graphic.legend)

    return mesh, legend


# Component Interface
# -----------------------------------------------------------------------------
class HBPH_LBTRadSettings:
    """LBT Radiation Solver Settings."""

    def __init__(self,  _wsm, _ssm, _mshp, _gs, _lgp, _cpus):
        # type: (Any, Any, rg.MeshingParameters, float, Any, Optional[int]) -> None
        self.winter_sky_matrix = _wsm
        self.summer_sky_matrix = _ssm
        self.mesh_params = _mshp
        self.grid_size = _gs
        self.legend_par = _lgp
        self.cpus = _cpus

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class IShadingLBTRadiationSettings(object):
    """Interface for LBT Radiation Solver Settings."""

    # -- Defaults
    winter_period = (10, 3)  # October 1 to March 31
    summer_period = (6, 9)  # June 1 to September 30'

    def __init__(self, _epw_file, _north, _winter_sky_matrix, _summer_sky_matrix,
                 _mesh_params, _grid_size, _legend_par, _cpus):
        # type: (str, float, Any, Any, rg.MeshingParameters, float, Any, Optional[int]) -> None
        self.epw_file = _epw_file
        self.winter_sky_matrix = _winter_sky_matrix or sky_matrix.gen_matrix(
            self.epw_file, self.winter_period, _north)
        self.summer_sky_matrix = _summer_sky_matrix or sky_matrix.gen_matrix(
            self.epw_file, self.summer_period, _north)
        self.mesh_params = _mesh_params or rg.MeshingParameters.Default
        self.grid_size = _grid_size or 1.0
        self.legend_par = _legend_par or None
        self.cpus = _cpus or None

    def create_hbph_obj(self):
        hbph_obj = HBPH_LBTRadSettings(
            self.winter_sky_matrix,
            self.summer_sky_matrix,
            self.mesh_params,
            self.grid_size,
            self.legend_par,
            self.cpus
        )
        return hbph_obj


class IShadingLBTRadiation(object):

    def __init__(self,
                 _settings,
                 _shading_surfaces_winter,
                 _shading_surfaces_summer,
                 _hb_rooms,
                 ):
        # type: (Any, List, List, List) -> None
        self.settings = _settings
        self.shading_surfaces_winter = _shading_surfaces_winter
        self.shading_surfaces_summer = _shading_surfaces_summer
        self.hb_rooms = _hb_rooms

    def run(self):
        hb_rooms_ = []

        # -- Create context Shade meshes
        # ---------------------------------------------------------------------
        shade_mesh_winter = create_shading_mesh(
            self.shading_surfaces_winter,
            self.settings.mesh_params
        )
        shade_mesh_summer = create_shading_mesh(
            self.shading_surfaces_summer,
            self.settings.mesh_params
        )

        # Deconstruct the sky-matrix and get the sky dome vectors. Winter (w) and Summer (s)
        # ---------------------------------------------------------------------
        w_sky_vecs, w_total_sky_rad = deconstruct_sky_matrix(
            self.settings.winter_sky_matrix)
        s_sky_vecs, s_total_sky_rad = deconstruct_sky_matrix(
            self.settings.summer_sky_matrix)

        # Calc window surface shaded and unshaded radiation
        # ---------------------------------------------------------------------
        lb_window_meshes = []
        winter_radiation_shaded_ = DataTree[Object]()
        winter_radiation_shaded_detailed_ = DataTree[Object]()
        winter_radiation_unshaded_ = DataTree[Object]()
        summer_radiation_shaded_ = DataTree[Object]()
        summer_radiation_shaded_detailed_ = DataTree[Object]()
        summer_radiation_unshaded_ = DataTree[Object]()
        mesh_by_window = DataTree[Object]()

        win_count = 0
        for room in self.hb_rooms:
            new_room = room.duplicate()

            for face in new_room.faces:
                for aperture in face.apertures:
                    window_surface = ghio_win_shade_surfaces.create_inset_aperture_surface(
                        aperture)

                    # Build the meshes
                    # ----------------------------------------------------------------------
                    pts, nrmls, win_msh, win_msh_bck, rh_msh = build_window_meshes(
                        window_surface, self.settings.grid_size, self.settings.mesh_params)
                    lb_window_meshes.append(win_msh)

                    # Solve Winter
                    # ----------------------------------------------------------------------
                    args_winter = (shade_mesh_winter, win_msh_bck, pts,
                                   w_sky_vecs, nrmls, self.settings.cpus)

                    int_matrix_s, int_matrix_u, angles_s, angles_u = generate_intersection_data(
                        *args_winter)
                    w_rads_shaded, face_areas = calc_win_radiation(
                        int_matrix_s, angles_s, w_total_sky_rad, win_msh)
                    w_rads_unshaded, face_areas = calc_win_radiation(
                        int_matrix_u, angles_u, w_total_sky_rad, win_msh)

                    winter_rad_shaded = sum(w_rads_shaded)/sum(face_areas)
                    winter_rad_unshaded = sum(w_rads_unshaded)/sum(face_areas)

                    winter_radiation_shaded_detailed_.AddRange(
                        w_rads_shaded, GH_Path(win_count))
                    winter_radiation_shaded_.Add(winter_rad_shaded, GH_Path(win_count))
                    winter_radiation_unshaded_.Add(
                        winter_rad_unshaded, GH_Path(win_count))

                    # Solve Summer
                    # ----------------------------------------------------------------------
                    args_summer = (shade_mesh_summer, win_msh_bck, pts,
                                   s_sky_vecs, nrmls, self.settings.cpus)

                    int_matrix_s, int_matrix_u, angles_s, angles_u = generate_intersection_data(
                        *args_summer)
                    s_rads_shaded, face_areas = calc_win_radiation(
                        int_matrix_s, angles_s, s_total_sky_rad, win_msh)
                    s_rads_unshaded, face_areas = calc_win_radiation(
                        int_matrix_u, angles_u, s_total_sky_rad, win_msh)

                    summer_rad_shaded = sum(s_rads_shaded)/sum(face_areas)
                    summer_rad_unshaded = sum(s_rads_unshaded)/sum(face_areas)

                    summer_radiation_shaded_detailed_.AddRange(
                        s_rads_shaded, GH_Path(win_count))
                    summer_radiation_shaded_.Add(summer_rad_shaded, GH_Path(win_count))
                    summer_radiation_unshaded_.Add(
                        summer_rad_unshaded, GH_Path(win_count))

                    mesh_by_window.Add(rh_msh, GH_Path(win_count))

                    # Set the aperture shading factors
                    # ----------------------------------------------------------------------
                    aperture.properties.ph.winter_shading_factor = winter_rad_shaded / winter_rad_unshaded
                    aperture.properties.ph.summer_shading_factor = summer_rad_shaded / summer_rad_unshaded

                    win_count += 1

            # -- Add the new room to the output set
            # ----------------------------------------------------------------------
            hb_rooms_.append(new_room)

        # Create the mesh and legend outputs
        # --------------------------------------------------------------------------
        # Flatten the radiation data trees
        winter_rad_vals = [
            item for branch in winter_radiation_shaded_detailed_.Branches for item in branch]
        summer_rad_vals = [
            item for branch in summer_radiation_shaded_detailed_.Branches for item in branch]

        # Create the single window Mesh
        joined_window_mesh = create_window_mesh(lb_window_meshes)

        winter_graphic, title = create_graphic_container(
            'Winter', winter_rad_vals, joined_window_mesh, self.settings.legend_par)
        winter_radiation_shaded_mesh_, legend_ = create_rhino_mesh(
            winter_graphic, joined_window_mesh)

        summer_graphic, title = create_graphic_container(
            'Summer', summer_rad_vals, joined_window_mesh, self.settings.legend_par)
        summer_radiation_shaded_mesh_, legend_ = create_rhino_mesh(
            summer_graphic, joined_window_mesh)

        return legend_, winter_radiation_shaded_mesh_, summer_radiation_shaded_mesh_, hb_rooms_
