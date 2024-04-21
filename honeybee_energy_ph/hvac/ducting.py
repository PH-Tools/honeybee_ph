# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-


"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


from honeybee_energy_ph.hvac import _base


class PhDuctSegment(_base._PhHVACBase):
    message = "PhDuctSegment is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)


class PhDuctElement(_base._PhHVACBase):
    message = "PhDuctElement is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
