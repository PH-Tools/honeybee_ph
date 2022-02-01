# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House HVAC Equipment Classes"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython


class Ventilator:
    def __init__(self):
        self.name = '_unnamed_ventilator_'
        self.sensible_heat_recovery = 0.0
        self.latent_heat_recovery = 0.0
        self.electric_efficiency = 0.55
        self.temperature_below_defrost_used = -5
        self.in_conditioned_space = True

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['name'] = self.name
        d['sensible_heat_recovery'] = self.sensible_heat_recovery
        d['latent_heat_recovery'] = self.latent_heat_recovery
        d['electric_efficiency'] = self.electric_efficiency
        d['temperature_below_defrost_used'] = self.temperature_below_defrost_used
        d['in_conditioned_space'] = self.in_conditioned_space

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> Ventilator
        obj = cls()

        obj.name = _input_dict['name']
        obj.sensible_heat_recovery = _input_dict['sensible_heat_recovery']
        obj.latent_heat_recovery = _input_dict['latent_heat_recovery']
        obj.electric_efficiency = _input_dict['electric_efficiency']
        obj.temperature_below_defrost_used = _input_dict['temperature_below_defrost_used']
        obj.in_conditioned_space = _input_dict['in_conditioned_space']

        return obj

    def __repr__(self):
        return "{}(name={!r}, sensible_heat_recovery={:0.2f})".format(self.__class__.__name__, self.name, self.sensible_heat_recovery)

    def ToString(self):
        return self.__repr__()


class PhVentilationSystem:
    """Passive House Fresh-Air Ventilation System."""

    def __init__(self):
        self.name = '_unnamed_ph_vent_system_'
        self.sys_type = 1  # '1-Balanced PH ventilation with HR'
        self.duct_01 = None
        self.duct_02 = None
        self.ventilation_unit = None

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['name'] = self.name
        d['sys_type'] = self.sys_type
        d['duct_01'] = self.duct_01
        d['duct_02'] = self.duct_02

        if self.ventilation_unit:
            d['ventilation_unit'] = self.ventilation_unit.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhVentilationSystem
        obj = cls()

        obj.name = _input_dict['name']
        obj.sys_type = _input_dict['sys_type']
        obj.duct_01 = _input_dict['duct_01']
        obj.duct_02 = _input_dict['duct_02']

        vent_unit_dict = _input_dict.get('ventilation_unit', None)
        if vent_unit_dict:
            obj.ventilation_unit = Ventilator.from_dict(vent_unit_dict)

        return obj

    def __repr__(self):
        return "{}(name={!r}, sys_type={!r})".format(self.__class__.__name__, self.name, self.sys_type)

    def ToString(self):
        return self.__repr__()
