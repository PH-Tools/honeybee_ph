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
    """Base class PHX MechanicalEquipment Params"""
    aux_energy: Optional[float] = None
    aux_energy_dhw: Optional[float] = None
    solar_fraction: Optional[float] = None
    in_conditioned_space: bool = True


class PhxMechanicalEquipment:
    """Base class for PHX Mechanical Devices (heaters, tanks, ventilators)

    This equipment will be part of a PhxMechanicalSubSystem along with distribution.
    """
    _count: int = 0

    def __init__(self):
        self.device_type_num: DeviceType = DeviceType.ELECTRIC
        self.display_name: str = '_unnamed_equipment_'
        self.id_num: int = self._count
        self.quantity: int = 0
        self.unit: float = 0.0
        self.percent_coverage: float = 0.0
        self.usage_profile: PhxUsageProfile = PhxUsageProfile(
            False, False, False, False, False, False)
        self.params: PhxMechanicalEquipmentParams = PhxMechanicalEquipmentParams()

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipment, cls).__new__(cls, *args, **kwargs)


class PhxMechanicalSubSystem:
    """Base class for a sub-system (heating, cooling, ventilation, hot-water)

    This sub-system will include the device/equipment (heater) and may also
    include any distribution such as ducting or piping.
    """

    _count: int = 0

    def __init__(self):
        self.display_name: str = '_unnamed_mech_subsystem_'
        self.id_num: int = self._count

        self.device: PhxMechanicalEquipment = PhxMechanicalEquipment()
        self.distribution = None  # TODO: Distribution....
        self.percent_coverage: float = 0.0
        self.usage_profile: PhxUsageProfile = PhxUsageProfile(
            False, False, False, False, False, False)

    @property
    def system_type_num(self):
        return SystemType(self.device.device_type_num.value)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalSubSystem, cls).__new__(cls, *args, **kwargs)

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)
