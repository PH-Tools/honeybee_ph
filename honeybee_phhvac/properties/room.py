# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive-House-HVAC-Equipment Properties."""

try:
    from typing import Any, Dict, Optional, Set
except ImportError:
    pass  # Python2.7

try:
    from ladybug_geometry import geometry3d
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee import room
    from honeybee.properties import RoomProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_ph import space
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))

try:
    from honeybee_phhvac.heat_pumps import PhHeatPumpSystem, PhHeatPumpSystemBuilder
    from honeybee_phhvac.heating import PhHeatingSystem, PhHeatingSystemBuilder
    from honeybee_phhvac.hot_water_system import PhHotWaterSystem
    from honeybee_phhvac.renewable_devices import PhRenewableEnergyDevice, PhRenewableEnergyDeviceBuilder
    from honeybee_phhvac.supportive_device import PhSupportiveDevice
    from honeybee_phhvac.ventilation import PhExhaustDeviceBuilder, PhVentilationSystem, _ExhaustVentilatorBase
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class RoomPhHvacProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(RoomPhHvacProperties_FromDictError, self).__init__(self.msg)


class RoomPhHvacProperties(object):
    def __init__(self, _host):
        # type: (Optional[RoomProperties]) -> None
        self._host = _host
        self.id_num = 0
        self._ventilation_system = None  # type: Optional[PhVentilationSystem]
        self._heating_systems = set()  # type: set[PhHeatingSystem]
        self._heat_pump_systems = set()  # type: set[PhHeatPumpSystem]
        self._exhaust_vent_devices = set()  # type: set[_ExhaustVentilatorBase]
        self._supportive_devices = set()  # type: set[PhSupportiveDevice]
        self._renewable_devices = set()  # type: set[PhRenewableEnergyDevice]
        self._hot_water_system = None  # type: Optional[PhHotWaterSystem]

    @property
    def host(self):
        # type: () -> Optional[RoomProperties]
        return self._host

    @property
    def ventilation_system(self):
        # type: () -> Optional[PhVentilationSystem]
        return self._ventilation_system

    @property
    def heating_systems(self):
        # type: () -> Set[PhHeatingSystem]
        return self._heating_systems

    @property
    def heat_pump_systems(self):
        # type: () -> Set[PhHeatPumpSystem]
        return self._heat_pump_systems

    @property
    def exhaust_vent_devices(self):
        # type: () -> Set[_ExhaustVentilatorBase]
        return self._exhaust_vent_devices

    @property
    def supportive_devices(self):
        # type: () -> Set[PhSupportiveDevice]
        return self._supportive_devices

    @property
    def renewable_devices(self):
        # type: () -> Set[PhRenewableEnergyDevice]
        return self._renewable_devices

    @property
    def hot_water_system(self):
        # type: () -> Optional[PhHotWaterSystem]
        return self._hot_water_system

    def set_ventilation_system(self, _ventilation_system):
        # type: (Optional[PhVentilationSystem]) -> None
        """Set the Ventilation System serving the Room."""
        self._ventilation_system = _ventilation_system

    def add_heating_system(self, _heating_system):
        # type: (Optional[PhHeatingSystem]) -> None
        """Add a Heating System serving the Room."""
        if _heating_system:
            self._heating_systems.add(_heating_system)

    def add_heat_pump_system(self, _heat_pump_system):
        # type: (Optional[PhHeatPumpSystem]) -> None
        """Add a Heat Pump System serving the Room."""
        if _heat_pump_system:
            self._heat_pump_systems.add(_heat_pump_system)

    def add_exhaust_vent_device(self, _exhaust_vent_device):
        # type: (Optional[_ExhaustVentilatorBase]) -> None
        """Add an Exhaust Vent Device serving the Room."""
        if _exhaust_vent_device:
            self._exhaust_vent_devices.add(_exhaust_vent_device)

    def add_supportive_device(self, _supportive_device):
        # type: (Optional[PhSupportiveDevice]) -> None
        """Add a Supportive Device serving the Room."""
        if _supportive_device:
            self._supportive_devices.add(_supportive_device)

    def add_renewable_device(self, _renewable_device):
        # type: (Optional[PhRenewableEnergyDevice]) -> None
        """Add a Renewable Energy Device serving the Room."""
        if _renewable_device:
            self._renewable_devices.add(_renewable_device)

    def set_hot_water_system(self, _hot_water_system):
        # type: (Optional[PhHotWaterSystem]) -> None
        """Set the Hot Water System serving the Room."""
        self._hot_water_system = _hot_water_system

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Any]
        d = {}

        if abridged:
            d["type"] = "RoomPhHvacPropertiesAbridged"
        else:
            d["type"] = "RoomPhHvacProperties"

        d["id_num"] = self.id_num

        d["ventilation_system"] = self.ventilation_system.to_dict() if self.ventilation_system else None

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

        d["hot_water_system"] = self.hot_water_system.to_dict() if self.hot_water_system else None

        return {"ph_hvac": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], Optional[RoomProperties]) -> RoomPhHvacProperties
        valid_types = ("RoomPhHvacProperties", "RoomPhHvacPropertiesAbridged")

        if _input_dict["type"] not in valid_types:
            raise RoomPhHvacProperties_FromDictError(valid_types, _input_dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _input_dict.get("id_num", 0)

        vent_sys_dict = _input_dict.get("ventilation_system")
        if vent_sys_dict:
            new_prop.set_ventilation_system(PhVentilationSystem.from_dict(vent_sys_dict))

        for htg_sys_dict in _input_dict.get("heating_systems", []):
            htg_sys = PhHeatingSystemBuilder.from_dict(htg_sys_dict)
            new_prop.add_heating_system(htg_sys)

        for heat_pump_sys_dict in _input_dict.get("heat_pump_systems", []):
            heat_pump_sys = PhHeatPumpSystemBuilder.from_dict(heat_pump_sys_dict)
            new_prop.add_heat_pump_system(heat_pump_sys)

        for exhaust_vent_device_dict in _input_dict.get("exhaust_vent_devices", []):
            exhaust_device = PhExhaustDeviceBuilder.from_dict(exhaust_vent_device_dict)
            new_prop.add_exhaust_vent_device(exhaust_device)

        for supportive_device_dict in _input_dict.get("supportive_devices", []):
            supportive_device = PhSupportiveDevice.from_dict(supportive_device_dict)
            new_prop.add_supportive_device(supportive_device)

        for renewable_device_dict in _input_dict.get("renewable_devices", []):
            renewable_device = PhRenewableEnergyDeviceBuilder.from_dict(renewable_device_dict)
            new_prop.add_renewable_device(renewable_device)

        hot_water_sys_dict = _input_dict.get("hot_water_system")
        if hot_water_sys_dict:
            new_prop.set_hot_water_system(PhHotWaterSystem.from_dict(hot_water_sys_dict))

        return new_prop

    def apply_properties_from_dict(self, room_prop_dict, mech_systems, *args, **kwargs):
        # type: (Dict[str, Any], Dict[str, dict[str, Any]], list, dict) -> None
        """Apply properties from a RoomPhHvacPropertiesAbridged dictionary."""
        self.id_num = room_prop_dict["id_num"]

        # -- Find the identifiers for each of the room's mechanical systems
        vent_sys_dict = room_prop_dict.get("ventilation_system", {}) or {}
        vent_system_id = vent_sys_dict.get("identifier", None)
        heating_system_ids = [sys.get("identifier") for sys in room_prop_dict.get("heating_systems", [])]
        heat_pump_system_ids = [sys.get("identifier") for sys in room_prop_dict.get("heat_pump_systems", [])]
        exhaust_vent_ids = [sys.get("identifier") for sys in room_prop_dict.get("exhaust_vent_devices", [])]
        supportive_device_ids = [sys.get("identifier") for sys in room_prop_dict.get("supportive_devices", [])]
        renewable_device_ids = [sys.get("identifier") for sys in room_prop_dict.get("renewable_devices", [])]
        hot_water_sys_dict = room_prop_dict.get("hot_water_system", {}) or {}
        hot_water_sys_id = hot_water_sys_dict.get("identifier", None)

        # -- Pull out the actual mechanical systems from the dictionary and apply them to the Properties
        self.set_ventilation_system(mech_systems.get("ventilation_systems", {}).get(vent_system_id, None))

        for sys in (mech_systems.get("heating_systems", {}).get(_id) for _id in heating_system_ids):
            self.add_heating_system(sys)

        for sys in (mech_systems.get("heat_pump_systems", {}).get(_id) for _id in heat_pump_system_ids):
            self.add_heat_pump_system(sys)

        for sys in (mech_systems.get("exhaust_vent_devices", {}).get(_id) for _id in exhaust_vent_ids):
            self.add_exhaust_vent_device(sys)

        for sys in (mech_systems.get("supportive_devices", {}).get(_id) for _id in supportive_device_ids):
            self.add_supportive_device(sys)

        for sys in (mech_systems.get("renewable_devices", {}).get(_id) for _id in renewable_device_ids):
            self.add_renewable_device(sys)

        self.set_hot_water_system(mech_systems.get("hot_water_systems", {}).get(hot_water_sys_id, None))

        return None

    def duplicate(self, new_host=None, include_spaces=True):
        # type: (Optional[RoomProperties], bool) -> RoomPhHvacProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Optional[RoomProperties]) -> RoomPhHvacProperties
        _host = new_host or self._host
        new_obj = RoomPhHvacProperties(_host)
        new_obj.id_num = self.id_num

        new_obj.set_ventilation_system(self.ventilation_system)

        for htg_sys in self.heating_systems:
            new_obj.add_heating_system(htg_sys)

        for heat_pump_sys in self.heat_pump_systems:
            new_obj.add_heat_pump_system(heat_pump_sys)

        for exhaust_device in self.exhaust_vent_devices:
            new_obj.add_exhaust_vent_device(exhaust_device)

        for supportive_device in self.supportive_devices:
            new_obj.add_supportive_device(supportive_device)

        for renewable_device in self.renewable_devices:
            new_obj.add_renewable_device(renewable_device)

        new_obj.set_hot_water_system(self.hot_water_system)

        return new_obj

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the room, and all the spaces in the room by a specified factor."""
        # TODO: Scale any ducts and pipes
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


# -----------------------------------------------------------------------------
# -- Helper Functions to get HVAC Devices and Properties from HB-Room and HB-Space


def get_ph_hvac_prop_from_room(_room):
    # type: (room.Room) -> RoomPhHvacProperties
    """Get the RoomPhHvacProperties of a HB-Room object."""
    return getattr(_room.properties, "ph_hvac")


def get_ph_hvac_from_space(_space):
    # type: (space.Space) -> Optional[RoomPhHvacProperties]
    """Return the "ph_hvac" Properties of a Honeybee-PH Space's host Room."""
    if not _space.host:
        return None
    return getattr(_space.host.properties, "ph_hvac")


def get_ventilation_system_from_space(_space):
    # type: (space.Space) -> Optional[PhVentilationSystem]
    """Get the Ventilation System from a Honeybee-PH Space."""
    ph_hvac = get_ph_hvac_from_space(_space)
    if not ph_hvac:
        return None
    return ph_hvac.ventilation_system


def get_exhaust_vent_devices_from_space(_hph_space):
    # type: (space.Space) -> Set[_ExhaustVentilatorBase]
    """Return a set of all the ExhaustVentilators found on a space's host HB Room."""
    hvac_prop_ph = get_ph_hvac_from_space(_hph_space)
    if not hvac_prop_ph:
        return set()
    return hvac_prop_ph.exhaust_vent_devices


def get_heating_systems_from_space(_space):
    # type: (space.Space)-> Set[PhHeatingSystem]
    """Return the Heating Systems from a Honeybee-PH Space."""
    ph_hvac = get_ph_hvac_from_space(_space)
    if not ph_hvac:
        return set()
    return ph_hvac.heating_systems


def get_heat_pump_systems_from_space(_space):
    # type: (space.Space) -> Set[PhHeatPumpSystem]
    """Return the Heat-Pump Systems from a Honeybee-PH Space."""
    ph_hvac = get_ph_hvac_from_space(_space)
    if not ph_hvac:
        return set()
    return ph_hvac.heat_pump_systems


def get_supportive_devices_from_space(_hph_space):
    # type: ( space.Space) -> Set[PhSupportiveDevice]
    """Return a set of all the SupportiveDevices found on a space's host HB Room."""
    hvac_prop_ph = get_ph_hvac_from_space(_hph_space)
    if not hvac_prop_ph:
        return set()
    else:
        return hvac_prop_ph.supportive_devices


def get_renewable_devices_from_space(_hph_space):
    # type: (space.Space) -> Set[PhRenewableEnergyDevice]
    """Return a set of all the Renewable Energy Devices found on a space's host HB Room."""
    hvac_prop_ph = get_ph_hvac_from_space(_hph_space)
    if not hvac_prop_ph:
        return set()
    else:
        return hvac_prop_ph.renewable_devices


def get_hot_water_system_from_space(_space):
    # type: (space.Space) -> Optional[PhHotWaterSystem]
    """Get the Hot Water System from a Honeybee-PH Space."""
    ph_hvac = get_ph_hvac_from_space(_space)
    if not ph_hvac:
        return None
    return ph_hvac.hot_water_system
