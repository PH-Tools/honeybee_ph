# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive-House-HVAC-Equipment Properties."""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # Python2.7

try:
    from ladybug_geometry import geometry3d
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee.properties import RoomProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_phhvac.heat_pumps import PhHeatPumpSystem, PhHeatPumpSystemBuilder
    from honeybee_phhvac.heating import PhHeatingSystem, PhHeatingSystemBuilder
    from honeybee_phhvac.renewable_devices import PhRenewableEnergyDevice, PhRenewableEnergyDeviceBuilder
    from honeybee_phhvac.supportive_device import PhSupportiveDevice
    from honeybee_phhvac.ventilation import PhExhaustDeviceBuilder, PhVentilationSystem, _ExhaustVentilatorBase
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class RoomPhHvacEquipmentProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(RoomPhHvacEquipmentProperties_FromDictError, self).__init__(self.msg)


class RoomPhHvacEquipmentProperties(object):
    def __init__(self, _host):
        # type: (RoomProperties) -> None
        self._host = _host
        self.id_num = 0
        self.ventilation_system = None  # type: Optional[PhVentilationSystem]
        self.heating_systems = set()  # type: set[PhHeatingSystem]
        self.heat_pump_systems = set()  # type: set[PhHeatPumpSystem]
        self.exhaust_vent_devices = set()  # type: set[_ExhaustVentilatorBase]
        self.supportive_devices = set()  # type: set[PhSupportiveDevice]
        self.renewable_devices = set()  # type: set[PhRenewableEnergyDevice]

    @property
    def host(self):
        # type: () -> RoomProperties
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Any]
        d = {}

        if abridged:
            d["type"] = "RoomPhHvacEquipmentPropertiesAbridged"
        else:
            d["type"] = "RoomPhHvacEquipmentProperties"

        d["id_num"] = self.id_num

        if self.ventilation_system:
            d["ventilation_system"] = self.ventilation_system.to_dict()
        else:
            d["ventilation_system"] = None

        d["heating_systems"] = [sys.to_dict() for sys in sorted([_ for _ in self.heating_systems if _ is not None])]

        d["heat_pump_systems"] = [sys.to_dict() for sys in sorted([_ for _ in self.heat_pump_systems if _ is not None])]

        d["exhaust_vent_devices"] = [
            sys.to_dict() for sys in sorted([_ for _ in self.exhaust_vent_devices if _ is not None])
        ]

        d["supportive_devices"] = [
            device.to_dict() for device in sorted([_ for _ in self.supportive_devices if _ is not None])
        ]

        d["renewable_devices"] = [
            device.to_dict() for device in sorted([_ for _ in self.renewable_devices if _ is not None])
        ]

        return {"ph_hvac": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], RoomProperties) -> RoomPhHvacEquipmentProperties
        valid_types = ("RoomPhHvacEquipmentProperties", "RoomPhHvacEquipmentPropertiesAbridged")

        if _input_dict["type"] not in valid_types:
            raise RoomPhHvacEquipmentProperties_FromDictError(valid_types, _input_dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _input_dict.get("id_num", 0)

        vent_sys_dict = _input_dict["ventilation_system"]
        if vent_sys_dict:
            ph_vent_sys = PhVentilationSystem.from_dict(vent_sys_dict)
            new_prop.ventilation_system = ph_vent_sys

        for htg_sys_dict in _input_dict.get("heating_systems", []):
            htg_sys = PhHeatingSystemBuilder.from_dict(htg_sys_dict)
            new_prop.heating_systems.add(htg_sys)

        for heat_pump_sys_dict in _input_dict.get("heat_pump_systems", []):
            heat_pump_sys = PhHeatPumpSystemBuilder.from_dict(heat_pump_sys_dict)
            new_prop.heat_pump_systems.add(heat_pump_sys)

        for exhaust_vent_device_dict in _input_dict.get("exhaust_vent_devices", []):
            exhaust_device = PhExhaustDeviceBuilder.from_dict(exhaust_vent_device_dict)
            new_prop.exhaust_vent_devices.add(exhaust_device)

        for supportive_device_dict in _input_dict.get("supportive_devices", []):
            supportive_device = PhSupportiveDevice.from_dict(supportive_device_dict)
            new_prop.supportive_devices.add(supportive_device)

        for renewable_device_dict in _input_dict.get("renewable_devices", []):
            renewable_device = PhRenewableEnergyDeviceBuilder.from_dict(renewable_device_dict)
            new_prop.renewable_devices.add(renewable_device)

        return new_prop

    def apply_properties_from_dict(self, room_prop_dict):
        # type: (Dict[str, Any]) -> None
        """Apply properties from a RoomPhPropertiesAbridged dictionary."""
        return None

    def duplicate(self, new_host=None, include_spaces=True):
        # type: (Optional[RoomProperties], bool) -> RoomPhHvacEquipmentProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Optional[RoomProperties]) -> RoomPhHvacEquipmentProperties
        _host = new_host or self._host
        new_obj = RoomPhHvacEquipmentProperties(_host)
        new_obj.id_num = self.id_num

        new_obj.ventilation_system = self.ventilation_system

        for htg_sys in self.heating_systems:
            new_obj.heating_systems.add(htg_sys)

        for heat_pump_sys in self.heat_pump_systems:
            new_obj.heat_pump_systems.add(heat_pump_sys)

        for exhaust_device in self.exhaust_vent_devices:
            new_obj.exhaust_vent_devices.add(exhaust_device)

        for supportive_device in self.supportive_devices:
            new_obj.supportive_devices.add(supportive_device)

        for renewable_device in self.renewable_devices:
            new_obj.renewable_devices.add(renewable_device)

        return new_obj

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the room, and all the spaces in the room by a specified factor."""
        # TODO: Scale the ducts and pipes
        return None

    # TODO: Add other Transforms

    def __str__(self):
        # type: () -> str
        return "{}(host={!r})".format(self.__class__.__name__, self.host)

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return self.__repr__()
