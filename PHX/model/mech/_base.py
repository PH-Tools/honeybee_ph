# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from dataclasses import dataclass
from typing import Optional
from PHX.model.mech.enums import SystemType, DeviceType


@dataclass
class PhxUsageProfile:
    """Is the device used to provide..."""
    space_heating: bool = False
    dhw_heating: bool = False
    cooling: bool = False
    ventilation: bool = False
    humidification: bool = False
    dehumidification: bool = False


class PhxMechanicalEquipmentParams:
    """Base class PHX Mechanical Params"""
    aux_energy: Optional[float] = None
    aux_energy_dhw: Optional[float] = None
    solar_fraction: Optional[float] = None
    in_conditioned_space: bool = True


class PhxMechanicalEquipment:
    """Base class for PHX Mechanical Devices (heaters, tanks, ventilators)"""
    _count: int = 0

    def __init__(self):
        self.system_type_num: SystemType = SystemType.ELECTRIC
        self.device_type_num: DeviceType = DeviceType.ELECTRIC

        self.display_name: str = '_unnamed_equipment_'
        self.id_num: int = self._count
        self.quantity: int = 0
        self.unit: float = 0.0
        self.percent_coverage: float = 0.0
        self.usage_profile: PhxUsageProfile = PhxUsageProfile(
            False, False, False, False, False, False)
        self.params: Optional[PhxMechanicalEquipmentParams] = None

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipment, cls).__new__(cls, *args, **kwargs)
