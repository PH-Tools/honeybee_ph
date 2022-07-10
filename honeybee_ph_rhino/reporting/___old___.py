#
# IDF2PHPP: A Plugin for exporting an EnergyPlus IDF file to the Passive House Planning Package (PHPP). Created by blgdtyp, llc
#
# This component is part of IDF2PHPP.
#
# Copyright (c) 2020, bldgtyp, llc <info@bldgtyp.com>
# IDF2PHPP is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License,
# or (at your option) any later version.
#
# IDF2PHPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License
# see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
#
"""
This will take in a Tree of GH objects, bake to the scene and Print to PDF, then remove the baked geom from the scene. Basically, its a GH PDF Printer. 
Each branch on the GH input tree will be output to a separate PDF, so organize inputs accordingly. Use a 'MeshColor' object on all surfaces before passing in to make them come out as solid fills in the PDF
NOTE: be sure to turn off all your GH Previews - otherwise they will print to the PDF as well.
-
EM Jun. 07, 2020
    Args:
        layersOn_: (Tree - strings) <Optional> A Tree of layers names to have 'On' during each export. If the tree length matches the '_geomToBake' the layer states will be modified for each output. Otherwise the first tree branch's values will be used for all. If none are passed, all Rhino Layers will be set to 'Off' for all the exports. Note: When passing in child/nested layers, use the Rhino convention <"Parent::Child"> - ie: "00_CAD::Floor_1" for a nested layer 'Floor_1' under '00_CAD'.
        _print: (Bool): Set to True to run. Use Boolean toggle not a button (for some reason?)
        _saveFolder: (string) File path where the outputs should be saved. Will create if it doesn't exist. ie: "C:\My_Project\Exports"
        fileName_:(List - string) <Optional> If a List of names are input, will use those for the exports. The length of the list should match the BranchCount of "_geomToBake". If a single name is input, will use that as the base name for the export files. If nothing is input, will use the name of the active Rhino File as the base.
        _viewName: (string) Input the name of the view you'd like to export. Will accept either a basic Rhino View or a Layout Page name
        _geomToBake: (Tree - meshes) The Grasshopper objects to be printed as a Tree. Each branch of the tree and all objects on that branch will be printed one at a time to separate PDF files. Before inputting surfaces, pass them through a 'MeshColor' component to assign colors correctly.
        _geomAttributes: (Tree - Rhino.DocObjects.ObjectAttributes) The Rhino Object Attributes (Color, Draworder, etc) to use for printing.
        _notesToBake: (Tree - strings) A Tree of any notes / text to be printed to the files
        _noteLocations: (Tree - Point3d) A Tree of center-point locations for the text note. Should match the _notesToBake in length and order
        noteTxtSize_: (Float) <Optional> A size (height) for the text. Note this refers to the 'Layout' units. File/Properties/Units/Layout.... For reference 7pt=2.5mm, 8pt=2.8mm, 9pt=3.4mm, 10pt=3.6mm, 12pt=4.2mm, 14pt=5mm
        _tablesToBake: (Tree - Table Object) <Optional>
        titleBlockTxtToBake_: (Tree) Each Branch should contain one or more text strings to write out to the Layout Page (Paperspace). Useful for Titleblock items.
        titleBlockTxtLocatons_: (List) Center Points for the Text items to be bakes to the Layout. List length should match the length of each of the Tree Branches in 'titleBlockTxtToBake_'
    Returns:
        
"""

import System.Drawing.Color
import System.Drawing
import System.Guid
import System
import os
import ghpythonlib.components as ghc
import Grasshopper.Kernel as ghK
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino
ghenv.Component.Name = "BT_2PDF_Print"
ghenv.Component.NickName = "2PDF | Print"
ghenv.Component.Message = 'JUN_07_2020'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "BT"
ghenv.Component.SubCategory = "03 | PDF"


def mesh2Hatch(mesh):
    # Copied / Adapted from Ladybug Definition

    # Make some lists to hold key parameters
    hatches = []
    colors = []
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
        hatchColor = System.Drawing.Color.FromArgb(
            255, hatchColorR, hatchColorG, hatchColorB)

        # Create the outline of a new hatch.
        hatchCurveInit = Rhino.Geometry.PolylineCurve(facePointList)
        if face.IsQuad:
            hatchExtra = Rhino.Geometry.LineCurve(facePointList[0], facePointList[3])
        else:
            hatchExtra = Rhino.Geometry.LineCurve(facePointList[0], facePointList[2])
        hatchCurve = Rhino.Geometry.Curve.JoinCurves(
            [hatchCurveInit, hatchExtra], sc.doc.ModelAbsoluteTolerance)[0]

        # Create the hatch.
        try:
            if hatchCurve.IsPlanar():
                meshFaceHatch = Rhino.Geometry.Hatch.Create(hatchCurve, 0, 0, 0)[0]
                hatches.append(meshFaceHatch)
                colors.append(hatchColor)
            else:
                # We have to split the quad face into two triangles.
                hatchCurveInit1 = Rhino.Geometry.PolylineCurve(
                    [facePointList[0], facePointList[1], facePointList[2]])
                hatchExtra1 = Rhino.Geometry.LineCurve(
                    facePointList[0], facePointList[2])
                hatchCurve1 = Rhino.Geometry.Curve.JoinCurves(
                    [hatchCurveInit1, hatchExtra1], sc.doc.ModelAbsoluteTolerance)[0]
                meshFaceHatch1 = Rhino.Geometry.Hatch.Create(hatchCurve1, 0, 0, 0)[0]
                hatchCurveInit2 = Rhino.Geometry.PolylineCurve(
                    [facePointList[2], facePointList[3], facePointList[0]])
                hatchExtra2 = Rhino.Geometry.LineCurve(
                    facePointList[2], facePointList[0])
                hatchCurve2 = Rhino.Geometry.Curve.JoinCurves(
                    [hatchCurveInit2, hatchExtra2], sc.doc.ModelAbsoluteTolerance)[0]
                meshFaceHatch2 = Rhino.Geometry.Hatch.Create(hatchCurve2, 0, 0, 0)[0]

                hatches.extend([meshFaceHatch1, meshFaceHatch2])
                colors.extend([hatchColor, hatchColor])
        except:
            pass

    return hatches, colors


def bakeText(_txt, _txtLocation, _layer, _txtSize=1, _neighbors=[], _avoidCollisions=False):
    """Bakes some Text to the Rhino scene

    _txt: <String> The actual text / note to bake
    _txtLocation: <Point3D> The reference point  / location for the object
    _layer: <String> The layer to bake the object to
    _txtSize: <Float> The size of the text (height). Refers to the Annotation scale of the Page being printed
    _neighbors: <List> The other text tags being printed
    """
    # https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_TextEntity.htm
    sc.doc = Rhino.RhinoDoc.ActiveDoc

    # The baseplane for the Text
    origin = _txtLocation
    basePlane_origin = Rhino.Geometry.Point3d(origin)
    basePlan_normal = Rhino.Geometry.Vector3d(0, 0, 1)  # Assumes Top View
    basePlane = Rhino.Geometry.Plane(origin=basePlane_origin, normal=basePlan_normal)

    # Create the txt object
    txt = Rhino.Geometry.TextEntity()
    txt.Text = _txt
    txt.Plane = basePlane
    txt.TextHeight = _txtSize
    txt.Justification = Rhino.Geometry.TextJustification.MiddleCenter

    if _avoidCollisions:
        # Test against the other text items on the sheet
        # First, find / create the bouding box rectangle of the text note
        thisBB = txt.GetBoundingBox(txt.Plane)
        boxXdim = abs(thisBB.Min.X - thisBB.Max.X)
        boxYdim = abs(thisBB.Min.Y - thisBB.Max.Y)
        domainX = ghc.ConstructDomain((boxXdim/2)*-1,  boxXdim/2)
        domainY = ghc.ConstructDomain((boxYdim/2)*-1,  boxYdim/2)
        boundingRect = ghc.Rectangle(txt.Plane, domainX, domainY, 0).rectangle

        # Compare the current text note to the others already in the scene
        # Move the current tag if neccessary
        for eachNeighbor in _neighbors:
            intersection = ghc.CurveXCurve(eachNeighbor, boundingRect)
            if intersection.points != None:
                neighbor = ghc.DeconstuctRectangle(
                    eachNeighbor)  # The overlapping textbox
                neighborY = neighbor.Y  # Returns a domain
                # neighborY = abs(neighborY[0] - neighborY[1]) # Total Y distance

                neighborCP = neighbor.base_plane.Origin
                thisCP = ghc.DeconstuctRectangle(boundingRect).base_plane.Origin

                if thisCP.Y > neighborCP.Y:
                    # Move the tag 'up'
                    neighborMaxY = neighborCP.Y + neighborY[1]
                    thisMinY = thisCP.Y - (boxYdim/2)
                    moveVector = Rhino.Geometry.Vector3d(0, neighborMaxY-thisMinY, 0)
                    boundingRect = ghc.Move(boundingRect, moveVector).geometry
                else:
                    # Move the tag 'down'
                    neighborMinY = neighborCP.Y - neighborY[1]
                    thisMaxY = thisCP.Y + (boxYdim/2)
                    moveVector = Rhino.Geometry.Vector3d(0, neighborMinY-thisMaxY, 0)
                    boundingRect = ghc.Move(boundingRect, moveVector).geometry

                # Re-Set the text tag's origin to the new location
                txt.Plane = ghc.DeconstuctRectangle(boundingRect).base_plane
    else:
        boundingRect = None

    # Add the new text object to the Scene
    txtObj = Rhino.RhinoDoc.ActiveDoc.Objects.AddText(txt)

    # Set the new Text's Layer
    if not rs.IsLayer(_layer):
        rs.AddLayer(_layer)
    rs.ObjectLayer(txtObj, _layer)

    sc.doc = ghdoc

    return boundingRect  # Return the text bounding box


def bakeObject(_obj, _attrs, _layer):
    """ Takes in an obj and bakes to a Layer

    If the Object is a Mesh, will bake that using the Mesh's Vertex Colors. To 
    set these, use the Grasshopper MeshColor component (ghc.MeshColours() ) before
    inputting here.

    If its a Curve input, will try and look for Attribute information in the
    _geomAttributes input.

    If its some other type of geometry, will just use a default attribute for printing.
    """
    doc_object = rs.coercerhinoobject(_obj, True, True)
    geometry = doc_object.Geometry

    sc.doc = Rhino.RhinoDoc.ActiveDoc
    layerT = Rhino.RhinoDoc.ActiveDoc.Layers  # layer table

    if rs.IsMesh(geometry):
        # Find the targer layer index
        parentLayerIndex = Rhino.DocObjects.Tables.LayerTable.FindByFullPath(
            layerT, _layer, True)

        # Create a hatch from the mesh
        guids = []
        hatches, colors = mesh2Hatch(geometry)

        # Bake the Hatches into the Rhino Doc
        for count, hatch in enumerate(hatches):
            attr = Rhino.DocObjects.ObjectAttributes()
            attr.LayerIndex = parentLayerIndex
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            attr.ObjectColor = colors[count]
            attr.DisplayOrder = -1  # 1 = Front, -1 = Back

            guids.append(Rhino.RhinoDoc.ActiveDoc.Objects.AddHatch(hatch, attr))

        # Group the hatches so are manageable
        groupT = Rhino.RhinoDoc.ActiveDoc.Groups
        Rhino.DocObjects.Tables.GroupTable.Add(groupT, guids)
        sc.doc.Views.Redraw()

    elif geometry.GetType() == Rhino.Geometry.PolylineCurve or geometry.GetType() == Rhino.Geometry.Curve:
        # If its a curve, use the input User Determined Attributes

        # Check that the input is a good ObjectAttributes Object
        if type(_attrs) is Rhino.DocObjects.ObjectAttributes:
            attr = _attrs
        else:
            doc_object.Attributes

        rhino_geom = sc.doc.Objects.Add(geometry, attr)

        # Set the new Object's Layer
        if not rs.IsLayer(_layer):
            rs.AddLayer(_layer)
        rs.ObjectLayer(rhino_geom, _layer)

    else:
        # Just bake the regular Geometry with default attributes
        rhino_geom = sc.doc.Objects.Add(geometry, doc_object.Attributes)

        # Set the new Object's Layer
        if not rs.IsLayer(_layer):
            rs.AddLayer(_layer)
        rs.ObjectLayer(rhino_geom, _layer)

    sc.doc = ghdoc


def setOutputLayerVis(_detailViewLayers=[], _udLayersOn=[]):
    # Turn all Layer Visibilities 'Off' except for the designeted layers

    sc.doc = Rhino.RhinoDoc.ActiveDoc
    layers = rs.LayerNames()
    # All the Page's DetailView Layers, as well we as the User Determined 'On'
    allLayersOn = _detailViewLayers + _udLayersOn
    # Add in the Current Active Layer
    allLayersOn.append(str(Rhino.RhinoDoc.ActiveDoc.Layers.CurrentLayer))

    print 'Turning on layers: {}'.format(allLayersOn)
    print '----'

    # Record the Starting State
    layerVisibilites = []  # True/False record (for resetting when done)
    for layer in layers:
        layerVisibilites.append(rs.LayerVisible(layer))

    # Set layers 'off' if they aren't on the list to stay on
    for layer in layers:
        # if list(layer.Split(":"))[-1] not in allLayersOn:
        if layer in allLayersOn:
            rs.LayerVisible(layer, True)
        else:
            rs.LayerVisible(layer, False)

    Rhino.RhinoDoc.ActiveDoc.Views.RedrawEnabled = True
    Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    sc.doc = ghdoc

    return layerVisibilites


def createTempLayer():
    sc.doc = Rhino.RhinoDoc.ActiveDoc

    # Create an Unused Layer Name
    layer_name = sc.doc.Layers.GetUnusedLayerName(False)

    # Add a new Layer to the Document
    layer_index = sc.doc.Layers.Add(layer_name, System.Drawing.Color.Black)

    if layer_index < 0:
        print "Unable to add {} layer.".format(layer_name)
    else:
        print "Added Layer: '{}' ".format(layer_name)

    sc.doc = ghdoc

    return layer_name


def removeTempLayer(_tmpLayerName):
    sc.doc = Rhino.RhinoDoc.ActiveDoc

    # Be sure the temp layer exists?
    if _tmpLayerName in rs.LayerNames():
        print "Removing Layer: '{}'".format(_tmpLayerName)
        tmpLayer = sc.doc.Layers.FindName(_tmpLayerName)
        sc.doc.Layers.Delete(tmpLayer)

    sc.doc = ghdoc


def allLayersReset(_layerVisSettings):
    # Reset all the Layer Vis settings to the original State

    sc.doc = Rhino.RhinoDoc.ActiveDoc

    currentLayer = Rhino.RhinoDoc.ActiveDoc.Layers.CurrentLayer
    layers = rs.LayerNames()
    for i in range(len(layers)):
        # print layers[i], _layerVisSettings[i]
        rs.LayerVisible(layers[i], _layerVisSettings[i])
    Rhino.RhinoDoc.ActiveDoc.Views.RedrawEnabled = True
    Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    sc.doc = ghdoc


def createSinglePDF(_view, _saveFolder, _fileName):
    # Takes in a RhinoView and Exports it to PDF

    subFolder = ''  # '\Exports\\'
    outputFolderPath = '{}{}'.format(_saveFolder, subFolder)

    if outputFolderPath[-1] == '\\':
        pass
    else:
        outputFolderPath = outputFolderPath + '\\'

    # If the folder doesn't already exist, create it
    if os.path.exists(os.path.dirname(outputFolderPath)) == False:
        print 'Creating the folder: {}'.format(outputFolderPath)
        os.makedirs(os.path.dirname(outputFolderPath))
    else:
        pass

    # Layout Page Size in Layout's Units
    pageHeight = sc.doc.Views.ActiveView.PageHeight
    pageWidth = sc.doc.Views.ActiveView.PageWidth

    # Layout Page Size in Inches
    # Ref: https://developer.rhino3d.com/api/RhinoScriptSyntax/#document-UnitScale
    # Ref: https://developer.rhino3d.com/api/RhinoCommon/html/P_Rhino_RhinoDoc_PageUnitSystem.htm
    pageUnitSysemNumber = rs.UnitSystem(in_model_units=False)

    pageHeight = pageHeight * rs.UnitScale(8, pageUnitSysemNumber)  # Type 8 = Inches
    pageWidth = pageWidth * rs.UnitScale(8, pageUnitSysemNumber)
    pageHeight = round(pageHeight, 2)
    pageWidth = round(pageWidth, 2)

    pdf = Rhino.FileIO.FilePdf.Create()
    dpi = 300
    # Should get this from the view?
    size = System.Drawing.Size(pageWidth*dpi, pageHeight*dpi)
    settings = Rhino.Display.ViewCaptureSettings(_view, size, dpi)
    settings.OutputColor = Rhino.Display.ViewCaptureSettings.ColorMode.DisplayColor
    pdf.AddPage(settings)

    filePath = outputFolderPath + _fileName + '.pdf'
    pdf.Write(filePath)


def setActiveViewByName(_targetViewName):
    # https://developer.rhino3d.com/samples/rhinocommon/get-and-set-the-active-view/

    # active view and non-active view names
    active_view_name = sc.doc.Views.ActiveView.ActiveViewport.Name
    non_active_views = [(view.ActiveViewport.Name, view)
                        for view in sc.doc.Views if view.ActiveViewport.Name != active_view_name]

    if _targetViewName != active_view_name:
        if _targetViewName in [seq[0] for seq in non_active_views]:
            sc.doc.Views.ActiveView = [seq[1]
                                       for seq in non_active_views if seq[0] == _targetViewName][0]
            print "Setting Active View to {}".format(_targetViewName)
        else:
            warning = "\"{0}\" is not a valid view name?".format(_targetViewName)
            ghenv.Component.AddRuntimeMessage(
                ghK.GH_RuntimeMessageLevel.Warning, warning)


def findAllDetailViewLayers():
    # Goes to the Active Layer, looks to see if there are any DetailViews,
    # If so, finds the Layer the DetailViews are on and adds the layerIndex to the list to keep 'on'

    layer_Names_ = []
    layer_IDs_ = []

    sc.doc = Rhino.RhinoDoc.ActiveDoc

    active_view = sc.doc.Views.ActiveView  # .ActiveViewport.Name
    detailViews = active_view.GetDetailViews()
    for eachDtlView in detailViews:
        layer_IDs_.append(eachDtlView.Attributes.LayerIndex)
        # print 'View: "{}" has a DetailView: "{}" on LayerIndex: {}'.format(active_view.ActiveViewport.Name, eachDtlView, eachDtlView.Attributes.LayerIndex)

    # Find the right Layer Names from the Index vals
    layer_IDs_ = list(set(layer_IDs_))  # Keep only one of each unique index val

    for i in range(len(layer_IDs_)):
        # Get the Layer and any parents
        layerPath = sc.doc.Layers[layer_IDs_[i]].FullPath
        layerNames = list(layerPath.Split(':'))

        for layerName in layerNames:
            layer_Names_.append(layerPath)
            layer_Names_.append(layerName)

    sc.doc = ghdoc

    print list(set(layer_Names_))
    return list(set(layer_Names_))


# Sort out the filenames to use for outputs
if fileName_ and _geomToBake:
    if len(fileName_) == _geomToBake.BranchCount:
        fileNames = fileName_
    else:
        fileNames = []
        for i in range(_geomToBake.BranchCount):
            fileNames.append("{}_{:03d}".format(fileName_[0], i+1).replace(" ", "_"))
elif _geomToBake and not fileName_:
    fileNames = []
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    # Use the Rhino filename if none provided
    rhinoFileName = sc.doc.Name.replace('.3dm', "")
    sc.doc = ghdoc

    for i in range(_geomToBake.BranchCount):
        fileNames.append("{}_{:03d}".format(rhinoFileName, i+1).replace(" ", "_"))

# Bake all the objects and print to PDF
if _print and _viewName and _saveFolder and _geomToBake:
    setActiveViewByName(_viewName)  # Set to the View to be exported
    detailViewLayers = findAllDetailViewLayers()  # Find the layers to leave on

    for branchNum, branch in enumerate(_geomToBake.Branches):
        try:
            udLayersOn = list(layersOn_.Branch(branchNum))
        except:
            try:
                udLayersOn = list(layersOn_.Branch(0))
            except:
                udLayersOn = []
                msg = 'No input in "LayersOn_" found? Turning all Rhino Scene layers off.'
                ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Remark, msg)

        # Turn off all the Layers (Except the Designated Layers)
        layerVis = setOutputLayerVis(detailViewLayers, udLayersOn)

        # Bake------
        tempLayer_Notes = createTempLayer()
        tempLayer_Geom = createTempLayer()  # Create a temporary layer for the Baked Geometry
        tempLayer_TitleBlock = createTempLayer()
        setActiveViewByName('Top')  # Change to 'Top' View for Baking

        # > Geometry
        for i, geomGUID in enumerate(branch):
            try:
                geomAttrs = _geomAttributes.Branch(branchNum)[i]
            except:
                geomAttrs = None
            # Bake Geometry to the specified layer
            bakeObject(geomGUID, geomAttrs, tempLayer_Geom)

        # > Notes
        # Change to the Designated Output view/Page for Printing PDF
        setActiveViewByName(_viewName)
        dtlViews = sc.doc.Views.ActiveView.GetDetailViews()
        dtlViewTransforms = []
        for eachView in dtlViews:
            dtlViewTransforms.append(eachView.WorldToPageTransform)

        if len(dtlViewTransforms) > 1:
            warning = "Looks like there are two Detail Views on your "\
                "Layout Page? This Probably will not work right with more than one view on a page."
            ghenv.Component.AddRuntimeMessage(
                ghK.GH_RuntimeMessageLevel.Warning, warning)

        # > Find the note's Paperspace location
        noteCP_transformed = []
        if _noteLocations.BranchCount > 0:
            for eachCP in _noteLocations.Branch(branchNum):
                noteCP_transformed.append(ghc.Transform(eachCP, dtlViewTransforms[0]))

            txtBoxes = []  # the note bounding boxes
            for noteNum, eachNote in enumerate(_notesToBake.Branch(branchNum)):
                txtBox = bakeText(_txt=eachNote,
                                  _txtLocation=noteCP_transformed[noteNum],
                                  _layer=tempLayer_Notes,
                                  _txtSize=float(noteTxtSize_),
                                  _neighbors=txtBoxes,
                                  _avoidCollisions=True)
                txtBoxes.append(txtBox)

        # > Layout Page Titleblock Text Objects
        if titleBlockTxtToBake_.BranchCount > 0:
            for i, txtItem in enumerate(titleBlockTxtToBake_.Branch(branchNum)):
                bakeText(_txt=txtItem,
                         _txtLocation=titleBlockTxtLocatons_.Branch(0)[i],
                         _layer=tempLayer_TitleBlock,
                         _txtSize=3.4,
                         _avoidCollisions=False)

        # > Layout Page Table Objects
        if _tablesToBake.BranchCount > 0:
            for table in _tablesToBake.Branch(branchNum):
                for k, cell in table.Cells.items():
                    bakeText(_txt=str(cell.ValueFormated),
                             _txtLocation=cell.Location,
                             _layer=tempLayer_Notes,
                             _txtSize=cell.TextHeight,
                             _avoidCollisions=False)

        # > Export the PDF
        createSinglePDF(sc.doc.Views.ActiveView, _saveFolder,
                        fileNames[branchNum])  # Export to PDF

        # Delete the baked Geometry and the Temporary Layer(s)
        sc.doc = Rhino.RhinoDoc.ActiveDoc
        rs.DeleteObjects(rs.ObjectsByLayer(tempLayer_Geom))
        rs.DeleteObjects(rs.ObjectsByLayer(tempLayer_Notes))
        rs.DeleteObjects(rs.ObjectsByLayer(tempLayer_TitleBlock))
        removeTempLayer(tempLayer_Geom)
        removeTempLayer(tempLayer_Notes)
        removeTempLayer(tempLayer_TitleBlock)

        # Turn all the Layers back to original Visibilities
        allLayersReset(layerVis)

        sc.doc = ghdoc
