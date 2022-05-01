# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Valid 'types' for Mech Equipment Options."""

from enum import Enum


class ComponentExposureExterior(Enum):
    EXTERIOR = -1
    GROUND = -2
    SURFACE = -3


class ComponentFaceType(Enum):
    OPAQUE = 1
    TRANSPARENT = 2
    AIRBOUNDARY = 3


class ComponentColor(Enum):
    EXT_WALL_INNER = 1
    EXT_WALL_OUTER = 2
    INNER_WALL = 3
    WINDOW = 4
    FLOOR = 5
    CEILING = 6
    SLOPED_ROOF_OUTER = 7
    SLOPED_ROOF_INNER = 8
    SLOPED_ROOF_THATCH = 9  # WTF?
    FLAT_ROOF_OUTER = 10
    FLAT_ROOF_INNER = 11
    SURFACE_GROUND_CONTACT = 12
    GROUND_ABOVE = 13
    GROUND_BENEATH = 14
