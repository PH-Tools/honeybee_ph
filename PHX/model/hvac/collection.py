# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Colletion Classes"""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, Optional, List
from PHX.model.hvac import _base


@dataclass
class PhxZoneCoverage:
    """Percentage of the building load-type covered by the subsystem."""
    zone_num: float = 1.0
    heating: float = 1.0
    cooling: float = 1.0
    ventilation: float = 1.0
    humidification: float = 1.0
    dehumidification: float = 1.0


@dataclass
class PhxMechanicalEquipmentCollection:
    """A collection of all the mechanical subsystems (heating, cooling, etc) in the project"""
    _count: ClassVar[int] = 0

    id_num: int = field(init=False, default=0)
    display_name: str = "Ideal Air System"
    sys_type_num: int = 1
    sys_type_str: str = "User defined (ideal system)"

    zone_coverage: PhxZoneCoverage = field(default_factory=PhxZoneCoverage)
    _subsystems: Dict[str, _base.PhxMechanicalSubSystem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    @property
    def subsystems(self):
        return self._subsystems.values()

    def subsystem_in_collection(self, _subsystem_key) -> bool:
        return _subsystem_key in self._subsystems.keys()

    def get_mech_subsystem_by_key(self, _key: str) -> Optional[_base.PhxMechanicalSubSystem]:
        return self._subsystems.get(_key, None)

    def add_new_mech_subsystem(self, _key: str, _subsystem: _base.PhxMechanicalSubSystem) -> None:
        """Adds a new PHX Mechanical SubSystem device to the collection.

        Arguments:
        ----------
            * _key (str): The key to use when storing the new mechanical subsystem
            * _subsystem (_base.PhxMechanicalSubSystem): The new PHX mechanical subsystem to 
                add to the collection.

        Returns:
        --------
            * None
        """
        self._subsystems[_key] = _subsystem

    @property
    def cooling_subsystems(self) -> List[_base.PhxMechanicalSubSystem]:
        """Returns a list of the 'Cooling' subsystems in the collection."""
        return [sys for sys in self.subsystems if sys.device.usage_profile.cooling]
