# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-


"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


from honeybee_energy_ph.hvac import _base


class Ventilator(_base._PhHVACBase):
    message = "Ventilator is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhVentilationSystem(_base._PhHVACBase):
    message = "PhVentilationSystem is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class _ExhaustVentilatorBase(_base._PhHVACBase):
    message = "_ExhaustVentilatorBase is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class ExhaustVentDryer(_ExhaustVentilatorBase):
    message = "ExhaustVentDryer is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class ExhaustVentKitchenHood(_ExhaustVentilatorBase):
    message = "ExhaustVentKitchenHood is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class ExhaustVentUserDefined(_ExhaustVentilatorBase):
    message = "ExhaustVentUserDefined is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhExhaustDeviceBuilder(object):
    message = "PhExhaustDeviceBuilder is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
