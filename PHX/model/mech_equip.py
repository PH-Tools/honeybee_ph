# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from dataclasses import dataclass, field
from typing import ClassVar, Any, Dict, Optional


class PhxMechanicalEquipment:
    _count: int = 0

    def __init__(self):
        self.name: str = '_unnamed_equipment_'
        self.id_num: int = self._count
        self.system_type_num = 0
        self.system_type_str = ''
        self.device_type_num = 0
        self.device_type_str = ''

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipment, cls).__new__(cls, *args, **kwargs)


class PhxVentilator(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.quantity: int = 1
        self.system_type_num: int = 1
        self.system_type_str: str = 'Mechanical ventilation'
        self.device_type_num: int = 1
        self.device_type_str: str = 'Mechanical ventilation unit'
        self.heat_recovery_efficiency: float = 0.0
        self.moisture_recovery_efficiency: float = 0.0
        self.fan_power: float = 0.55
        self.frost_protection_reqd: bool = True
        self.frost_temp: float = -5.0
        self.in_conditioned_space: bool = True


@dataclass
class PhxZoneCoverage:
    zone_num: int = 1
    heating: int = 1
    cooling: int = 1
    ventilation: int = 1
    humidification: int = 1
    dehumidification: int = 1


@dataclass
class PhxMechanicalEquipmentCollection:
    """A collection of all the mechanical equipment (ERV, DHW, etc..) in the project"""
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = "Ideal Air System"
    sys_type_num: int = 1
    sys_type_str: str = "User defined (ideal system)"

    zone_coverage: PhxZoneCoverage = field(default_factory=PhxZoneCoverage)
    _equipment: Dict[str, Any] = field(default_factory=dict)

    @property
    def equipment(self):
        return self._equipment.values()

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipmentCollection, cls).__new__(cls, *args, **kwargs)

    def equipment_in_collection(self, _equipment_key) -> bool:
        return _equipment_key in self._equipment.keys()

    def get_mech_equipment_by_key(self, _key: str) -> Optional[PhxMechanicalEquipment]:
        return self._equipment.get(_key, None)

    def add_new_mech_equipment(self, _key: str, _equipment: PhxMechanicalEquipment) -> None:
        """

        Arguments:
        ----------
            *

        Returns:
        --------
            *
        """
        self._equipment[_key] = _equipment
