# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Adding PH-Equipment to Honeybee Rooms"""

try:
    from typing import List
except ImportError:
    pass  # IronPython 2.7

from honeybee import room
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.load import equipment
from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier
from honeybee.typing import clean_and_id_ep_string, clean_ep_string
from honeybee_ph_standards.programtypes.default_elec_equip import ph_default_equip


from honeybee_energy_ph.load import ph_equipment

# -- NOTE: remember, we have to do it this way since the HBE-Elec-Equip is NOT duplicated
# -- during normal operation, so changes to object state here would propagate outwards (ie:
# -- backwards upstream in the GH definition) and cause unwanted behavior.


class HBElecEquipWithRooms:
    """An HBE-ElectricEquipment object, with a list of the rooms it is assigned to."""

    def __init__(self, _hb_electric_equipment):
        # type: (equipment.ElectricEquipment) -> None
        self.hb_electric_equipment = _hb_electric_equipment.duplicate()
        self.hb_rooms = []  # type: list[room.Room]

    def set_hb_room_ee(self):
        # type: () -> None
        """Set all of the HB-Rooms in the set with the HBE-ElecEquipment obj."""
        # -- Duplicate the HBE-ElecEquipment and
        # -- manually reset the identifier and name
        dup_hb_ee = self.hb_electric_equipment.duplicate()
        dup_hb_ee.identifier = clean_and_id_ep_string(dup_hb_ee.display_name)

        new_rooms = []
        for hb_room in self.hb_rooms:
            dup_room = hb_room.duplicate()
            dup_room.properties.energy.electric_equipment = dup_hb_ee
            new_rooms.append(dup_room)

        self.hb_rooms = new_rooms

    def add_hbph_equipment(self, ph_equip_item):
        # type: (ph_equipment.PhEquipment) -> None
        self.hb_electric_equipment.properties.ph.equipment_collection.add_equipment(
            ph_equip_item)

    def set_hb_ee_wattage(self):
        # type: () -> None
        """Set the HBE-ElecEquip watts-per-area from the PH-Equip."""
        dup_ee = self.hb_electric_equipment.duplicate()

        ph_equip = dup_ee.properties.ph.equipment_collection
        total_wattage = sum(ph_equip.total_collection_wattage(hb_room)
                            for hb_room in self.hb_rooms)
        total_m2 = sum(rm.floor_area for rm in self.hb_rooms)
        avg_wattage_per_m2 = total_wattage / total_m2
        dup_ee.watts_per_area = avg_wattage_per_m2

        self.hb_electric_equipment = dup_ee

    def __str__(self):
        return '{}(hb_electric_equipment={}, hb_rooms={})'.format(
            self.__class__.__name__, self.hb_electric_equipment, self.hb_rooms)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class HBElecEquipCollection:
    """A collection of HB-ElecEquipWithRooms objects."""

    def __init__(self):
        self._collection = {}

    def add_to_collection(self, _hb_room):
        # type: (room.Room) -> None
        """Use the HB-Room's ElectricEquipment.identifier as the key to log the HBElecEquipWithRooms"""
        ee_id = _hb_room.properties.energy.electric_equipment.identifier
        try:
            self._collection[ee_id].hb_rooms.append(_hb_room.duplicate())
        except KeyError:
            new_ee_with_rooms = HBElecEquipWithRooms(
                _hb_electric_equipment=_hb_room.properties.energy.electric_equipment
            )
            new_ee_with_rooms.hb_rooms.append(_hb_room)
            self._collection[ee_id] = new_ee_with_rooms

    def values(self):
        return self._collection.values()

    def keys(self):
        return self._collection.keys()

    def items(self):
        return self._collection.items()

    def __str__(self):
        return '{}({} items in the collection)'.format(self.__class__.__name__, len(self.keys()))

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


def _create_default_hb_elec_equip(_identifier):
    # type: (str) -> equipment.ElectricEquipment
    """Returns a default HB-Elec-Equip object with a constant operation schedule."""
    return equipment.ElectricEquipment(
        identifier=_identifier,
        watts_per_area=0.0,
        schedule=ScheduleRuleset.from_constant_value(
            clean_ep_string(clean_and_id_ep_string('EEConstantSchedule')),
            1.0,
            schedule_type_limit_by_identifier('Fractional')
        ),
        radiant_fraction=0.0,
        latent_fraction=0.0,
        lost_fraction=0.0
    )


def clean_rooms_elec_equip(_hb_rooms):
    # type: (room.Room) -> List[room.Room]
    """Cleanup cases where the HB-room does not already have an HBE-ElectricEquipment"""

    hb_rooms_ = []
    for hb_room in _hb_rooms:
        if hb_room.properties.energy.electric_equipment is None:
            hb_room.properties.energy.electric_equipment = _create_default_hb_elec_equip(
                hb_room.display_name)
        hb_rooms_.append(hb_room)

    return hb_rooms_


def add_Phius_default_equipment_to_list(_equipment, _defaults=1):
    # type: (List[ph_equipment.PhEquipment], int) -> List[ph_equipment.PhEquipment]
    """Adds Phius default equipment to an existing equipment list

    Arguments:
    ----------
        * _equipment (List[ph_equipment.PhEquipment]): A list of any existing PH-Equipment
            to add the new equipment to.
        * _defaults (int): input either
            0 = No defaults
            1 = Residential Single family
            2 = Multifamily Residential
            3 = Multifamily NonResidential

    Returns:
    --------
        * (List[ph_equipment.PhEquipment]): A list of PH-Equipment.
    """

    equipment_list_ = _equipment[:]

    if _defaults == 1:  # Residential Single family:
        equipment_list_.append(ph_equipment.PhDishwasher(
            _defaults=ph_default_equip['PhDishwasher']['PHIUS']))
        equipment_list_.append(ph_equipment.PhClothesWasher(
            _defaults=ph_default_equip['PhClothesWasher']['PHIUS']))
        equipment_list_.append(ph_equipment.PhClothesDryer(
            _defaults=ph_default_equip['PhClothesDryer']['PHIUS']))
        equipment_list_.append(ph_equipment.PhFridgeFreezer(
            _defaults=ph_default_equip['PhFridgeFreezer']['PHIUS']))
        equipment_list_.append(ph_equipment.PhCooktop(
            _defaults=ph_default_equip['PhCooktop']['PHIUS']))
        equipment_list_.append(ph_equipment.PhPhiusMEL(
            _defaults=ph_default_equip['PhPhiusMEL']['PHIUS']))
        equipment_list_.append(ph_equipment.PhPhiusLightingInterior(
            _defaults=ph_default_equip['PhPhiusLightingInterior']['PHIUS']))
        equipment_list_.append(ph_equipment.PhPhiusLightingExterior(
            _defaults=ph_default_equip['PhPhiusLightingExterior']['PHIUS']))

    if _defaults == 2:  # Multifamily Residential
        equipment_list_.append(ph_equipment.PhDishwasher(
            _defaults=ph_default_equip['PhDishwasher']['PHIUS']))
        equipment_list_.append(ph_equipment.PhClothesWasher(
            _defaults=ph_default_equip['PhClothesWasher']['PHIUS']))
        equipment_list_.append(ph_equipment.PhClothesDryer(
            _defaults=ph_default_equip['PhClothesDryer']['PHIUS']))
        equipment_list_.append(ph_equipment.PhFridgeFreezer(
            _defaults=ph_default_equip['PhFridgeFreezer']['PHIUS']))
        equipment_list_.append(ph_equipment.PhCooktop(
            _defaults=ph_default_equip['PhCooktop']['PHIUS']))

    if _defaults == 3:  # Multifamily NonResidential
        pass

    print(equipment_list_)
    return equipment_list_


def add_Phi_default_equipment_to_list(_equipment, _defaults=0):
    # type: (List[ph_equipment.PhEquipment], int) -> List[ph_equipment.PhEquipment]
    """Adds Phius default equipment to an existing equipment list

    Arguments:
    ----------
        * _equipment (List[ph_equipment.PhEquipment]): A list of any existing PH-Equipment
            to add the new equipment to.

        * _default (int): input either
            0 = No defaults
            1 = Residential Single family

    Returns:
    --------
        * (List[ph_equipment.PhEquipment]): A list of PH-Equipment.
    """

    equipment_list_ = _equipment[:]

    if _defaults == 1:
        equipment_list_.append(ph_equipment.PhDishwasher(
            _defaults=ph_default_equip['PhDishwasher']['PHI']))
        equipment_list_.append(ph_equipment.PhClothesWasher(
            _defaults=ph_default_equip['PhClothesWasher']['PHI']))
        equipment_list_.append(ph_equipment.PhClothesDryer(
            _defaults=ph_default_equip['PhClothesDryer']['PHI']))
        equipment_list_.append(ph_equipment.PhFridgeFreezer(
            _defaults=ph_default_equip['PhFridgeFreezer']['PHI']))
        equipment_list_.append(ph_equipment.PhCooktop(
            _defaults=ph_default_equip['PhCooktop']['PHI']))

    return equipment_list_
