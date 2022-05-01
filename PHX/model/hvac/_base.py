# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from __future__ import annotations
from inspect import signature
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Union
import uuid

from PHX.model.enums.hvac import DeviceType


@dataclass
class PhxUsageProfile:
    """Is the device used to provide..."""
    space_heating: bool = False
    dhw_heating: bool = False
    cooling: bool = False
    ventilation: bool = False
    humidification: bool = False
    dehumidification: bool = False

    def __add__(self, other: PhxUsageProfile) -> PhxUsageProfile:
        obj = self.__class__()
        obj.space_heating = any((self.space_heating, other.space_heating))
        obj.dhw_heating = any((self.dhw_heating, other.dhw_heating))
        obj.cooling = any((self.cooling, other.cooling))
        obj.ventilation = any((self.ventilation, other.ventilation))
        obj.humidification = any((self.humidification, other.humidification))
        obj.dehumidification = any((self.dehumidification, other.dehumidification))
        return obj


@dataclass
class PhxMechanicalEquipmentParams:
    """Base class PHX MechanicalEquipment Params"""
    aux_energy: Optional[float] = None
    aux_energy_dhw: Optional[float] = None
    solar_fraction: Optional[float] = None
    in_conditioned_space: bool = True

    @staticmethod
    def safe_add(attr_1, attr_2):
        if not attr_1 and not attr_2:
            return None
        elif not attr_1 and attr_2:
            return attr_2
        elif attr_1 and not attr_2:
            return attr_1
        else:
            return attr_1 + attr_2

    def __add__(self, other: PhxMechanicalEquipmentParams) -> PhxMechanicalEquipmentParams:
        new_obj = self.__class__()
        new_obj.aux_energy = new_obj.safe_add(self.aux_energy, other.aux_energy)
        new_obj.aux_energy_dhw = new_obj.safe_add(
            self.aux_energy_dhw, other.aux_energy_dhw)
        new_obj.solar_fraction = new_obj.safe_add(
            self.solar_fraction, other.solar_fraction)
        new_obj.in_conditioned_space = any(
            [self.in_conditioned_space, other.in_conditioned_space])
        return new_obj

    def __radd__(self, other):
        if isinstance(other, int):
            return self
        else:
            return self + other


@dataclass
class PhxMechanicalEquipment:
    """Base class for PHX Mechanical Devices (heaters, tanks, ventilators)

    This equipment will be part of a PhxMechanicalSubSystem along with distribution.
    """
    _count: ClassVar[int] = 0

    id_num: int = field(init=False, default=0)
    device_type: DeviceType = DeviceType.ELECTRIC
    display_name: str = '_unnamed_equipment_'
    quantity: int = 0
    unit: float = 0.0
    percent_coverage: float = 0.0
    usage_profile: PhxUsageProfile = field(default_factory=PhxUsageProfile)
    params: PhxMechanicalEquipmentParams = field(
        default_factory=PhxMechanicalEquipmentParams)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    def __add__(self, other: PhxMechanicalEquipment) -> PhxMechanicalEquipment:
        obj = self.__class__()
        # obj.id_num = self.id_num  # TODO: verify this can be removed?
        obj.device_type = self.device_type
        obj.display_name = self.display_name
        obj.quantity = self.quantity + other.quantity
        obj.unit = self.unit + other.unit
        obj.percent_coverage = self.percent_coverage + other.percent_coverage
        obj.usage_profile = self.usage_profile + other.usage_profile
        obj.params = self.params + other.params
        return obj

    def __radd__(self, other) -> PhxMechanicalEquipment:
        if isinstance(other, int):
            return self
        else:
            return self + other

    @classmethod
    def from_kwargs(cls, **kwargs):
        """Allow for the create of base object from arbitrary kwarg input.

        This is used by subclasses dring __add__ or __copy__, otherwise fields
        such as 'id_num' or any other init=False fields result in an AttributeError.
        """
        # fetch the constructor's signature
        cls_fields = {field for field in signature(cls).parameters}

        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
            else:
                new_args[name] = val

        # use the native ones to create the class ...
        return cls(**native_args)


@dataclass
class PhxMechanicalSubSystem:
    """Base class for a sub-system (heating, cooling, ventilation, hot-water)

    This sub-system will include the device/equipment (heater) and may also
    include any distribution such as ducting or piping.
    """

    _count: ClassVar[int] = 0

    _identifier: Union[uuid.UUID, str] = field(init=False, default_factory=uuid.uuid4)
    id_num: int = field(init=False, default=0)
    display_name: str = '_unnamed_mech_subsystem_'
    device: PhxMechanicalEquipment = field(default_factory=PhxMechanicalEquipment)
    distribution = None  # TODO: Distribution....
    percent_coverage: float = 0.0
    usage_profile: PhxUsageProfile = field(default_factory=PhxUsageProfile)

    @property
    def identifier(self):
        return str(self._identifier)

    @identifier.setter
    def identifier(self, _in: str):
        if not _in:
            return
        self._identifier = str(_in)

    @property
    def system_type(self):
        return self.device.device_type

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)
