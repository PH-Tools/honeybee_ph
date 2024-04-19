# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-


"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


from honeybee_energy_ph.hvac import _base


class PhHeatPumpSystem(_base._PhHVACBase):
    message = "PhHeatPumpSystem is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCoolingParams_Base(_base._PhHVACBase):
    message = "PhHeatPumpCoolingParams_Base is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCoolingParams_Ventilation(PhHeatPumpCoolingParams_Base):
    message = "PhHeatPumpCoolingParams_Ventilation is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCoolingParams_Recirculation(PhHeatPumpCoolingParams_Base):
    message = "PhHeatPumpCoolingParams_Recirculation is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCoolingParams_Dehumidification(PhHeatPumpCoolingParams_Base):
    message = "PhHeatPumpCoolingParams_Dehumidification is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCoolingParams_Panel(PhHeatPumpCoolingParams_Base):
    message = "PhHeatPumpCoolingParams_Panel is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCoolingParams:
    message = "PhHeatPumpCoolingParams is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpAnnual(PhHeatPumpSystem):
    message = "PhHeatPumpAnnual is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpRatedMonthly(PhHeatPumpSystem):
    message = "PhHeatPumpRatedMonthly is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpCombined(PhHeatPumpSystem):
    message = "PhHeatPumpCombined is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhHeatPumpSystemBuilder(object):
    message = "PhHeatPumpSystemBuilder is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
