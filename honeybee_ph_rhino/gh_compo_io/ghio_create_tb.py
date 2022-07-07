# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Create Thermal Bridge Interface"""

try:
    from typing import Union
except ImportError:
    pass  # IronPython 2.7

from ladybug_rhino.togeometry import to_polyline3d
from ladybug_geometry.geometry3d.polyline import Polyline3D, LineSegment3D
from honeybee_ph_rhino.gh_compo_io import ghio_validators
from honeybee_energy_ph.construction import thermal_bridge
from uuid import uuid4
from honeybee_ph_rhino import gh_io


class IThermalBridge(object):
    """Interface for collect and clean PhThermalBridge user-inputs"""

    display_name = ghio_validators.HBName("display_name")
    psi_value = ghio_validators.Float("psi_value")
    fRsi_value = ghio_validators.Float("fRsi_value")

    def __init__(self, _IGH, _geometry):
        # type: (gh_io.IGH, Union[Polyline3D, LineSegment3D]) -> None
        self.IGH = _IGH
        self.geometry = _geometry
        self.display_name = '_unnamed_bldg_segment_'
        self.psi_value = 0.1
        self.fRsi_value = 0.75
        self.quantity = 1.0
        self._group_type = thermal_bridge.PhThermalBridgeType(15)

    def _convert_to_polyline(self, _input):
        """Try to convert to a Rhino Polyline object"""
        cps = self.IGH.ghpythonlib_components.ControlPoints(_input).points
        return self.IGH.ghpythonlib_components.PolyLine(cps, False)

    @property
    def geometry(self):
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
                    "{}\nError: Input {} cannot be converted to an LBT Polyline3D?".format(
                        e, _input)
                )

    @property
    def group_type(self):
        return self._group_type

    @group_type.setter
    def group_type(self, _in):
        self._group_type = thermal_bridge.PhThermalBridgeType(_in)

    def create_hbph_thermal_bridge(self):
        # type () -> thermal_bridge.PhThermalBridge
        if not self.geometry:
            raise Exception(
                "Error: Invalid or None Geometry input? Cannot build Thermal Bridge.")

        new_obj = thermal_bridge.PhThermalBridge(
            uuid4(), self.geometry
        )
        new_obj.display_name = self.display_name
        new_obj.psi_value = self.psi_value
        new_obj.fRsi_value = self.fRsi_value
        new_obj.quantity = self.quantity
        new_obj.group_type = self.group_type.number

        return new_obj
