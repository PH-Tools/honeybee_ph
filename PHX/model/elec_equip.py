# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Electrical Equipment (Appliances) Classes"""

from typing import Optional, ClassVar, Union, List
from dataclasses import dataclass, field
import uuid


@dataclass
class PhxElectricalEquipment:
    """Base class for PHX Electrical Equipment (dishwashers, laundry, lighting, etc.)"""
    _count: ClassVar[int] = 0

    identifier: Union[uuid.UUID, str] = field(default_factory=uuid.uuid4)
    display_name: str = '_unnamed_equipment_'
    id_num: int = field(init=False, default=0)
    comment: str = ""
    reference_quantity: int = 1
    quantity: int = 1
    in_conditioned_space: bool = True
    reference_energy_norm: int = 2
    energy_demand: float = 100
    energy_demand_per_use: float = 100
    combined_energy_factor: float = 0

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count


class PhxDishwasher(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "Kitchen Dishwasher"
        self.capacity_type: int = 1
        self.capacity: float = 1
        self.water_connection: int = 1


class PhxClothesWasher(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "Laundry - washer"
        self.capacity: float = 0.0814  # m3
        self.modified_energy_factor: float = 2.38
        self.connection: int = 1  # DHW Connection
        self.utilization_factor: float = 1


class PhxClothesDryer(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "Laundry - dryer"
        self.dryer_type: int = 4  # Condensation dryer
        self.gas_consumption: float = 0  # kWh
        self.gas_efficiency_factor: float = 2.67
        self.field_utilization_factor_type: int = 1  # Timer
        self.field_utilization_factor: float = 1.18


class PhxRefrigerator(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "Kitchen refrigerator"


class PhxFreezer(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "kitchen freezer"


class PhxFridgeFreezer(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "Kitchen fridge/freeze combo"


class PhxCooktop(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "Kitchen cooking"
        self.cooktop_type: int = 1  # Electric


class PhxMEL(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "PHIUS+ MELS"


class PhxLightingInterior(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "PHIUS+ Interior Lighting"
        self.frac_high_efficiency: float = 1.0


class PhxLightingExterior(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "PHIUS+ Exterior Lighting"
        self.frac_high_efficiency: float = 1.0


class PhxLightingGarage(PhxElectricalEquipment):
    def __init__(self):
        super().__init__()
        self.display_name = "PHIUS+ Garage Lighting"
        self.frac_high_efficiency: float = 1.0


class PhxCustomElec(PhxElectricalEquipment):
    def __init__(self):
        self.display_name = "User defined"
        super().__init__()


class PhxCustomLighting(PhxElectricalEquipment):
    def __init__(self):
        self.display_name = "User defined - lighting"
        super().__init__()


class PhxCustomMEL(PhxElectricalEquipment):
    def __init__(self):
        self.display_name = "User defined - Misc electrical loads"
        super().__init__()


# -----------------------------------------------------------------------------


@dataclass
class PhxElectricEquipmentCollection:
    """A collection of all the electric-equipment (laundry, lighting, etc.) on the Zone"""
    _equipment: dict = field(default_factory=dict)

    @property
    def equipment(self) -> List[PhxElectricalEquipment]:
        if not self._equipment:
            return []
        return sorted(self._equipment.values(), key=lambda e: e.display_name)

    def equipment_in_collection(self, _equipment_key) -> bool:
        """Returns True if the key supplied is in the existing equipment set."""
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

    def __bool__(self) -> bool:
        return bool(self._equipment)
