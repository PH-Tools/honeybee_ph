# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.construction.window.WindowConstruction Objects"""


class WindowConstructionPhProperties:
    def __init__(self):
        self.id_num = 0

    def __repr__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)
