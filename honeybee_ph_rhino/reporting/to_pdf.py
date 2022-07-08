# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for exporting a PDF report page."""

import os
from xml.etree.ElementTree import tostring
try:
    from itertools import izip_longest
except:
    from itertools import zip_longest as izip_longest

try:
    from typing import List, Tuple, Any, Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from System.Drawing import Color, Size
    from System import Guid
except ImportError:
    pass  # Outside .NET

try:
    from Rhino.Geometry import Mesh, Hatch, TextJustification, Point3d
    from Rhino.DocObjects import ObjectAttributes
except ImportError:
    pass  # Outside Rhino

try:
    from Grasshopper import DataTree
except ImportError:
    pass  # Outside Grasshopper

from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.gh_compo_io import ghio_validators


class RHTextJustify(ghio_validators.Validated):
    """Validator for Integer user-input conversion into Rhino.Geometry.TextJustification Enum."""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        mapping = {
            0: TextJustification.BottomLeft, 1: TextJustification.BottomCenter,
            2: TextJustification.BottomRight, 3: TextJustification.MiddleLeft,
            4: TextJustification.MiddleCenter, 5: TextJustification.MiddleRight,
            6: TextJustification.TopLeft, 7: TextJustification.TopCenter,
            8: TextJustification.TopRight
        }
        return mapping[int(new_value)]


class LayoutPageLabel(object):
    """Dataclass for Layout-Page Labels."""
    justification = RHTextJustify('justification')

    def __init__(self, _text, _size, _location, _format, _justification):
        # type: (str, float, Point3d, str, int) -> None
        self._text = _text
        self.text_size = _size
        self.location = _location
        self.format = _format
        self.justification = _justification

    @property
    def text(self):
        fmt = "{}".format(self.format)
        try:
            return fmt.format(self._text)
        except ValueError:
            try:
                return fmt.format(float(self._text))
            except Exception:
                return self._text

    def __str__(self):
        return '{}(text={}, text_size={}, location={}, format={}, justification={})'.format(
            self.__class__.__name__, self.text, self.text_size, self.location, self.format, self.justification)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


def _clean_filename(_input_str):
    # type: (str) -> str
    """Return a cleaned and validated filename string."""
    valid_filename = os.path.splitext(_input_str)[0]  # remove any extension
    valid_filename = valid_filename.replace(" ", "_").strip()
    valid_filename = "".join(_ if _.isalnum() else "_" for _ in valid_filename)
    return valid_filename


def gen_file_paths(_save_folder, _file_names, _target_length):
    # type: (str, DataTree, int) -> List[str]
    """Return a list of full paths for each PDF file to export. Will create save folder if needed.

    Arguments:
    ----------
        * _save_folder (str):
        * _file_names (DataTree):
        * _target_length (int):

    Returns:
    --------
        * List[str]
    """
    file_paths = []

    if not _save_folder:
        return file_paths

    if _file_names.BranchCount == 0:
        return file_paths

    if _target_length == 0:
        # save-file list len should match the target (geometry) len.
        return file_paths

    if _file_names.BranchCount != _target_length:
        raise Exception("Error: The number of geometry branches ({}) does not"
                        " match the number of file-names ({})?".format(
                            _target_length, _file_names.BranchCount)
                        )

    # --- Save folder
    if not os.path.exists(_save_folder):
        try:
            os.makedirs(_save_folder)
        except Exception as e:
            raise Exception("{}\nError creating save folder: {}".format(e, _save_folder))

    # -- Save filenames
    for branch in _file_names.Branches:
        file_name = _clean_filename(str(branch[0]))
        file_path = os.path.join(_save_folder, file_name + os.extsep + "pdf")
        file_paths.append(file_path)

    return file_paths


def get_active_view_name(_IGH):
    return _IGH.scriptcontext.doc.Views.ActiveView.ActiveViewport.Name


def set_active_view_by_name(_IGH, _view_name):
    # type: (gh_io.IGH, str) -> None
    """Changes the Active View to the specified layout/view by name. Raises an error if the target view name does not exist.

    Arguments:
    ----------
        * _IGH (gh_io.IGH):
        * _view_name (str):

    Returns:
    --------
        * (None)
    """
    # https://developer.rhino3d.com/samples/rhinocommon/get-and-set-the-active-view/

    # active view and non-active view names
    active_view_name = get_active_view_name(_IGH)
    non_active_views = [(view.ActiveViewport.Name, view)
                        for view in _IGH.scriptcontext.doc.Views if view.ActiveViewport.Name != active_view_name]

    if _view_name != active_view_name:
        if _view_name in [seq[0] for seq in non_active_views]:
            _IGH.scriptcontext.doc.Views.ActiveView = [seq[1]
                                                       for seq in non_active_views if seq[0] == _view_name][0]
            # print("Setting Active View to: '{}'".format(_view_name))
        else:
            msg = "\"{0}\" is not a valid view name?".format(_view_name)
            _IGH.error(msg)


def set_active_layer_by_name(_IGH, _layer_name):
    # type: (gh_io.IGH, str) -> None
    """Change the active layer by name"""
    with _IGH.context_rh_doc():
        if _layer_name not in _IGH.rhinoscriptsyntax.LayerNames():
            raise Exception(
                "Error: Cannot find the Layer with name: '{}'?".format(_layer_name))
        _IGH.rhinoscriptsyntax.CurrentLayer(_layer_name)


def find_layers_with_detail_views(_IGH):
    # type: (gh_io.IGH) -> List[str]
    """Goes to the Active View and looks to see if there are any 'DetailViews' present,
    If so, find the Layer the DetailViews are on and add the layerIndex to the list.
    This is used to ensure that the DetailViews will remain 'on' when exporting the PDF.

    Arguments:
    ----------
        * (gh_io.IGH):

    Returns:
    --------
        * (List[str]):
    """

    layer_names_ = []  # type: List[str]
    layer_IDs_ = []  # type: List[int]

    with _IGH.context_rh_doc():
        active_view = _IGH.scriptcontext.doc.Views.ActiveView
        detail_views = active_view.GetDetailViews()
        for detail_view in detail_views:
            layer_IDs_.append(detail_view.Attributes.LayerIndex)

        # Find the right Layer Names from the Index vals
        layer_IDs_ = list(set(layer_IDs_))  # Keep only one of each unique index val

        for i in range(len(layer_IDs_)):
            # Get the Layer and any parents
            layer_path = _IGH.scriptcontext.doc.Layers[layer_IDs_[i]].FullPath
            layer_names = list(layer_path.Split(':'))  # type: List[str]

            for layerName in layer_names:
                layer_names_.append(layer_path)
                layer_names_.append(layerName)

    return list(set(layer_names_))


def turn_off_all_layers(_IGH, _except_layers):
    # type: (gh_io.IGH, List[str]) -> List[bool]
    """Turn all Layer Visibilities 'Off' except for the specified layers. Returns a list
        of the starting layer states before changing as a bool (True=On, False=Off).

    Arguments:
    ----------
        * _IGH (gh_io.IGH):
        * _except_layers (List[str]): A list of the Layers to leave 'on'

    Returns:
    --------
        * (List[bool]): List of the starting layer states before changing (True=On, False=Off)
    """

    with _IGH.context_rh_doc():

        # Record the starting layer visibility state for resetting when done
        layer_visibilities = [_IGH.rhinoscriptsyntax.LayerVisible(layer)
                              for layer
                              in _IGH.rhinoscriptsyntax.LayerNames()]

        # Set layers 'off' if they aren't on the list to stay on
        for layer_name in _IGH.rhinoscriptsyntax.LayerNames():
            # if list(layer.Split(":"))[-1] not in allLayersOn:
            if layer_name in _except_layers:
                _IGH.rhinoscriptsyntax.LayerVisible(layer_name, True)
            else:
                _IGH.rhinoscriptsyntax.LayerVisible(layer_name, False)

        _IGH.Rhino.RhinoDoc.ActiveDoc.Views.RedrawEnabled = True
        _IGH.Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    return layer_visibilities


def reset_all_layer_visibility(_IGH, _layer_vis_settings):
    # type: (gh_io.IGH, List[bool]) -> None
    """Reset all the Layer Vis settings to the original State

    Arguments:
    ----------
        *
        *

    Returns:
    --------
        * (None)
    """

    with _IGH.context_rh_doc():
        layers = _IGH.rhinoscriptsyntax.LayerNames()

        for layer, vis_setting, in izip_longest(layers, _layer_vis_settings):
            _IGH.rhinoscriptsyntax.LayerVisible(layer, vis_setting)

        _IGH.Rhino.RhinoDoc.ActiveDoc.Views.RedrawEnabled = True
        _IGH.Rhino.RhinoDoc.ActiveDoc.Views.Redraw()


def create_bake_layer(_IGH):
    # type: (gh_io.IGH) -> str
    """Creates a new layer which is used for bake objects. Returns the name of the new layer.

    Arguments:
    ----------
        *

    Returns:
    --------
        *
    """

    with _IGH.context_rh_doc():
        # Create an Unused Layer Name
        new_layer_name = _IGH.scriptcontext.doc.Layers.GetUnusedLayerName(False)

        # Add a new Layer to the Document
        _IGH.scriptcontext.doc.Layers.Add(new_layer_name, Color.Black)

    return new_layer_name


def remove_bake_layer(_IGH, _layer_name):
    # type: (gh_io.IGH, str) -> None
    """Remove a layer with the specified name. Will also delete all objects on the layer.

    Arguments:
    ----------
        *

    Returns:
    --------
        *
    """

    with _IGH.context_rh_doc():
        # Be sure the temp layer exists
        if _layer_name not in _IGH.rhinoscriptsyntax.LayerNames():
            return

        # Remove all the objects on the specified layer
        _IGH.rhinoscriptsyntax.DeleteObjects(
            _IGH.rhinoscriptsyntax.ObjectsByLayer(_layer_name)
        )

        # Remove the layer
        _IGH.scriptcontext.doc.Layers.Delete(
            _IGH.scriptcontext.doc.Layers.FindName(_layer_name)
        )


def mesh2Hatch(_IGH, mesh):
    # type: (gh_io.IGH, Mesh) -> Tuple[List[Hatch], List[Color]]
    """Copied / Adapted from Ladybug Definition

    Arguments:
    ----------
        *

    Returns:
    --------
        *
    """

    # Make some lists to hold key parameters
    hatches = []  # type: List[Hatch]
    colors = []  # type: List[Color]
    guids = []
    runningVertexCount = 0
    meshColors = mesh.VertexColors

    for faceCount, face in enumerate(mesh.Faces):
        faceColorList = []
        facePointList = []

        # Extract the points and colors.
        if face.IsQuad:
            faceColorList.append(meshColors[face.A])
            faceColorList.append(meshColors[face.B])
            faceColorList.append(meshColors[face.C])
            faceColorList.append(meshColors[face.D])

            facePointList.append(mesh.PointAt(faceCount, 1, 0, 0, 0))
            facePointList.append(mesh.PointAt(faceCount, 0, 1, 0, 0))
            facePointList.append(mesh.PointAt(faceCount, 0, 0, 1, 0))
            facePointList.append(mesh.PointAt(faceCount, 0, 0, 0, 1))
        else:
            faceColorList.append(meshColors[face.A])
            faceColorList.append(meshColors[face.B])
            faceColorList.append(meshColors[face.C])

            facePointList.append(mesh.PointAt(faceCount, 1, 0, 0, 0))
            facePointList.append(mesh.PointAt(faceCount, 0, 1, 0, 0))
            facePointList.append(mesh.PointAt(faceCount, 0, 0, 1, 0))

        # Calculate the average color of the face.
        if face.IsQuad:
            hatchColorR = (faceColorList[0].R + faceColorList[1].R +
                           faceColorList[2].R + faceColorList[3].R) / 4
            hatchColorG = (faceColorList[0].G + faceColorList[1].G +
                           faceColorList[2].G + faceColorList[3].G) / 4
            hatchColorB = (faceColorList[0].B + faceColorList[1].B +
                           faceColorList[2].B + faceColorList[3].B) / 4
        else:
            hatchColorR = (faceColorList[0].R +
                           faceColorList[1].R + faceColorList[2].R) / 3
            hatchColorG = (faceColorList[0].G +
                           faceColorList[1].G + faceColorList[2].G) / 3
            hatchColorB = (faceColorList[0].B +
                           faceColorList[1].B + faceColorList[2].B) / 3
        hatchColor = Color.FromArgb(
            255, hatchColorR, hatchColorG, hatchColorB)

        # Create the outline of a new hatch.
        hatchCurveInit = _IGH.Rhino.Geometry.PolylineCurve(facePointList)
        if face.IsQuad:
            hatchExtra = _IGH.Rhino.Geometry.LineCurve(
                facePointList[0], facePointList[3])
        else:
            hatchExtra = _IGH.Rhino.Geometry.LineCurve(
                facePointList[0], facePointList[2])
        hatchCurve = _IGH.Rhino.Geometry.Curve.JoinCurves(
            [hatchCurveInit, hatchExtra], _IGH.scriptcontext.doc.ModelAbsoluteTolerance)[0]

        # Create the hatch.
        try:
            if hatchCurve.IsPlanar():
                meshFaceHatch = _IGH.Rhino.Geometry.Hatch.Create(hatchCurve, 0, 0, 0)[0]
                hatches.append(meshFaceHatch)
                colors.append(hatchColor)
            else:
                # We have to split the quad face into two triangles.
                hatchCurveInit1 = _IGH.Rhino.Geometry.PolylineCurve(
                    [facePointList[0], facePointList[1], facePointList[2]])
                hatchExtra1 = _IGH.Rhino.Geometry.LineCurve(
                    facePointList[0], facePointList[2])
                hatchCurve1 = _IGH.Rhino.Geometry.Curve.JoinCurves(
                    [hatchCurveInit1, hatchExtra1], _IGH.scriptcontext.doc.ModelAbsoluteTolerance)[0]
                meshFaceHatch1 = _IGH.Rhino.Geometry.Hatch.Create(hatchCurve1, 0, 0, 0)[
                    0]
                hatchCurveInit2 = _IGH.Rhino.Geometry.PolylineCurve(
                    [facePointList[2], facePointList[3], facePointList[0]])
                hatchExtra2 = _IGH.Rhino.Geometry.LineCurve(
                    facePointList[2], facePointList[0])
                hatchCurve2 = _IGH.Rhino.Geometry.Curve.JoinCurves(
                    [hatchCurveInit2, hatchExtra2], _IGH.scriptcontext.doc.ModelAbsoluteTolerance)[0]
                meshFaceHatch2 = _IGH.Rhino.Geometry.Hatch.Create(hatchCurve2, 0, 0, 0)[
                    0]

                hatches.extend([meshFaceHatch1, meshFaceHatch2])
                colors.extend([hatchColor, hatchColor])
        except:
            pass

    return hatches, colors


def bake_geometry_object(_IGH, _geom_obj, _attr_obj, _layer_name):
    # type: (gh_io.IGH, Guid, Optional[ObjectAttributes], str) -> None
    """ Takes in a geom obj Guid and attributes, then bakes to a Layer

    If the Object is a Mesh, will bake that using the Mesh's Vertex Colors. To
    set these, use the Grasshopper MeshColor component (ghc.MeshColours() ) before
    inputting here.

    If its a Curve input, will try and look for Attribute information in the
    _geomAttributes input.

    If its some other type of geometry, will just use a default attribute for printing.

    Arguments:
    ----------
        * _IGH (gh_io.IGH):
        * _geom_obj (Guid):
        * _attr_obj (ObjectAttributes):
        * _layer_name (str):

    Returns:
    --------
        * (None)
    """

    doc_object = _IGH.rhinoscriptsyntax.coercerhinoobject(_geom_obj, True, True)
    geometry = doc_object.Geometry

    with _IGH.context_rh_doc():
        layerT = _IGH.Rhino.RhinoDoc.ActiveDoc.Layers  # layer table

        if _IGH.rhinoscriptsyntax.IsMesh(geometry):
            # Find the target layer index
            parentLayerIndex = _IGH.Rhino.DocObjects.Tables.LayerTable.FindByFullPath(
                layerT, _layer_name, True)

            # Create a hatch from the mesh
            guids = []
            hatches, colors = mesh2Hatch(_IGH, geometry)

            # Bake the Hatches into the Rhino Doc
            for count, hatch in enumerate(hatches):
                attr = _IGH.Rhino.DocObjects.ObjectAttributes()
                attr.LayerIndex = parentLayerIndex
                attr.ObjectColor = colors[count]
                attr.PlotColor = colors[count]
                attr.ColorSource = _IGH.Rhino.DocObjects.ObjectColorSource.ColorFromObject
                attr.PlotColorSource = _IGH.Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject
                # attr.DisplayOrder = 0  # 1 = Front, -1 = Back

                guids.append(_IGH.Rhino.RhinoDoc.ActiveDoc.Objects.AddHatch(hatch, attr))

            # Group the hatches so are manageable
            groupT = _IGH.Rhino.RhinoDoc.ActiveDoc.Groups
            _IGH.Rhino.DocObjects.Tables.GroupTable.Add(groupT, guids)
            _IGH.scriptcontext.doc.Views.Redraw()

        elif isinstance(geometry, _IGH.Rhino.Geometry.Curve):
            rhino_geom = _IGH.scriptcontext.doc.Objects.Add(
                geometry, _attr_obj or doc_object.Attributes)

            # Set the new Object's Layer
            if not _IGH.rhinoscriptsyntax.IsLayer(_layer_name):
                _IGH.rhinoscriptsyntax.AddLayer(_layer_name)
            _IGH.rhinoscriptsyntax.ObjectLayer(rhino_geom, _layer_name)

        else:
            # Just bake the regular Geometry with default attributes
            rhino_geom = _IGH.scriptcontext.doc.Objects.Add(
                geometry, doc_object.Attributes)

            # Set the new Object's Layer
            if not _IGH.rhinoscriptsyntax.IsLayer(_layer_name):
                _IGH.rhinoscriptsyntax.AddLayer(_layer_name)
            _IGH.rhinoscriptsyntax.ObjectLayer(rhino_geom, _layer_name)


def bake_label_object(_IGH, _label, _label_layer, _avoidCollisions=False):
    # type: (gh_io.IGH, LayoutPageLabel, str, bool) -> None
    """

    Arguments:
    ----------
        *

    Returns:
    --------
        *
    """

    # https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_TextEntity.htm
    with _IGH.context_rh_doc():

        # The base-plane for the Text
        origin = _label.location
        basePlane_origin = _IGH.Rhino.Geometry.Point3d(origin)
        basePlan_normal = _IGH.Rhino.Geometry.Vector3d(0, 0, 1)  # Assumes Top View
        basePlane = _IGH.Rhino.Geometry.Plane(
            origin=basePlane_origin, normal=basePlan_normal)

        # Create the txt object
        txt = _IGH.Rhino.Geometry.TextEntity()
        txt.Text = _label.text
        txt.Plane = basePlane
        txt.TextHeight = _label.text_size
        txt.Justification = _label.justification

        if _avoidCollisions:
            raise NotImplementedError('Not yet....')
            #  Test against the other text items on the sheet
            # First, find / create the bouding box rectangle of the text note
            this_bounding_box = txt.GetBoundingBox(txt.Plane)
            box_x_dim = abs(this_bounding_box.Min.X - this_bounding_box.Max.X)
            box_y_dim = abs(this_bounding_box.Min.Y - this_bounding_box.Max.Y)
            domain_x = _IGH.ghpythonlib_components.ConstructDomain(
                (box_x_dim/2)*-1,  box_x_dim/2)
            domain_y = _IGH.ghpythonlib_components.ConstructDomain(
                (box_y_dim/2)*-1,  box_y_dim/2)
            bounding_rect = _IGH.ghpythonlib_components.Rectangle(
                txt.Plane, domain_x, domain_y, 0).rectangle

            # Compare the current text note to the others already in the scene
            # Move the current tag if neccessary
            for eachNeighbor in _neighbors:
                intersection = _IGH.ghpythonlib_components.CurveXCurve(
                    eachNeighbor, bounding_rect)
                if intersection.points != None:
                    neighbor = _IGH.ghpythonlib_components.DeconstuctRectangle(
                        eachNeighbor)  # The overlapping textbox
                    neighborY = neighbor.Y  # Returns a domain
                    # neighborY = abs(neighborY[0] - neighborY[1]) # Total Y distance

                    neighborCP = neighbor.base_plane.Origin
                    thisCP = _IGH.ghpythonlib_components.DeconstuctRectangle(
                        bounding_rect).base_plane.Origin

                    if thisCP.Y > neighborCP.Y:
                        # Move the tag 'up'
                        neighborMaxY = neighborCP.Y + neighborY[1]
                        thisMinY = thisCP.Y - (box_y_dim/2)
                        moveVector = _IGH.Rhino.Geometry.Vector3d(
                            0, neighborMaxY-thisMinY, 0)
                        bounding_rect = _IGH.ghpythonlib_components.Move(
                            bounding_rect, moveVector).geometry
                    else:
                        # Move the tag 'down'
                        neighborMinY = neighborCP.Y - neighborY[1]
                        thisMaxY = thisCP.Y + (box_y_dim/2)
                        moveVector = _IGH.Rhino.Geometry.Vector3d(
                            0, neighborMinY-thisMaxY, 0)
                        bounding_rect = _IGH.ghpythonlib_components.Move(
                            bounding_rect, moveVector).geometry

                    # Re-Set the text tag's origin to the new location
                    txt.Plane = _IGH.ghpythonlib_components.DeconstuctRectangle(
                        bounding_rect).base_plane
        else:
            bounding_rect = None

        # Add the new text object to the Scene
        txtObj = _IGH.Rhino.RhinoDoc.ActiveDoc.Objects.AddText(txt)

        # Set the new Text's Layer
        if not _IGH.rhinoscriptsyntax.IsLayer(_label_layer):
            _IGH.rhinoscriptsyntax.AddLayer(_label_layer)
        _IGH.rhinoscriptsyntax.ObjectLayer(txtObj, _label_layer)

    return bounding_rect  # Return the text bounding box


def export_single_pdf(_IGH, _file_path):
    # type: (gh_io.IGH,  str) -> None
    """

    Arguments:
    ----------
        *

    Returns:
    --------
        *
    """
    # Layout Page Size in Layout's Units
    page_height = _IGH.scriptcontext.doc.Views.ActiveView.PageHeight
    page_width = _IGH.scriptcontext.doc.Views.ActiveView.PageWidth

    # Layout Page Size in Inches
    # Ref: https://developer.rhino3d.com/api/RhinoScriptSyntax/#document-UnitScale
    # Ref: https://developer.rhino3d.com/api/RhinoCommon/html/P_Rhino_RhinoDoc_PageUnitSystem.htm
    page_unit_system_number = _IGH.rhinoscriptsyntax.UnitSystem(in_model_units=False)

    page_height = page_height * \
        _IGH.rhinoscriptsyntax.UnitScale(8, page_unit_system_number)  # Type 8 = Inches
    page_width = page_width * \
        _IGH.rhinoscriptsyntax.UnitScale(8, page_unit_system_number)
    page_height = round(page_height, 2)
    page_width = round(page_width, 2)

    pdf = _IGH.Rhino.FileIO.FilePdf.Create()
    dpi = 300
    # Should get this from the view?
    size = Size(page_width*dpi, page_height*dpi)
    settings = _IGH.Rhino.Display.ViewCaptureSettings(
        _IGH.scriptcontext.doc.Views.ActiveView, size, dpi)
    settings.RasterMode = True
    settings.OutputColor = _IGH.Rhino.Display.ViewCaptureSettings.ColorMode.DisplayColor
    pdf.AddPage(settings)

    try:
        os.remove(_file_path)
        # print("Removed file: {}".format(_file_path))
    except OSError as e:
        if not os.path.exists(_file_path):
            pass
        else:
            raise OSError("{}/nFile {} can not be removed".format(e, _file_path))

    # print('Writing file: {}'.format(_file_path))
    pdf.Write(_file_path)


def export_pdfs(_IGH, _file_paths, _layout_name, _layers_on, _geom, _geom_attrs, _labels):
    # type: (gh_io.IGH, List[str], str, List[str], DataTree[Guid], DataTree[ObjectAttributes], DataTree[LayoutPageLabel]) -> None
    """

    Arguments:
    ----------
        * _IGH (gh_io.IGH): Grasshopper Interface.
        * _file_paths (List[str]): A list of the full file-paths to save out to.
        * _layout_name (str): The name of the Layout (View) to export as PDF
        * _layers_on (List[str]): A list of the layer-names to leave 'on' during export.
        * _geom (DataTree[Guid]):
        * _geom_attrs (DataTree[ObjectAttributes]):
        * _labels (DataTree[LayoutPageLabel]):

    Returns:
    --------
        * None
    """

    # print('writing PDF files....')

    # -- Setup the layers and views
    starting_active_view_name = get_active_view_name(_IGH)
    set_active_view_by_name(_IGH, _layout_name)
    detail_view_layers = find_layers_with_detail_views(_IGH)
    set_active_layer_by_name(_IGH, detail_view_layers[0])

    # add all layers with a detail views to the 'on' list
    _layers_on.extend(detail_view_layers)
    starting_layer_visibilities = turn_off_all_layers(_IGH, _except_layers=_layers_on)

    # -- Bake objects
    for branch_num, geom_list in enumerate(_geom.Branches):
        geom_bake_layer = create_bake_layer(_IGH)  # Make temp layer
        label_bake_layer = create_bake_layer(_IGH)  # Make temp layer
        set_active_view_by_name(_IGH, 'Top')  # Change to 'Top' View for Baking

        for i, geom_obj in enumerate(geom_list):
            # -- Object Attribute
            attr_obj = _geom_attrs.Branch(branch_num)[i]

            # -- Bake Geometry to the specified layer
            bake_geometry_object(_IGH, geom_obj, attr_obj, geom_bake_layer)

        # -- Bake Labels to the specified layer
        set_active_view_by_name(_IGH, _layout_name)
        try:
            for label in _labels.Branch(branch_num):
                bake_label_object(_IGH, label, label_bake_layer)
        except ValueError:
            pass

        # # -- Export PDF file
        set_active_view_by_name(_IGH, _layout_name)
        export_single_pdf(_IGH, _file_paths[branch_num])

        # -- Cleanup baked items
        remove_bake_layer(_IGH, geom_bake_layer)
        remove_bake_layer(_IGH, label_bake_layer)

    # -- Cleanup layer vis and active view
    reset_all_layer_visibility(_IGH, starting_layer_visibilities)
    set_active_view_by_name(_IGH, starting_active_view_name)
