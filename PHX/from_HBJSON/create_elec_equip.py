# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create new PhxElectricalDevices from HBPH-PhEquipment"""

from honeybee_energy_ph.load import ph_equipment
from PHX.model import elec_equip


def build_phx_elec_device(_hbph_device: ph_equipment.PhEquipment) -> elec_equip.PhxElectricalDevice:
    """Returns a new PhxElectricalDevice based on the HBPH-PhEquipment input.

    Arguments:
    ----------
        * _hbph_device (ph_equipment.PhEquipment): The HBPH-PhEquipment
            to use as the source for the new PhxElectricalDevice.

    Returns:
    --------
        * elec_equip.PhxElectricalEquipment: The new PhxElectricalDevice.
    """
    # -- Get the right PHX Device constructor based on the type of HBPH Equipment input
    devices = {
        'PhDishwasher': elec_equip.PhxDeviceDishwasher,
        'PhClothesWasher': elec_equip.PhxDeviceClothesWasher,
        'PhClothesDryer': elec_equip.PhxDeviceClothesDryer,
        'PhRefrigerator': elec_equip.PhxDeviceRefrigerator,
        'PhFreezer': elec_equip.PhxDeviceFreezer,
        'PhFridgeFreezer': elec_equip.PhxDeviceFridgeFreezer,
        'PhCooktop': elec_equip.PhxDeviceCooktop,
        'PhPhiusMEL': elec_equip.PhxDeviceMEL,
        'PhPhiusLightingInterior': elec_equip.PhxDeviceLightingInterior,
        'PhPhiusLightingExterior': elec_equip.PhxDeviceLightingExterior,
        'PhPhiusLightingGarage': elec_equip.PhxDeviceLightingGarage,
        'PhCustomAnnualElectric': elec_equip.PhxDeviceCustomElec,
        'PhCustomAnnualLighting': elec_equip.PhxDeviceCustomLighting,
        'PhCustomAnnualMEL': elec_equip.PhxDeviceCustomMEL,
    }

    # -- Build the basic device
    device_class = devices[_hbph_device.__class__.__name__]
    phx_device = device_class()

    # -- Pull out all the PH attributes and set the PHX ones to match.
    for attr_name in vars(_hbph_device).keys():
        try:
            if attr_name.startswith('_'):
                attr_name = attr_name[1:]
            setattr(phx_device, attr_name, getattr(_hbph_device, attr_name))
        except KeyError:
            pass

    return phx_device
