# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from dataclasses import dataclass
from typing import Optional
from PHX.model.mech.enums import DeviceType


@dataclass
class PhxUsageProfile:
    """Is the device used to provide..."""
    space_heating: bool = False
    dhw_heating: bool = False
    cooling: bool = False
    ventilation: bool = False
    humidification: bool = False
    dehumidification: bool = False

    def __add__(self, other: 'PhxUsageProfile') -> 'PhxUsageProfile':
        obj = self.__class__()
        obj.space_heating = any([self.space_heating, other.space_heating])
        obj.dhw_heating = any([self.dhw_heating, other.dhw_heating])
        obj.cooling = any([self.cooling, other.cooling])
        obj.ventilation = any([self.ventilation, other.ventilation])
        obj.humidification = any([self.humidification, other.humidification])
        obj.dehumidification = any([self.dehumidification, other.dehumidification])
        return obj


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
        self.device_type: DeviceType = DeviceType.ELECTRIC
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

    def __add__(self, other: 'PhxMechanicalEquipment') -> 'PhxMechanicalEquipment':
        obj = self.__class__()
        obj.device_type = self.device_type
        obj.display_name = self.display_name
        obj.id_num = self.id_num
        obj.quantity = self.quantity + other.quantity
        obj.unit = self.unit + other.unit
        obj.percent_coverage = self.percent_coverage + other.percent_coverage
        obj.usage_profile = self.usage_profile + other.usage_profile
        return obj

    def __radd__(self, other):
        if isinstance(other, int):
            return self + self
        else:
            return self + other


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
    def system_type(self):
        return self.device.device_type

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalSubSystem, cls).__new__(cls, *args, **kwargs)

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)
