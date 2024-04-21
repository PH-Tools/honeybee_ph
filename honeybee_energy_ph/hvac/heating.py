# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-


"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


from honeybee_energy_ph.hvac import _base


class PhHeatingSystem(_base._PhHVACBase):
    message = "PhHeatingSystem is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatingDirectElectric(PhHeatingSystem):
    message = "PhHeatingDirectElectric is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatingFossilBoiler(PhHeatingSystem):
    message = "PhHeatingFossilBoiler is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatingWoodBoiler(PhHeatingSystem):
    message = "PhHeatingWoodBoiler is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatingDistrict(PhHeatingSystem):
    message = "PhHeatingDistrict is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatingSystemBuilder(object):
    message = "PhHeatingSystemBuilder is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
