# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House HVAC Equipment Classes"""

try:
    from typing import Any, Optional
except ImportError:
    pass  # IronPython

from honeybee_energy_ph.hvac import _base


class Ventilator(_base._PhHVACBase):
    def __init__(self):
        super(Ventilator, self).__init__()
        self.display_name = '_unnamed_ventilator_'
        self.id_num = 0
        self.quantity = 1
        self.sensible_heat_recovery = 0.0
        self.latent_heat_recovery = 0.0
        self.electric_efficiency = 0.55
        self.frost_protection_reqd = True
        self.temperature_below_defrost_used = -5
        self.in_conditioned_space = True

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['display_name'] = self.display_name
        d['quantity'] = self.quantity
        d['sensible_heat_recovery'] = self.sensible_heat_recovery
        d['latent_heat_recovery'] = self.latent_heat_recovery
        d['electric_efficiency'] = self.electric_efficiency
        d['frost_protection_reqd'] = self.frost_protection_reqd
        d['temperature_below_defrost_used'] = self.temperature_below_defrost_used
        d['in_conditioned_space'] = self.in_conditioned_space

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> Ventilator
        obj = cls()

        obj.display_name = _input_dict['display_name']
        obj.quantity = _input_dict['quantity']
        obj.sensible_heat_recovery = _input_dict['sensible_heat_recovery']
        obj.latent_heat_recovery = _input_dict['latent_heat_recovery']
        obj.electric_efficiency = _input_dict['electric_efficiency']
        obj.frost_protection_reqd = _input_dict['frost_protection_reqd']
        obj.temperature_below_defrost_used = _input_dict['temperature_below_defrost_used']
        obj.in_conditioned_space = _input_dict['in_conditioned_space']

        return obj

    def __repr__(self):
        return "{}(display_name={!r}, sensible_heat_recovery={:0.2f})".format(self.__class__.__name__, self.display_name, self.sensible_heat_recovery)

    def ToString(self):
        return self.__repr__()


class PhVentilationSystem(_base._PhHVACBase):
    """Passive House Fresh-Air Ventilation System."""

    def __init__(self):
        super(PhVentilationSystem, self).__init__()
        self.display_name = '_unnamed_ph_vent_system_'
        self.sys_type = 1  # '1-Balanced PH ventilation with HR'
        self.duct_01 = None
        self.duct_02 = None
        self._ventilation_unit = None  # type: Optional[Ventilator]

    @property
    def ventilation_unit(self):
        # type: () -> Optional[Ventilator]
        return self._ventilation_unit

    @ventilation_unit.setter
    def ventilation_unit(self, _in):
        # type: (Optional[Ventilator]) -> None
        self._ventilation_unit = _in

        if not self._ventilation_unit:
            return None

        if self._ventilation_unit.display_name == '_unnamed_ventilator_':
            self._ventilation_unit.display_name = self.display_name
        return None

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['identifier'] = str(self.identifier)
        d['name'] = self.display_name
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

        obj.identifier = _input_dict['identifier']
        obj.display_name = _input_dict['name']
        obj.sys_type = _input_dict['sys_type']
        obj.duct_01 = _input_dict['duct_01']
        obj.duct_02 = _input_dict['duct_02']

        vent_unit_dict = _input_dict.get('ventilation_unit', None)
        if vent_unit_dict:
            obj.ventilation_unit = Ventilator.from_dict(vent_unit_dict)

        return obj

    def __repr__(self):
        return "{}(display_name={!r}, sys_type={!r})".format(self.__class__.__name__, self.display_name, self.sys_type)

    def ToString(self):
        return self.__repr__()
