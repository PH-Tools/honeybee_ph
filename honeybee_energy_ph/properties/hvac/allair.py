# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""DEPRECATED in favor of the new 'honeybee_phhvac' module."""


class AllAirSystemPhProperties(object):
    message = "AllAirSystemPhProperties is deprecated, use 'honeybee_phhvac' instead"

    def __init__(self, *args, **kwargs):
        raise Exception(self.message)
