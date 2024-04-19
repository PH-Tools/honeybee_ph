# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


from honeybee_energy_ph.hvac import _base
from honeybee_ph_utils import enumerables


class PhPipeDiameter(enumerables.CustomEnum):
    message = "PhPipeDiameter is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhPipeMaterial(enumerables.CustomEnum):
    message = "PhPipeMaterial is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhPipeSegment(_base._PhHVACBase):
    message = "PhPipeSegment is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhPipeElement(_base._PhHVACBase):
    message = "PhPipeElement is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhPipeBranch(_base._PhHVACBase):
    message = "PhPipeBranch is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhPipeTrunk(_base._PhHVACBase):
    message = "PhPipeTrunk is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWTankType(enumerables.CustomEnum):
    message = "PhSHWTankType is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWTank(_base._PhHVACBase):
    message = "PhSHWTank is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHotWaterHeater(_base._PhHVACBase):
    message = "PhHotWaterHeater is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWHeaterElectric(PhHotWaterHeater):
    message = "PhSHWHeaterElectric is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWHeaterBoiler(PhHotWaterHeater):
    message = "PhSHWHeaterBoiler is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWHeaterBoilerWood(PhHotWaterHeater):
    message = "PhSHWHeaterBoilerWood is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWHeaterDistrict(PhHotWaterHeater):
    message = "PhSHWHeaterDistrict is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWHeaterHeatPump(PhHotWaterHeater):
    message = "PhSHWHeaterHeatPump is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhSHWHeaterBuilder(object):
    message = "PhSHWHeaterBuilder is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
