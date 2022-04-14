# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create PHX-HVAC objects from Honeybee-Energy-PH HVAC"""

from PHX.model import mech_equip
from honeybee_energy_ph.hvac import ventilation, heating, _base


def _transfer_attributes(_hbeph_obj: _base._PhHVACBase,
                         _phx_obj: mech_equip.PhxMechanicalEquipment) -> mech_equip.PhxMechanicalEquipment:
    """Copy the common attributes from a Honeybee-Energy-PH obj to a PHX-object

    Arguments:
    ---------
        * _hbeph_obj (_base._PhHVACBase): A Honeybee-Energy-PH HVAC Object.
        * _phx_obj (mech_equip.PhxMechanicalEquipment): A PHX-Mechanical
            Equipment object.

    Returns:
    --------
        * (mech_equip.PhxMechanicalEquipment): The input PHX Mechanical Equipment 
            object, with its attribute values set to match the HBEPH object.
    """

    # -- Copy the base scope attributes from HB->PHX
    hb_attrs = {attr_name for attr_name in dir(
        _hbeph_obj) if not attr_name.startswith('_')}
    phx_base_attrs = {attr_name for attr_name in dir(
        _phx_obj) if not attr_name.startswith('_')}

    for attr_nm in hb_attrs.intersection(phx_base_attrs):
        setattr(_phx_obj, attr_nm, getattr(_hbeph_obj, attr_nm))

    # -- Also copy attrs to PHX.params for objects which have them
    if _phx_obj.params:
        phx_params_attrs = {attr_name for attr_name in dir(
            _phx_obj.params) if not attr_name.startswith('_')}
        for attr_nm in hb_attrs.intersection(phx_params_attrs):
            setattr(_phx_obj.params, attr_nm, getattr(_hbeph_obj, attr_nm))

    return _phx_obj


# -- Ventilation


def build_phx_ventilation_sys(_hbeph_vent: ventilation.PhVentilationSystem) -> mech_equip.PhxVentilator:
    """Returns a new Fresh-Air Ventilator built from the hb-energy hvac paramaters.

    This will look at the Space's Host-Room .properties.energy.hvac for data.

    Arguments:
    ----------
        *_hbeph_vent (ventilation.PhVentilationSystem): The HBE-PH Ventilation System
            to build the PHX-Ventilation from.

    Returns:
    --------
        * mech_equip.Ventilator: The new Passive House Ventilator created.
    """

    phx_vent = mech_equip.PhxVentilator()

    phx_vent.display_name = 'Ventilator:'\
        f' {_hbeph_vent.ventilation_unit.sensible_heat_recovery*100 :0.0f}%-HR,'\
        f' {_hbeph_vent.ventilation_unit.latent_heat_recovery*100 :0.0f}%-MR'

    phx_vent.display_name = _hbeph_vent.ventilation_unit.display_name
    phx_vent.fan_power = _hbeph_vent.ventilation_unit.electric_efficiency
    phx_vent.frost_protection_reqd = _hbeph_vent.ventilation_unit.frost_protection_reqd
    phx_vent.frost_temp = _hbeph_vent.ventilation_unit.temperature_below_defrost_used
    phx_vent.in_conditioned_space = _hbeph_vent.ventilation_unit.in_conditioned_space

    return phx_vent


# -- Heating


def build_phx_heating_electric(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterElectric()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_fossil_boiler(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterBoilerFossil()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_wood_boiler(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterBoilerWood()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_district(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterDistrictHeat()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_hp_annual(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterHeatPump.annual()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_hp_monthly(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterHeatPump.monthly()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_hp_combined(_hbeph_heater: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    phx_obj = mech_equip.PhxHeaterHeatPump.combined()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_sys(_htg_sys: heating.PhHeatingSystem) -> mech_equip.PhxHeater:
    """Returns a new PHX-Heating-System based on an input HBE-PH Heating.

    Arguments:
    ----------
        * _htg_sys (heating.PhHeatingSystem): The HBE-PH Heating System to build 
            the new PHX Heating system from.

    Returns:
    --------
        * (mech_equip.PhxHeater): The new PHX Heating System created.
    """

    # -- Mapping HBEPH -> PHX types
    phx_heater_classes = {
        'PhHeatingDirectElectric': build_phx_heating_electric,
        'PhHeatingFossilBoiler': build_phx_heating_fossil_boiler,
        'PhHeatingWoodBoiler': build_phx_heating_wood_boiler,
        'PhHeatingDistrict': build_phx_heating_district,
        'PhHeatingHeatPumpAnnual': build_phx_heating_hp_annual,
        'PhHeatingHeatPumpRatedMonthly': build_phx_heating_hp_monthly,
        'PhHeatingHeatPumpCombined': build_phx_heating_hp_combined,
    }

    # -- Get and build the right heater type
    phx_heater = phx_heater_classes[_htg_sys.heating_type](_htg_sys)
    return phx_heater
