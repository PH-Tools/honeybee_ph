# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Electrical Equipment (Appliances) Classes"""

from typing import Dict, Optional, Any
from dataclasses import dataclass, field


class PhxElectricalEquipment:
    """Base class for PHX Electrical Equipment (dishwashers, laundry, lighting, etc.)"""
    _count: int = 0

    def __init__(self):
        self.display_name: str = '_unnamed_equipment_'
        self.id_num: int = self._count
        self.comment: Optional[str] = None
        self.reference_quantity: int = 1
        self.quantity: int = 1
        self.in_conditioned_space: bool = True
        self.reference_energy_norm: int = 2
        self.energy_demand: float = 100
        self.energy_demand_per_use: float = 100
        self.combined_energy_factor: float = 0

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxElectricalEquipment, cls).__new__(cls, *args, **kwargs)


class PhxDishwasher(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.capacity_type: int = 1
        self.capacity: float = 1
        self.water_connection: int = 1


class PhxClothesWasher(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.capacity: float = 0.0814  # m3
        self.modified_energy_factor: float = 2.38
        self.connection: int = 1  # DHW Connection
        self.utilization_factor: float = 1


class PhxClothesDryer(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.dryer_type: int = 4  # Condensation dryer
        self.gas_consumption: float = 0  # kWh
        self.gas_efficiency_factor: float = 2.67
        self.field_utilization_factor_type: int = 1  # Timer
        self.field_utilization_factor: float = 1.18


class PhxRefrigerator(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()


class PhxFreezer(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()


class PhxFridgeFreezer(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()


class PhxCooktop(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.cooktop_type: int = 1  # Electric


class PhxMEL(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()


class PhxLightingInterior(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.frac_high_efficiency: float = 1.0


class PhxLightingExterior(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.frac_high_efficiency: float = 1.0


class PhxLightingGarage(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.frac_high_efficiency: float = 1.0


@dataclass
class PhxElectricEquipmentCollection:
    """A collection of all the electric-equipment (laundry, lighting, etc.) on the Zone"""
    _equipment: Dict[str, Any] = field(default_factory=dict)

    @property
    def equipment(self):
        return self._equipment.values()

    def equipment_in_collection(self, _equipment_key) -> bool:
        return _equipment_key in self._equipment.keys()

    def get_equipment_by_key(self, _key: str) -> Optional[PhxElectricalEquipment]:
        return self._equipment.get(_key, None)

    def add_new_equipment(self, _key: str, _equipment: PhxElectricalEquipment) -> None:
        """Adds a new PHX Electric-Equipment device to the collection.

        Arguments:
        ----------
            * _key (str): The key to use when storing the new electric-equipment
            * _equipment (PhxElectricalEquipment): The new PHX electric-equipment to 
                add to the collection.

        Returns:
        --------
            * None
        """
        self._equipment[_key] = _equipment
