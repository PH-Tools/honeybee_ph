# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Create SHW Mech System Interface"""

try:
    from typing import List, Optional, Union
except ImportError:
    pass  # IronPython 2.7

try:  # import the honeybee extension
    from honeybee.room import Room
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the honeybee-energy extension
    from honeybee_energy import shw
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy:\n\t{}'.format(e))

from honeybee_energy_ph.hvac import hot_water
from honeybee_ph_rhino.gh_compo_io import ghio_validators


class ICreateSHWSystem(object):
    """Interface for collect and clean SHW System user-inputs."""
    display_name = ghio_validators.HBName("display_name", default="SHW System")
    efficiency = ghio_validators.FloatPercentage("efficiency")
    loss_coeff = ghio_validators.UnitW_K("loss_coeff")

    def __init__(self, sys_type, display_name, efficiency, condition, loss_coeff, tank_1, tank_2, buffer_tank, solar_tank, heaters, branch_piping, recirc_piping):
        # type: (str, str, Optional[float], Union[None, Room, int], Union[None, float, str], Optional[hot_water.PhSHWTank], Optional[hot_water.PhSHWTank], Optional[hot_water.PhSHWTank], Optional[hot_water.PhSHWTank], List, List, List) -> None
        self.sys_type = sys_type
        self.display_name = display_name
        self.efficiency = efficiency
        self.condition = condition
        self.loss_coeff = loss_coeff or 6  # W/K
        self.tank_1 = tank_1
        self.tank_2 = tank_2
        self.buffer_tank = buffer_tank
        self.solar_tank = solar_tank
        self.heaters = heaters
        self.branch_piping = branch_piping
        self.recirc_piping = recirc_piping

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, _in):
        # -- Copied from HB-Energy SHW System component
        if _in is None:
            self._condition = 22
        elif isinstance(_in, Room):
            self._condition = _in.identifier
        else:
            try:
                self._condition = float(_in)
            except Exception:
                raise ValueError(
                    'Input _condition_ must be a Room in which the system is located '
                    'or a number\nfor the ambient temperature in which the hot water '
                    'tank is located [C].\nGot {}.'.format(type(_in))
                )

    def create_hb_shw_obj(self):
        # type: () -> shw.SHWSystem

        # -- Create the basic HB-Energy object
        shw_sys = shw.SHWSystem(self.display_name, self.sys_type,
                                self.efficiency, self.condition, self.loss_coeff)
        shw_sys.display_name = self.display_name

        # -- Add any HB-PH Tanks
        if self.tank_1:
            shw_sys.properties.ph.tank_1 = self.tank_1
        if self.tank_2:
            shw_sys.properties.ph.tank_2 = self.tank_2
        if self.buffer_tank:
            shw_sys.properties.ph.tank_buffer = self.buffer_tank
        if self.solar_tank:
            shw_sys.properties.ph.tank_solar = self.solar_tank

        # -- Add any HB-PH Heaters and Piping
        for heater in self.heaters:
            shw_sys.properties.ph.add_heater(heater)
        for branch_piping in self.branch_piping:
            shw_sys.properties.ph.add_branch_piping(branch_piping)
        for recirc_piping in self.recirc_piping:
            shw_sys.properties.ph.add_recirc_piping(recirc_piping)

        return shw_sys
