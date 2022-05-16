# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Colletion Classes"""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, Optional, List
from PHX.model import hvac


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
    _subsystems: Dict[str, hvac.PhxMechanicalSubSystem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    @property
    def subsystems(self):
        """Return a list of all the Mechanical SubSystems in the collection."""
        return self._subsystems.values()

    def subsystem_in_collection(self, _subsystem_key) -> bool:
        """Return True if the a Mech SubSystem with the matching key is already in the collection."""
        return _subsystem_key in self._subsystems.keys()

    def get_mech_subsystem_by_key(self, _key: str) -> Optional[hvac.PhxMechanicalSubSystem]:
        """Returns the mechanical SubSystem with the matching key, or None if not found.

        Arguments:
        ----------
            * _key (str): The key to search the collection for.

        Returns:
        --------
            * (Optional[hvac.PhxMechanicalSubSystem]) The Mechanical Subsystem with
                the matching key, or None if not found.
        """
        return self._subsystems.get(_key, None)

    def get_mech_subsystem_by_id(self, _id_num: int) -> hvac.PhxMechanicalSubSystem:
        """Returns a Mechanical SubSystem from the collection which has a matching id-num.

        Arguments:
        ----------
            * _id_num (int): The Mechanical SubSystem id-number to search for.

        Returns:
        --------
            * (hvac.PhxMechanicalSubSystem): The Mechanical SubSystem found with the
                matching ID-Number. Or Error if not found.
        """
        for sys in self._subsystems.values():
            if sys.id_num == _id_num:
                return sys

        msg = f"Error: Cannot locate the Mechanical Device with id num: {_id_num}"
        raise Exception(msg)

    def add_new_mech_subsystem(self, _key: str, _subsystem: hvac.PhxMechanicalSubSystem) -> None:
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
    def ventilation_subsystems(self) -> List[hvac.PhxMechanicalSubSystem]:
        """Returns a list of the 'Ventilation' subsystems in the collection."""
        return [sys for sys in self.subsystems if sys.device.usage_profile.ventilation]

    @property
    def space_heating_subsystems(self) -> List[hvac.PhxMechanicalSubSystem]:
        """Returns a list of the 'Space Heating' subsystems in the collection."""
        return [sys for sys in self.subsystems if sys.device.usage_profile.space_heating]

    @property
    def cooling_subsystems(self) -> List[hvac.PhxMechanicalSubSystem]:
        """Returns a list of the 'Cooling' subsystems in the collection."""
        return [sys for sys in self.subsystems if sys.device.usage_profile.cooling]

    @property
    def dhw_heating_subsystems(self) -> List[hvac.PhxMechanicalSubSystem]:
        """Returns a list of the 'DHW Heating' subsystems in the collection."""
        return [sys for sys in self.subsystems if sys.device.usage_profile.dhw_heating]
