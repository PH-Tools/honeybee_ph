from honeybee_energy_ph.load import ph_equipment
from PHX.model import elec_equip


def build_phx_elec_device(_hbph_device: ph_equipment.PhEquipment) -> elec_equip.PhxElectricalEquipment:
    """Returns a new PHX Elec-Equipment Device based on the HBPH Elec Equipment input.

    Arguments:
    ----------
        * _hbph_device (ph_equipment.PhEquipment): The HBPH-Elec Equipment Device
            to use as the source for the PHX-Elec Equipment Device.

    Returns:
    --------
        * elec_equip.PhxElectricalEquipment: The new PHX-Elec Equipment Device.
    """
    # -- Get the right constructor based on the type of heater
    devices = {
        'PhDishwasher': elec_equip.PhxDishwasher,
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
