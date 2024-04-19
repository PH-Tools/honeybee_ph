# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-


"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


from honeybee_energy_ph.hvac import _base


class PhRenewableEnergyDevice(_base._PhHVACBase):
    message = "PhRenewableEnergyDevice is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhPhotovoltaicDevice(PhRenewableEnergyDevice):
    message = "PhPhotovoltaicDevice is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhRenewableEnergyDeviceBuilder(object):
    message = "PhRenewableEnergyDeviceBuilder is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
