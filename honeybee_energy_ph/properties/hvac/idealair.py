# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties class for PH-HVAC IdealAir Systems"""

try:
    from typing import Any, Optional, Dict
except:
    pass  # IronPython

try:
    from honeybee_energy_ph.hvac import ventilation, heating, cooling
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph:\n\t{}".format(e))

try:
    from ladybug_geometry.geometry3d.pointvector import Point3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))


class IdealAirSystemPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(IdealAirSystemPhProperties_FromDictError, self).__init__(self.msg)


class IdealAirSystemPhProperties(object):
    """Honeybee-PH Properties for storing PH-style data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.ventilation_system = None  # type: Optional[ventilation.PhVentilationSystem]
        self.heating_systems = set()  # type: set[heating.PhHeatingSystem]
        self.cooling_systems = set()  # type: set[cooling.PhCoolingSystem]
        self.exhaust_vent_devices = set()  # type: set[ventilation._ExhaustVentilatorBase]

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged:
            d["type"] = "IdealAirSystemPhPropertiesAbridged"
        else:
            d["type"] = "IdealAirSystemPhProperties"

        d["id_num"] = self.id_num

        if self.ventilation_system:
            d["ventilation_system"] = self.ventilation_system.to_dict()
        else:
            d["ventilation_system"] = None

        d["heating_systems"] = [
            sys.to_dict()
            for sys in sorted([_ for _ in self.heating_systems if _ is not None])
        ]

        d["cooling_systems"] = [
            sys.to_dict()
            for sys in sorted([_ for _ in self.cooling_systems if _ is not None])
        ]

        d["exhaust_vent_devices"] = [
            sys.to_dict()
            for sys in sorted([_ for _ in self.exhaust_vent_devices if _ is not None])
        ]

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], Any) -> IdealAirSystemPhProperties
        valid_types = ("IdealAirSystemPhProperties", "IdealAirSystemPhPropertiesAbridged")
        if _input_dict["type"] not in valid_types:
            raise IdealAirSystemPhProperties_FromDictError(
                valid_types, _input_dict["type"]
            )

        new_prop = cls(host)
        new_prop.id_num = _input_dict["id_num"]

        vent_sys_dict = _input_dict["ventilation_system"]
        if vent_sys_dict:
            ph_vent_sys = ventilation.PhVentilationSystem.from_dict(vent_sys_dict)
            new_prop.ventilation_system = ph_vent_sys

        for htg_sys_dict in _input_dict.get("heating_systems", []):
            htg_sys = heating.PhHeatingSystemBuilder.from_dict(htg_sys_dict)
            new_prop.heating_systems.add(htg_sys)

        for cooling_sys_dict in _input_dict.get("cooling_systems", []):
            cooling_sys = cooling.PhCoolingSystemBuilder.from_dict(cooling_sys_dict)
            new_prop.cooling_systems.add(cooling_sys)

        for exhaust_vent_device_dict in _input_dict.get("exhaust_vent_devices", []):
            exhaust_device = ventilation.PhExhaustDeviceBuilder.from_dict(
                exhaust_vent_device_dict
            )
            new_prop.exhaust_vent_devices.add(exhaust_device)

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def duplicate(self, new_host=None):
        # type: (Any) -> IdealAirSystemPhProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Any) -> IdealAirSystemPhProperties
        _host = new_host or self._host
        new_obj = IdealAirSystemPhProperties(_host)

        new_obj.id_num = self.id_num
        new_obj.ventilation_system = self.ventilation_system

        for htg_sys in self.heating_systems:
            new_obj.heating_systems.add(htg_sys)

        for clg_sys in self.cooling_systems:
            new_obj.cooling_systems.add(clg_sys)

        for exhaust_device in self.exhaust_vent_devices:
            new_obj.exhaust_vent_devices.add(exhaust_device)

        return new_obj

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return "{}".format(self.__class__.__name__)
