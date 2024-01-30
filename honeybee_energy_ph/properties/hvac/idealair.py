# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties class for PH-HVAC IdealAir Systems"""

from honeybee_energy_ph.hvac import heat_pumps

try:
    from typing import Any, Dict, Optional
except:
    pass  # IronPython

try:
    from honeybee_energy_ph.hvac import heating, ventilation
    from honeybee_energy_ph.hvac.renewable_devices import (
        PhRenewableEnergyDevice,
        PhRenewableEnergyDeviceBuilder,
    )
    from honeybee_energy_ph.hvac.supportive_device import PhSupportiveDevice
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph:\n\t{}".format(e))


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
        self.heat_pump_systems = set()  # type: set[heat_pumps.PhHeatPumpSystem]
        self.exhaust_vent_devices = set()  # type: set[ventilation._ExhaustVentilatorBase]
        self.supportive_devices = set()  # type: set[PhSupportiveDevice]
        self.renewable_devices = set()  # type: set[PhRenewableEnergyDevice]

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

        d["heat_pump_systems"] = [
            sys.to_dict()
            for sys in sorted([_ for _ in self.heat_pump_systems if _ is not None])
        ]

        d["exhaust_vent_devices"] = [
            sys.to_dict()
            for sys in sorted([_ for _ in self.exhaust_vent_devices if _ is not None])
        ]

        d["supportive_devices"] = [
            device.to_dict()
            for device in sorted([_ for _ in self.supportive_devices if _ is not None])
        ]

        d["renewable_devices"] = [
            device.to_dict()
            for device in sorted([_ for _ in self.renewable_devices if _ is not None])
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

        for heat_pump_sys_dict in _input_dict.get("heat_pump_systems", []):
            heat_pump_sys = heat_pumps.PhHeatPumpSystemBuilder.from_dict(
                heat_pump_sys_dict
            )
            new_prop.heat_pump_systems.add(heat_pump_sys)

        for exhaust_vent_device_dict in _input_dict.get("exhaust_vent_devices", []):
            exhaust_device = ventilation.PhExhaustDeviceBuilder.from_dict(
                exhaust_vent_device_dict
            )
            new_prop.exhaust_vent_devices.add(exhaust_device)

        for supportive_device_dict in _input_dict.get("supportive_devices", []):
            supportive_device = PhSupportiveDevice.from_dict(supportive_device_dict)
            new_prop.supportive_devices.add(supportive_device)

        for renewable_device_dict in _input_dict.get("renewable_devices", []):
            renewable_device = PhRenewableEnergyDeviceBuilder.from_dict(
                renewable_device_dict
            )
            new_prop.renewable_devices.add(renewable_device)

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

        for heat_pump_sys in self.heat_pump_systems:
            new_obj.heat_pump_systems.add(heat_pump_sys)

        for exhaust_device in self.exhaust_vent_devices:
            new_obj.exhaust_vent_devices.add(exhaust_device)

        for supportive_device in self.supportive_devices:
            new_obj.supportive_devices.add(supportive_device)

        for renewable_device in self.renewable_devices:
            new_obj.renewable_devices.add(renewable_device)

        return new_obj

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return "{}".format(self.__class__.__name__)
