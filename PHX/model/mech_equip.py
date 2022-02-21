# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from dataclasses import dataclass, field
from typing import ClassVar, Any, Dict, Optional


class PhxMechanicalEquipment:
    """Base class for PHX Mechanical Devices (heaters, tanks, ventilators)"""
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


class PhxHotWaterTank(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.name = 'No_Name'
        self.quantity: int = 1

        self.system_type_num: int = 8
        self.system_type_str: str = 'Water storage'
        self.device_type_num: int = 8
        self.device_type_str: str = 'Water storage'

        self.solar_losses: float = 0.0  # W/K
        self.storage_loss_rate: float = 0.0  # W
        self.standby_losses: float = 0.0  # W/K

        self.storage_capacity: float = 0.0  # Liter
        self.input_option: int = 1

        self.in_conditioned_space: bool = True
        self.tank_room_temp: float = 20.0
        self.tank_water_temp: float = 55.0

        self.aux_energy: float = 0.0
        self.aux_energy_dhw: float = 0.0


class PhxHotWaterHeater(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.name = 'No_Name'

        self.system_type_num: int = 2
        self.system_type_str: str = "Electric resistance space heat / DHW"
        self.device_type_num: int = 2
        self.device_type_str: str = "Electric resistance space heat / DHW"

        self.percent_coverage: float = 0.0
        self.unit: float = 120  # Ltr/h


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
        """Adds a new PHX Mechanical Equipment device to the collection.

        Arguments:
        ----------
            * _key (str): The key to use when storing the new mechanical equipment
            * _equipment (PhxMechanicalEquipment): The new PHX mechanical equipment to 
                add to the collection.

        Returns:
        --------
            * None
        """
        self._equipment[_key] = _equipment
