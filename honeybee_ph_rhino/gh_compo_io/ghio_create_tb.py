# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Create Thermal Bridge Interface"""

from honeybee_ph_rhino.gh_compo_io import ghio_validators
from honeybee_energy_ph.construction import thermal_bridge
from uuid import uuid4


class IThermalBridge(object):
    """Interface for collect and clean PhThermalBridge user-inputs"""

    display_name = ghio_validators.HBName("display_name")
    psi_value = ghio_validators.Float("psi_value")
    fRsi_value = ghio_validators.Float("fRsi_value")
    length = ghio_validators.FloatPositiveValue("length")

    def __init__(self):
        self.display_name = '_unnamed_bldg_segment_'
        self.psi_value = 0.1
        self.fRsi_value = 0.75
        self.length = 0.0

    def create_hbph_thermal_bridge(self):
        # type () -> thermal_bridge.PhThermalBridge
        new_obj = thermal_bridge.PhThermalBridge(
            uuid4()
        )
        new_obj.display_name = self.display_name
        new_obj.psi_value = self.psi_value
        new_obj.fRsi_value = self.fRsi_value
        new_obj.length = self.length
        return new_obj
