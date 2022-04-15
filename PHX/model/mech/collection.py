# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, Optional
from PHX.model.mech import _base


@dataclass
class PhxZoneCoverage:
    """Percentage of the load-type covered by the device."""
    zone_num: float = 1.0
    heating: float = 1.0
    cooling: float = 1.0
    ventilation: float = 1.0
    humidification: float = 1.0
    dehumidification: float = 1.0


@dataclass
class PhxMechanicalEquipmentCollection:
    """A collection of all the mechanical equipment (ERV, DHW, etc..) in the project"""
    _count: ClassVar[int] = 0
    id_num: int = 0
    display_name: str = "Ideal Air System"
    sys_type_num: int = 1
    sys_type_str: str = "User defined (ideal system)"

    zone_coverage: PhxZoneCoverage = field(default_factory=PhxZoneCoverage)
    _equipment: Dict[str, _base.PhxMechanicalEquipment] = field(default_factory=dict)

    @property
    def equipment(self):
        return self._equipment.values()

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipmentCollection, cls).__new__(cls, *args, **kwargs)

    def equipment_in_collection(self, _equipment_key) -> bool:
        return _equipment_key in self._equipment.keys()

    def get_mech_equipment_by_key(self, _key: str) -> Optional[_base.PhxMechanicalEquipment]:
        return self._equipment.get(_key, None)

    def add_new_mech_equipment(self, _key: str, _equipment: _base.PhxMechanicalEquipment) -> None:
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
