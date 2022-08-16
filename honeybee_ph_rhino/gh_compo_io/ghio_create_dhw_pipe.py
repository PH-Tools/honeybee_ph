# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Create DHW Piping Interfaces"""

try:
    from typing import Union
except ImportError:
    pass  # IronPython 2.7

from ladybug_rhino.togeometry import to_polyline3d
from ladybug_geometry.geometry3d.polyline import Polyline3D, LineSegment3D

from honeybee_energy_ph.hvac import hot_water
from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.gh_compo_io import ghio_validators


class IDHWBranchPipe(object):
    """Interface for collect and clean DHW Branch Piping user-inputs"""
    diameter = ghio_validators.UnitM("diameter")
    display_name = ghio_validators.HBName("display_name")

    def __init__(self, IGH, _geometry, _name, _diameter):
        # type: (gh_io.IGH, Union[Polyline3D, LineSegment3D], str, float) -> None
        self.IGH = IGH
        self.geometry = _geometry
        self.display_name = _name
        self.diameter = _diameter

    def _convert_to_polyline(self, _input):
        """Try to convert input geometry to a Rhino Polyline object."""
        cps = self.IGH.ghpythonlib_components.ControlPoints(_input).points
        return self.IGH.ghpythonlib_components.PolyLine(cps, False)

    @property
    def geometry(self):
        # type: () -> Union[Polyline3D, LineSegment3D]
        return self._geometry

    @geometry.setter
    def geometry(self, _input):
        try:
            self._geometry = to_polyline3d(_input)
        except:
            try:
                self._geometry = to_polyline3d(
                    self._convert_to_polyline(_input))
            except Exception as e:
                raise Exception(
                    "{}\nError: Geometry input {} cannot be converted to an LBT Polyline3D?".format(
                        e, _input)
                )

    def create_hbph_dhw_branch_pipe(self):
        # type: () -> hot_water.PhPipeElement
        hbph_obj = hot_water.PhPipeElement()
        hbph_obj.display_name = self.display_name

        try:
            # If its a Polyline3D
            segments = self.geometry.segments
        except AttributeError:
            # If its a single LineSegment3D
            segments = [self.geometry]

        for segment in segments:
            hbph_obj.add_segment(
                hot_water.PhPipeSegment(segment, self.diameter)
            )

        return hbph_obj


class IDHWRecircPipe(object):
    """Interface for collect and clean DHW Recirculation Piping user-inputs"""
    diameter = ghio_validators.UnitM("diameter")
    display_name = ghio_validators.HBName("display_name")
    insul_thickness = ghio_validators.UnitM("insul_thickness")
    insul_conductivity = ghio_validators.UnitW_MK("insul_conductivity")
    daily_period = ghio_validators.FloatMax24("daily_period")

    def __init__(self, IGH, _geometry, _name="_unnamed_", _diameter=0.0254, _insul_thickness=0.0254, _insul_conductivity=0.04, _insul_reflective=True, _insul_quality=None, _daily_period=24.0):
        # type: (gh_io.IGH, Union[Polyline3D, LineSegment3D], str, float, float, float, bool, None, float) -> None
        self.IGH = IGH
        self.geometry = _geometry
        self.display_name = _name
        self.diameter = _diameter
        self.insul_thickness = _insul_thickness
        self.insul_conductivity = _insul_conductivity
        self.insul_reflective = _insul_reflective
        self.insul_quality = _insul_quality
        self.daily_period = _daily_period

    def _convert_to_polyline(self, _input):
        """Try to convert input geometry to a Rhino Polyline object."""
        cps = self.IGH.ghpythonlib_components.ControlPoints(_input).points
        return self.IGH.ghpythonlib_components.PolyLine(cps, False)

    @property
    def geometry(self):
        # type: () -> Union[Polyline3D, LineSegment3D]
        return self._geometry

    @geometry.setter
    def geometry(self, _input):
        try:
            self._geometry = to_polyline3d(_input)
        except:
            try:
                self._geometry = to_polyline3d(
                    self._convert_to_polyline(_input))
            except Exception as e:
                raise Exception(
                    "{}\nError: Geometry input {} cannot be converted to an LBT Polyline3D?".format(
                        e, _input)
                )

    def create_hbph_dhw_recirc_pipe(self):
        # type: () -> hot_water.PhPipeElement
        hbph_obj = hot_water.PhPipeElement()
        hbph_obj.display_name = self.display_name

        try:
            # If its a Polyline3D
            segments = self.geometry.segments
        except AttributeError:
            # If its a single LineSegment3D
            segments = [self.geometry]

        for segment in segments:
            hbph_obj.add_segment(
                hot_water.PhPipeSegment(
                    segment,
                    self.diameter,
                    self.insul_thickness,
                    self.insul_conductivity,
                    self.insul_reflective,
                    self.insul_quality,
                    self.daily_period,
                )
            )

        return hbph_obj
