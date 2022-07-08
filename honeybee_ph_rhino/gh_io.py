# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Interface Class. Used to pass Rhino, GH side dependencies to all other classes.

This is done so that other classes can be tested by mocking out this Interface. If I
could figure out how to get Rhino dependencies to be recognized by testing framework,
probably would not need something like this? I suppose it does help reduce coupling?
"""


try:
    from typing import Any, Sequence, Union, List, Dict
except ImportError:
    pass  # Python 3

try:
    from itertools import izip as zip
except ImportError:
    pass  # Python3+

from GhPython import Component

from contextlib import contextmanager
from copy import deepcopy

import honeybee.face
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_rhino.togeometry import (
    to_face3d,
    to_linesegment3d,
    to_mesh3d,
    to_point3d,
    to_polyline3d,
)
from ladybug_rhino.fromgeometry import (
    from_face3d,
    from_linesegment3d,
    from_mesh3d,
    from_point3d,
    from_polyline3d,
)

from honeybee_ph_utils.input_tools import input_to_int, clean_get


class LBTGeometryConversionError(Exception):
    def __init__(self, _in):
        self.message = 'Input Error: Cannot convert "{}" to LBT Geometry.'.format(
            type(_in))

        super(LBTGeometryConversionError, self).__init__(self.message)


class IGH:
    """PyPH Interface for basic Grasshopper (and Rhino) dependencies that can be
        used by other classes which accept this Interface object.

    Arguments:
    ----------
        * _ghdoc: (ghdoc)
        * _ghenv: (ghenv)
        * _sc: (scriptcontext)
        * _rh: (Rhino)
        * _rs (rhinoscriptsyntax)
        * _ghc (ghpythonlib.components)
        * _gh (Grasshopper)
    """

    def __init__(self, _ghdoc, _ghenv, _sc, _rh, _rs, _ghc, _gh):
        self.ghdoc = _ghdoc
        self.ghenv = _ghenv
        self.scriptcontext = _sc
        self.Rhino = _rh
        self.rhinoscriptsyntax = _rs
        self.ghpythonlib_components = _ghc
        self.Grasshopper = _gh

    def gh_compo_find_input_index_by_name(self, _input_name):
        # type: (str) -> int
        """
        Compares an input name against the list of GH_Component Inputs. Returns the
        index of any match or None if not found

        Arguments:
        ----------
            * _input_name (str): The name to search for

        Returns:
        --------
            * (int): The index of the matching item
        """

        for i, each in enumerate(list(self.ghenv.Component.Params.Input)):
            names = [str(each.Name).upper(), str(each.NickName).upper()]
            if _input_name.upper() in names:
                return i

        raise Exception(
            'Error: The input node "{}" cannot be found?'.format(_input_name))

    def gh_compo_get_input_for_node_number(self, _node_number):
        # type: (int) -> GH_Structure[IGH_Goo]
        """Returns the 'VolatileData' for a GH-Component's Input Param.

        Arguments:
        ----------
            * _node_number (int): The number of the GH-Component Input Node to read.

        Returns:
        --------
            * (GH_Structure[IGH_Goo]): The 'VolatileData' of the GH-Component Input Node.
        """
        return self.ghenv.Component.Params.Input[_node_number].VolatileData

    def gh_compo_get_input_guids(self, _input_index_number, _branch_num=0):
        # type: (int, int) -> List[System.Guid]
        """
        Returns a list of all the GUIDs of the objects being passed to the
        component's specified input node.

        Arguments:
        ----------
            * _input_index_number (int): The index number of the input node to
                look at.

        Returns:
        --------
            * list[System.Guid]: The GUIDs of the objects being input into the specified
                component input node.
        """

        guids = []
        try:
            for _ in self.ghenv.Component.Params.Input[_input_index_number].VolatileData[_branch_num]:
                try:
                    guids.append(_.ReferenceID)
                except AttributeError:
                    # If input doesn't have a ReferenceID, its probably a Panel text or number input
                    guids.append(None)
        except ValueError:
            nm = self.ghenv.Component.Params.Input[_input_index_number].NickName
            print('No input values found for "{}".'.format(nm))

        return guids

    @contextmanager
    def context_rh_doc(self):
        """
        Context Manager used to switch Grasshopper's scriptcontext.doc
        to Rhino.RhinoDoc.ActiveDoc temporarily. This is needed when trying
        to access information such as UserText for Rhino objects

        Use:
        ----
        >>> with context_rh_doc():\n
        >>>    run_some_command( gh_component_input )
        """

        try:
            self.scriptcontext.doc = self.Rhino.RhinoDoc.ActiveDoc
            yield
        except Exception as e:
            self.scriptcontext.doc = self.ghdoc
            print("Exception:", e.message)
            raise Exception
        finally:
            self.scriptcontext.doc = self.ghdoc

    def get_rh_obj_UserText_dict(self, _rh_obj_guids):
        # type: (System.guid) -> List[Dict]
        """
        Get any Rhino-side UserText attribute data for the Object/Elements.
        Note: this only works in Rhino v6.0+ I believe...

        Arguments:
        ----------
            _rh_obj_guids (list[Rhino Guid]): The Rhino Guid(s) of the Object/Elements.

        Returns:
        --------
            output_list (list[dict]): A list of dictionaries, each with all the data found
                in the Rhino object's UserText library.
        """

        def is_grasshopper_geometry(_guid):
            """If its GH generated geom, will have this GUID always"""
            return str(_guid) == "00000000-0000-0000-0000-000000000000"

        if not _rh_obj_guids:
            return []
        if not isinstance(_rh_obj_guids, list):
            _rh_obj_guids = [_rh_obj_guids]

        output_list = []
        with self.context_rh_doc():
            for guid in _rh_obj_guids:
                if not guid or is_grasshopper_geometry(guid):
                    output_list.append({"Object Name": None})
                else:
                    # -- Go get the data from Rhino
                    rh_obj = self.Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid)
                    object_rh_UserText_dict = {
                        k: self.rhinoscriptsyntax.GetUserText(rh_obj, k)
                        for k in self.rhinoscriptsyntax.GetUserText(rh_obj)
                    }

                    # -- Fix the name
                    object_name = self.rhinoscriptsyntax.ObjectName(guid)
                    object_rh_UserText_dict["Object Name"] = object_name

                    output_list.append(object_rh_UserText_dict)

        return output_list

    def convert_to_LBT_geom(self, _inputs):
        # type: (List[Any]) -> List[List]
        """Converts a list of RH- or GH-Geometry into a list of LBT-Geometry. If
            input is a string, boolean or number, will just return that without converting.

            Note: The return is a list of lists since the lbt converter might return
            triangulated faces in some cases.

        Arguments:
        ----------
            * _inputs (list[Any]): The Rhino items / objects to try and convert

        Returns:
        --------
            * list[list]: The input (RH/GH) geometry, converted to LBT-Geometry
        """

        if not isinstance(_inputs, list):
            _inputs = [_inputs]
        lbt_geometry = []
        for i, _ in enumerate(_inputs):
            if isinstance(_, list):
                for __ in _:
                    result = self.convert_to_LBT_geom(__)
                    lbt_geometry.append(result)
            elif isinstance(_, (str, int, float)):
                try:
                    lbt_geometry.append(float(str(_)))
                except ValueError:
                    lbt_geometry.append(str(_))
            elif isinstance(_, bool):
                lbt_geometry.append(_)
            elif isinstance(_, self.Rhino.Geometry.Brep):
                lbt_geometry.append(to_face3d(_))
            elif isinstance(_, self.Rhino.Geometry.PolylineCurve):
                lbt_geometry.append(to_polyline3d(_))
            elif isinstance(_, self.Rhino.Geometry.LineCurve):
                lbt_geometry.append(to_linesegment3d(_))
            elif isinstance(_, self.Rhino.Geometry.Line):
                lbt_geometry.append(to_linesegment3d(self.Rhino.Geometry.LineCurve(_)))
            elif isinstance(_, self.Rhino.Geometry.Mesh):
                lbt_geometry.append(to_mesh3d(_))
            elif isinstance(_, self.Rhino.Geometry.Point3d):
                lbt_geometry.append(to_point3d(_))
            else:
                raise LBTGeometryConversionError(_)

        return lbt_geometry

    def convert_to_rhino_geom(self, _inputs):
        # type: (List) -> List
        """Converts a list of LBT-Geometry into RH-Geometry.

        Arguments:
        ----------
            * _inputs (list): The LBT Geometry items / objects to try and convert

        Returns:
        --------
            * list: The input LBT geometry, converted to Rhino-Geometry
        """

        if not isinstance(_inputs, list):
            _inputs = [_inputs]

        rh_geom = []
        for _ in _inputs:
            if isinstance(_, list):
                for __ in _:
                    result = self.convert_to_rhino_geom(__)
                    rh_geom.append(result)
            elif isinstance(_, honeybee.face.Face):
                rh_geom.append(from_face3d(_.geometry))
            elif isinstance(_, honeybee.face.Face3D):
                rh_geom.append(from_face3d(_))
            else:
                raise Exception(
                    'Input Error: Cannot convert "{}" to Rhino Geometry.'.format(type(_)))

        return rh_geom

    def inset_LBT_face(self, _lbt_face, _inset_distance):
        # type: (honeybee.face.Face, float) -> List
        """Converts an LBT face to Rhino Geom and performs an 'inset' operation on it. Returns the newly inset Face3D

        Arguments:
        ----------
            * _lbt_face (honeybee.face.Face): The LBT Face to inset
            * _inset_distance (float): The distance to inset the surface

        Returns:
        --------
            * (honeybee.face.Face): A new LBT Face, inset by the specified amount
        """

        rh_floor_surface = self.convert_to_rhino_geom(_lbt_face)

        if _inset_distance < 0.001:
            return rh_floor_surface

        # -----------------------------------------------------------------------
        srfcPerim = self.ghpythonlib_components.JoinCurves(
            self.ghpythonlib_components.BrepEdges(rh_floor_surface)[0], preserve=False
        )

        # Get the inset Curve
        # -----------------------------------------------------------------------
        srfcCentroid = self.Rhino.Geometry.AreaMassProperties.Compute(
            rh_floor_surface).Centroid
        plane = self.ghpythonlib_components.XYPlane(srfcCentroid)
        plane = self.ghpythonlib_components.IsPlanar(rh_floor_surface, True).plane
        srfcPerim_Inset_Pos = self.ghpythonlib_components.OffsetCurve(
            srfcPerim, _inset_distance, plane, 1)
        srfcPerim_Inset_Neg = self.ghpythonlib_components.OffsetCurve(
            srfcPerim, _inset_distance * -1, plane, 1)

        # Choose the right Offset Curve. The one with the smaller area
        # Check IsPlanar first to avoid self.grasshopper_components.BoundarySurfaces error
        # -----------------------------------------------------------------------
        if srfcPerim_Inset_Pos.IsPlanar:
            srfcInset_Pos = self.ghpythonlib_components.BoundarySurfaces(
                srfcPerim_Inset_Pos)
        else:
            srfcInset_Pos = self.ghpythonlib_components.BoundarySurfaces(
                srfcPerim)  # Use the normal perim

        if srfcPerim_Inset_Neg.IsPlanar():
            srfcInset_Neg = self.ghpythonlib_components.BoundarySurfaces(
                srfcPerim_Inset_Neg)
        else:
            srfcInset_Neg = self.ghpythonlib_components.BoundarySurfaces(
                srfcPerim)  # Use the normal perim

        # -----------------------------------------------------------------------
        area_Pos = self.ghpythonlib_components.Area(srfcInset_Pos).area
        area_neg = self.ghpythonlib_components.Area(srfcInset_Neg).area

        if area_Pos < area_neg:
            return self.convert_to_LBT_geom(srfcInset_Pos)
        else:
            return self.convert_to_LBT_geom(srfcInset_Neg)

    def merge_Face3D(self, _face3Ds):
        # type: (honeybee.face.Face3D) -> List[ List[honeybee.face.Face3D] ]
        """Combine a set of Face3D surfaces together into 'merged' Face3Ds

        This *should* work on surfaces that are touching, AND ones that overlap. Using
        GH MergeFaces() only works on 'touching' surfaces, but not overlapping ones.
        Using 'RegionUnion' should work on both touching and overlapping surfaces.

        Arguments:
        ----------
            * _face3Ds (list[honeybee.face.Face3D]): The Face3Ds to try and merge

        Returns:
        --------
            * (list[list[honeybee.face.Face3D]]): The merged Face3Ds
        """

        # -- Pull out the Perimeter curves from each Face3D
        perims = []
        for face3D in _face3Ds:
            rh_brep = self.convert_to_rhino_geom(face3D)
            faces, edges, vertices = self.ghpythonlib_components.DeconstructBrep(rh_brep)
            perims.append(self.ghpythonlib_components.JoinCurves(edges, True))

        joined_curves = self.ghpythonlib_components.RegionUnion(perims)

        if not isinstance(joined_curves, list):
            joined_curves = [joined_curves]

        # -- Intersect and Merge the Perimeter Curves back together, make new Face3Ds
        new_LBT_face3ds = []
        for crv in joined_curves:
            merged_breps = self.Rhino.Geometry.Brep.CreatePlanarBreps(crv, 0.01)

            for new_brep in merged_breps:
                new_LBT_Face = self.convert_to_LBT_geom(new_brep)
                new_LBT_face3ds.extend(new_LBT_Face)

        return new_LBT_face3ds

    def extrude_Face3D_WorldZ(self, _face3D, _dist=2.5):
        # type: (List[Face3D], float) -> List[Face3D]
        """Returns a list of Face3D surfaces representing a closed brep extrusion of the base Face3D"""
        extrusion_vector = self.ghpythonlib_components.UnitZ(_dist)
        rh_brep = from_face3d(_face3D)
        volume_geom = self.ghpythonlib_components.Extrude(rh_brep, extrusion_vector)

        return self.convert_to_LBT_geom(volume_geom)[0]

    def error(self, _in):
        """Raise a runtime Error message on the GH Component"""
        if not _in:
            return None
        else:
            level = self.Grasshopper.Kernel.GH_RuntimeMessageLevel.Error
            self.ghenv.Component.AddRuntimeMessage(level, _in)

    def warning(self, _in):
        """Raise a runtime Warning message on the GH Component"""
        if not _in:
            return None
        else:
            level = self.Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning
            self.ghenv.Component.AddRuntimeMessage(level, _in)


class ComponentInput:
    """GH-Component Input Node data class."""

    def __init__(self, _name='-', _description='', _access=0, _type_hint=Component.NoChangeHint()):
        # type: (str, str, int, Component.NoChangeHint) -> None
        self.name = _name
        self.description = _description
        self.access = _access  # 0='item, 1='list', 2='tree'
        self.type_hint = _type_hint

    def __str__(self):
        return '{}(name={})'.format(self.__class__.__name__, self.name, self.access, self.type_hint)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


def handle_inputs(IGH, _input_objects, _input_name, _branch_num=0):
    # type: (IGH, list, str, int) -> List[dict]
    """
    Generic Rhino / GH Geometry input handler

    Arguments:
    ----------
        * IGH (PyPH_Rhino.gh_io.IGH)
        * _input_objects (Any):
        * _input_name (str):

    Returns:
    --------
        (list[dict]): A list of the object dictionaries with all the information found.
    """

    if not isinstance(_input_objects, list):
        _input_objects = list(_input_objects)

    # -- Get the Input Object Attribute UserText values (if any)
    input_index_number = IGH.gh_compo_find_input_index_by_name(_input_name)
    input_guids = IGH.gh_compo_get_input_guids(input_index_number, _branch_num)
    inputs = IGH.get_rh_obj_UserText_dict(input_guids)

    # -- Add the Input Geometry to the output dictionary
    input_geometry_lists = IGH.convert_to_LBT_geom(_input_objects)

    output_list = []
    for input_dict, geometry_list in zip(inputs, input_geometry_lists):
        if not isinstance(geometry_list, list):
            geometry_list = [geometry_list]

        for geometry in geometry_list:
            item = deepcopy(input_dict)
            item.update({"Geometry": [geometry]})
            output_list.append(item)

    return output_list


def setup_component_inputs(IGH, _input_dict, _start_i=1, _end_i=20):
    # type: (IGH, Dict[int, ComponentInput], int, int) -> None
    """Dynamic GH component input node configuration.

    Arguments:
    ----------
        * IGH (): The Grasshopper Interface object.
        * _input_dict (dict[int, ComponentInput]): The input dict with the field names
            and descriptions to use for the component input nodes.
        * _start_i (int): Optional starting node number. Default=1
        * _end_i (int): Optional ending node number. Default=20

    Returns:
    --------
        * None
    """
    for input_num in range(_start_i, _end_i):
        input_item = _input_dict.get(input_num, ComponentInput('-', '-'))

        try:
            input_node = IGH.ghenv.Component.Params.Input[input_num]
            input_node.NickName = input_item.name
            input_node.Name = input_item.name
            input_node.Description = input_item.description
            input_node.Access = IGH.Grasshopper.Kernel.GH_ParamAccess(input_item.access)
            input_node.TypeHint = input_item.type_hint
        except ValueError:
            # -- past end of component inputs
            pass

    return None


def _get_component_input_value(_input):
    # type: (Sequence[Any]) -> Union[float, str]
    """Try and cast the input value to the appropriate type."""

    try:
        input_value = _input[0].Value

        if isinstance(input_value, str):
            # For some reason, floats come as Str?....
            try:
                return float(input_value)
            except:
                return input_value
        else:
            return input_value
    except:
        return str(_input[0])


def get_component_input_values(ghenv):
    # type: (Any) -> Dict[str, Any]
    """ Dynamic Component Input 'get' - pulls all the component input names/values into a dictionary.

    Arguments:
    ----------
        * ghenv (): The Grasshopper ghenv variable.

    Returns:
    --------
        * dict[str, Any]: A dictionary of the component input node's user input values.

    """
    inputs = {}
    for input in ghenv.Component.Params.Input:
        try:
            # Cast from GH_Goo to a normal PH-List
            try:
                input_list = list(input.VolatileData[0])
            except:
                input_list = []

            if str(input.Access) == 'list':
                val = []
                for v in input_list:
                    val.append(_get_component_input_value([v]))
            elif str(input.Access) == 'tree':
                raise NotImplementedError("Tree input not allowed yet....")
            else:
                val = _get_component_input_value(input_list)

            inputs[input.Name] = val
        except:
            inputs[input.Name] = None

    return inputs
