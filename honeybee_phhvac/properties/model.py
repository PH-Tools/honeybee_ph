# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-PH-HVAC Model Properties."""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # Python 2.7

try:
    from itertools import izip as zip  # type: ignore
except ImportError:
    pass  # Python3

try:
    from honeybee import model, extensionutil
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_phhvac.heat_pumps import PhHeatPumpSystemBuilder
    from honeybee_phhvac.heating import PhHeatingSystemBuilder
    from honeybee_phhvac.renewable_devices import PhRenewableEnergyDeviceBuilder
    from honeybee_phhvac.supportive_device import PhSupportiveDevice
    from honeybee_phhvac.ventilation import PhExhaustDeviceBuilder, PhVentilationSystem
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class ModelPhHvacProperties(object):
    def __init__(self, _host):
        # type: (Optional[model.Model]) -> None
        self._host = _host

    @property
    def host(self):
        # type: () -> Optional[model.Model]
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> ModelPhHvacProperties
        _host = new_host or self._host
        new_properties_obj = ModelPhHvacProperties(_host)
        return new_properties_obj

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged == False:
            d["type"] = "ModelPhHvacPropertiesAbridged"
        else:
            d["type"] = "ModelPhHvacProperties"
        return {"ph_hvac": d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict[str, Any], Any) -> ModelPhHvacProperties
        assert _dict["type"] == "ModelPhHvacProperties", "Expected ModelPhHvacProperties. Got {}.".format(_dict["type"])
        new_prop = cls(host)
        return new_prop

    @staticmethod
    def _build_mechanical_devices_from_dict(data):
        # type: (list[dict]) -> dict[str, dict[str, Any]]
        """Return a dict of the mechanical systems, keyed by system-type then identifier."""

        mechanical_systems = {
            "ventilation_systems": {},
            "heating_systems": {},
            "heat_pump_systems": {},
            "exhaust_vent_devices": {},
            "supportive_devices": {},
            "renewable_devices": {},
        }

        for room_dict in data:
            d = room_dict.get("ventilation_system", {})
            if d:
                mechanical_systems["ventilation_systems"][d["identifier"]] = PhVentilationSystem.from_dict(d)

            for d in room_dict.get("heating_systems", []):
                mechanical_systems["heating_systems"][d["identifier"]] = PhHeatingSystemBuilder.from_dict(d)

            for d in room_dict.get("heat_pump_systems", []):
                mechanical_systems["heat_pump_systems"][d["identifier"]] = PhHeatPumpSystemBuilder.from_dict(d)

            for d in room_dict.get("supportive_devices", []):
                mechanical_systems["supportive_devices"][d["identifier"]] = PhSupportiveDevice.from_dict(d)

            for d in room_dict.get("exhaust_vent_devices", []):
                mechanical_systems["exhaust_vent_devices"][d["identifier"]] = PhExhaustDeviceBuilder.from_dict(d)

            for d in room_dict.get("renewable_devices", []):
                mechanical_systems["renewable_devices"][d["identifier"]] = PhRenewableEnergyDeviceBuilder.from_dict(d)

        return mechanical_systems

    @staticmethod
    def load_properties_from_dict(data):
        # type: (Dict[str, Dict]) -> None
        """Load the ModelPhHvacProperties attributes from an HB-Model dictionary as Python objects.

        Loaded objects include: None

        The function is called when re-serializing an HB-Model object from a
        dictionary. It will load honeybee_ph entities as Python objects and returns
        a tuple of dictionaries with all the de-serialized Honeybee-PH objects.

        Arguments:
        ----------
            data: A dictionary representation of an entire honeybee-core Model.
                 Note that this dictionary must have ModelPhProperties
                in order for this method to successfully apply the .ph properties.

                Note: data is an HB-Model dict and .keys() will include:
                [
                    'display_name', 'identifier', 'tolerance',
                    'angle_tolerance', 'rooms', 'type', 'version',
                    'units', 'orphaned_shades', 'properties'
                ]
        """
        assert "ph_hvac" in data["properties"], "Error: HB-Model Dictionary possesses no ModelPhHvacProperties?"

        return None

    def apply_properties_from_dict(self, data):
        # type: (Dict[str, Any]) -> None
        """Apply the ".ph_hvac" properties of a dictionary to the host Model of this object.

        This method is called when the HB-Model is de-serialized from a dict back into
        a Python object. In an 'Abridged' HBJSON file, all the property information
        is stored at the model level, not at the sub-model object level. In that case,
        this method is used to apply the right property data back onto all the sub-model
        objects (faces, rooms, apertures, etc).

        Arguments:
        ----------
            * data (dict[str, Any]): A dictionary representation of an entire honeybee-core
                Model. Note that this dictionary must have ModelPhHvacProperties
                in order for this method to successfully apply the .ph properties.

                Note: data is an HB-Model dict and .keys() will include:
                [
                    'display_name', 'identifier', 'tolerance',
                    'angle_tolerance', 'rooms', 'type', 'version',
                    'units', 'orphaned_shades', 'properties'
                ]

        Returns:
        --------
            * None
        """

        if not self.host:
            return None

        assert "ph_hvac" in data["properties"], "Error: Dictionary possesses no ModelPhHvacProperties?"

        # -------------------------------------------------------------------------------
        # -- 1) Re-build all of the 'ModelPhHvac' objects from the HB-Model dict as python objects
        _ = self.load_properties_from_dict(data)

        # -------------------------------------------------------------------------------
        # -- 2) Collect lists of .ph_hvac property dictionaries at the sub-model level (room, face, etc)
        (
            room_ph_dicts,
            face_ph_dicts,
            shd_ph_dicts,
            ap_ph_dicts,
            dr_ph_dicts,
        ) = extensionutil.model_extension_dicts(data, "ph_hvac", [], [], [], [], [])

        # -------------------------------------------------------------------------------
        # -- 3) Re-Build all of the mechanical HVAC objects from the HB-Model dict as python objects
        mechanical_systems = self._build_mechanical_devices_from_dict(room_ph_dicts)

        # -------------------------------------------------------------------------------
        # -- Pass the Mechanical Devices to the Rooms
        for room, room_dict in zip(self.host.rooms, room_ph_dicts):
            if not room_dict:
                continue
            room.properties.ph_hvac.apply_properties_from_dict(room_dict, mechanical_systems)

        # # -- Pull out all the Apertures, Faces, Shades, and Doors from the HB-Model
        # apertures, faces, shades, doors = [], [], [], []
        # for hb_room in self.host.rooms:
        #     for face in hb_room.faces:
        #         faces.append(face)
        #         for aperture in face.apertures:
        #             apertures.append(aperture)

        # for face, face_dict in zip(faces, face_ph_dicts):
        #     face.properties.ph_hvac.apply_properties_from_dict(face_dict)

        # for aperture, ap_dict in zip(apertures, ap_ph_dicts):
        #     aperture.properties.ph_hvac.apply_properties_from_dict(ap_dict)

        # for shade, ap_dict in zip(shades, shd_ph_dicts):
        #     shade.properties.ph_hvac.apply_properties_from_dict(ap_dict)

        # for door, ap_dict in zip(doors, dr_ph_dicts):
        #     door.properties.ph_hvac.apply_properties_from_dict(ap_dict)
