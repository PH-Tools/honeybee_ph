# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Electric Equipment"""

try:
    from typing import TYPE_CHECKING, Iterable

    if TYPE_CHECKING:
        from honeybee.room import Room
except ImportError:
    pass  # IronPython

try:
    from honeybee.typing import clean_ep_string
except ImportError as e:
    raise ImportError("Failed to import honeybee: {}".format(e))

try:
    from honeybee_energy.load.process import Process
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy: {}".format(e))

try:
    from honeybee_energy_ph.load import ph_equipment
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy_ph: {}".format(e))


def migrate_legacy_equipment_collections(_hb_rooms):
    # type: (Iterable[Room]) -> None
    """Move legacy Equipment Collections onto Process loads for each HB Room.

    This issue #79 migration implements decision 0009. Each PH Equipment becomes
    a zero-watt Process because the legacy Electric Equipment already includes its
    wattage; assigning wattage again would double-count it. Existing Process loads
    are checked by PH Equipment identifier, making the migration idempotent. Legacy
    collections are cleared only after all Rooms are migrated so that collections
    reached through a shared ProgramType remain available to every Room.

    Arguments:
    ----------
        * _hb_rooms (Iterable[Room]): The HB Rooms whose legacy Equipment Collections
            will be migrated.

    Returns:
    --------
        * None
    """
    legacy_collections = []
    legacy_collection_ids = set()

    for hb_room in _hb_rooms:
        room_properties = getattr(hb_room, "properties", None)
        if room_properties is None:
            continue

        energy_properties = getattr(room_properties, "energy", None)
        if energy_properties is None:
            continue

        electric_equipment = energy_properties.electric_equipment
        if electric_equipment is None:
            continue

        equipment_collection = electric_equipment.properties.ph.equipment_collection
        collection_id = id(equipment_collection)
        if collection_id not in legacy_collection_ids:
            legacy_collections.append(equipment_collection)
            legacy_collection_ids.add(collection_id)

        migrated_identifiers = set()
        for process_load in energy_properties.process_loads:
            equipment = process_load.properties.ph.ph_equipment
            if equipment is not None:
                migrated_identifiers.add(equipment.identifier)

        for equipment_key in sorted(equipment_collection.keys()):
            equipment = equipment_collection[equipment_key]
            if equipment.identifier in migrated_identifiers:
                continue

            process = Process(
                identifier=clean_ep_string("HBPH_Process_{}".format(equipment.identifier)),
                watts=0,
                schedule=electric_equipment.schedule,
                fuel_type="Electricity",
                end_use_category="HBPH_Process",
                radiant_fraction=0,
                latent_fraction=0,
                lost_fraction=0,
            )
            process.display_name = equipment.__class__.__name__
            process.properties.ph.ph_equipment = equipment.duplicate(new_host=process.properties.ph)
            energy_properties.add_process_load(process)
            migrated_identifiers.add(equipment.identifier)

    for equipment_collection in legacy_collections:
        equipment_collection.remove_all_equipment()


class ElectricEquipmentPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(ElectricEquipmentPhProperties_FromDictError, self).__init__(self.msg)


class ElectricEquipmentPhProperties(object):
    def __init__(self, _host):
        self._host = _host

        # Migration-only legacy attribute; removal is a later issue #79 step (decision 0009).
        self.equipment_collection = ph_equipment.PhEquipmentCollection(self)

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict
        d = {}

        if abridged:
            d["type"] = "ElectricEquipmentPhPropertiesAbridged"
        else:
            d["type"] = "ElectricEquipmentPhProperties"

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> ElectricEquipmentPhProperties
        valid_types = (
            "ElectricEquipmentPhProperties",
            "ElectricEquipmentPhPropertiesAbridged",
        )
        if _input_dict["type"] not in valid_types:
            raise ElectricEquipmentPhProperties_FromDictError(valid_types, _input_dict["type"])

        new_prop = cls(_host)

        if "equipment_collection" in _input_dict:
            new_prop.equipment_collection = ph_equipment.PhEquipmentCollection.from_dict(
                _input_dict["equipment_collection"], _host=new_prop
            )

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return None

    def __copy__(self, new_host=None):
        # type: (Any) -> ElectricEquipmentPhProperties
        host = new_host or self._host
        new_obj = self.__class__(host)
        new_obj.equipment_collection = self.equipment_collection.duplicate(host)
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> ElectricEquipmentPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(equipment_collection={})".format(self.__class__.__name__, self.equipment_collection)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
