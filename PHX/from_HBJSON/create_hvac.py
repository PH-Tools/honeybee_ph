# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create PHX-HVAC objects from Honeybee-Energy-PH HVAC"""

from PHX.model import mech
from honeybee_energy_ph.hvac import ventilation, heating, cooling, _base


def _transfer_attributes(_hbeph_obj: _base._PhHVACBase,
                         _phx_obj: mech.PhxMechanicalEquipment) -> mech.PhxMechanicalEquipment:
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


# -----------------------------------------------------------------------------
# -- Ventilation


def build_phx_ventilator(_hbeph_vent: ventilation.PhVentilationSystem) -> mech.PhxVentilator:
    """Returns a new Fresh-Air Ventilator built from the hb-energy hvac paramaters.

    This will look at the Space's Host-Room .properties.energy.hvac for data.

    Arguments:
    ----------
        *_hbeph_vent (ventilation.PhVentilationSystem): The HBE-PH Ventilation System
            to build the PHX-Ventilation from.

    Returns:
    --------
        * (mech_equip.Ventilator): The new Passive House Ventilator created.
    """

    phx_vent = mech.PhxVentilator()

    if not _hbeph_vent.ventilation_unit:
        return phx_vent
    phx_vent = _transfer_attributes(_hbeph_vent, phx_vent)
    phx_vent = _transfer_attributes(_hbeph_vent.ventilation_unit, phx_vent)

    phx_vent.display_name = 'Ventilator:'\
        f' {_hbeph_vent.ventilation_unit.sensible_heat_recovery*100 :0.0f}%-HR,'\
        f' {_hbeph_vent.ventilation_unit.latent_heat_recovery*100 :0.0f}%-MR'

    return phx_vent


def build_phx_ventilation_sys(_hbeph_vent: heating.PhHeatingSystem) -> mech.PhxMechanicalSubSystem:
    """Build a new PHX Ventilation Mechanical SubSystem.

    Arguments:
    ----------
        *_hbeph_vent (ventilation.PhVentilationSystem): The HBE-PH Ventilation System
            to build the PHX-Ventilation from.

    Returns:
    --------
        * (mech.PhxMechanicalSubSystem): A new mech subsystem with the heating device
            and distribution.
    """

    phx_vent_subsystem = mech.PhxMechanicalSubSystem()
    phx_vent_subsystem.device = build_phx_ventilator(_hbeph_vent)

    # TODO: Distribution...

    return phx_vent_subsystem


# -----------------------------------------------------------------------------
# -- Heating


def build_phx_heating_electric(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterElectric:
    phx_obj = mech.PhxHeaterElectric()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_fossil_boiler(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterBoiler:
    phx_obj = mech.PhxHeaterBoiler.fossil()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_wood_boiler(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterBoiler:
    phx_obj = mech.PhxHeaterBoiler.wood()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_district(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterDistrictHeat:
    phx_obj = mech.PhxHeaterDistrictHeat()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_hp_annual(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterHeatPump:
    phx_obj = mech.PhxHeaterHeatPump.annual()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_hp_monthly(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterHeatPump:
    phx_obj = mech.PhxHeaterHeatPump.monthly()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_hp_combined(_hbeph_heater: heating.PhHeatingSystem) -> mech.PhxHeaterHeatPump:
    phx_obj = mech.PhxHeaterHeatPump.combined()
    phx_obj = _transfer_attributes(_hbeph_heater, phx_obj)
    phx_obj.usage_profile.space_heating = True
    return phx_obj


def build_phx_heating_device(_htg_sys: heating.PhHeatingSystem) -> mech.PhxHeater:
    """Returns a new PHX-Heating-Device based on an input HBE-PH Heating System.

    Arguments:
    ----------
        * _htg_sys (heating.PhHeatingSystem): The HBE-PH Heating System to build 
            the new PHX Heating system from.

    Returns:
    --------
        * (mech.heating.PhxHeater): The new PHX Heating System created.
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

    # -- Get and build the right heater equipment type
    phx_heater = phx_heater_classes[_htg_sys.heating_type](_htg_sys)
    return phx_heater


def build_phx_heating_sys(_htg_sys: heating.PhHeatingSystem) -> mech.PhxMechanicalSubSystem:
    """

    Arguments:
    ----------
        * _htg_sys (heating.PhHeatingSystem): The HBE-PH Heating System to build 
            the new PHX Heating system from.

    Returns:
    --------
        * (mech.PhxMechanicalSubSystem): A new mech subsystem with the heating device
            and distribution.
    """
    phx_htg_subsystem = mech.PhxMechanicalSubSystem()
    phx_htg_subsystem.device = build_phx_heating_device(_htg_sys)

    # TODO: Distribution...

    return phx_htg_subsystem


# -----------------------------------------------------------------------------
# --- Cooling


def build_phx_cooling_ventilation(_hbeph_cooling: cooling.PhCoolingSystem) -> mech.PhxCoolingVentilation:
    phx_obj = mech.PhxCoolingVentilation()
    phx_obj = _transfer_attributes(_hbeph_cooling, phx_obj)
    phx_obj.usage_profile.cooling = True
    return phx_obj


def build_phx_cooling_recirculation(_hbeph_cooling: cooling.PhCoolingSystem) -> mech.PhxCoolingRecirculation:
    phx_obj = mech.PhxCoolingRecirculation()
    phx_obj = _transfer_attributes(_hbeph_cooling, phx_obj)
    phx_obj.usage_profile.cooling = True
    return phx_obj


def build_phx_cooling_dehumidification(_hbeph_cooling: cooling.PhCoolingSystem) -> mech.PhxCoolingDehumidification:
    phx_obj = mech.PhxCoolingDehumidification()
    phx_obj = _transfer_attributes(_hbeph_cooling, phx_obj)
    phx_obj.usage_profile.cooling = True
    return phx_obj


def build_phx_cooling_panel(_hbeph_cooling: cooling.PhCoolingSystem) -> mech.PhxCoolingPanel:
    phx_obj = mech.PhxCoolingPanel()
    phx_obj = _transfer_attributes(_hbeph_cooling, phx_obj)
    phx_obj.usage_profile.cooling = True
    return phx_obj


def build_phx_cooling_device(_clg_sys: cooling.PhCoolingSystem) -> mech.PhxHeater:
    """Returns a new PHX-Cooling-Device based on an input HBE-PH cooling System.

    Arguments:
    ----------
        * _clg_sys (cooling.PhCoolingSystem): The HBPH-Cooling-System to build 
            the new PHX-Cooling-System from.

    Returns:
    --------
        * (mech.cooling.PhxHeater): The new PHX cooling System created.
    """

    # -- Mapping HBEPH -> PHX types
    phx_cooling_classes = {
        'PhCoolingVentilation': build_phx_cooling_ventilation,
        'PhCoolingRecirculation': build_phx_cooling_recirculation,
        'PhCoolingDehumidification': build_phx_cooling_dehumidification,
        'PhCoolingPanel': build_phx_cooling_panel,
    }

    # -- Get and build the right heater equipment type
    phx_cooling = phx_cooling_classes[_clg_sys.cooling_class_name](_clg_sys)
    return phx_cooling


def build_phx_cooling_sys(_htg_sys: cooling.PhCoolingSystem) -> mech.PhxMechanicalSubSystem:
    """

    Arguments:
    ----------
        * _htg_sys (cooling.PhCoolingSystem): The HBE-PH cooling System to build 
            the new PHX cooling system from.

    Returns:
    --------
        * (mech.PhxMechanicalSubSystem): A new mech subsystem with the cooling device
            and distribution.
    """
    phx_htg_subsystem = mech.PhxMechanicalSubSystem()
    phx_htg_subsystem.device = build_phx_cooling_device(_htg_sys)

    # TODO: Distribution...

    return phx_htg_subsystem
