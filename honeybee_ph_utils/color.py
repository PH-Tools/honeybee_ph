# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Basic A-RGB Color class."""

from copy import copy

try:
    from System import Drawing # type: ignore
except ImportError:
    pass # outside .NET

try:
    from typing import Dict, Optional
except ImportError:
    pass # Python 2.7


class PhColor(object):
    def __init__(self):
        self.a = 0
        self.r = 0
        self.g = 0
        self.b = 0
    
    @classmethod
    def from_argb(cls, a, r, g, b):
        # type: (int, int, int, int) -> PhColor
        new_color = cls()
        new_color.a = int(max(0, min(a, 255)))
        new_color.r = int(max(0, min(r, 255)))
        new_color.g = int(max(0, min(g, 255)))
        new_color.b = int(max(0, min(b, 255)))
        return new_color
    
    @classmethod
    def from_rgb(cls, r, g, b):
        #type: (int, int, int) -> PhColor
        return cls.from_argb(255, r, g, b)

    @classmethod
    def from_system_color(cls, color):
        #type: (Drawing.Color) -> PhColor
        new_color = cls()
        new_color.a = int(max(0, min(color.A, 255)))
        new_color.r = int(max(0, min(color.R, 255)))
        new_color.g = int(max(0, min(color.G, 255)))
        new_color.b = int(max(0, min(color.B, 255)))
        return new_color

    def to_dict(self):
        # type: () -> Dict[str, float]
        return {
            "a": self.a,
            "r": self.r,
            "g": self.g,
            "b": self.b,
        }
    
    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Optional[Dict[str, float]]) -> Optional[PhColor]
        if not _input_dict:
            return None

        new_color = cls()
        new_color.a = int(_input_dict["a"])
        new_color.r = int(_input_dict["r"])
        new_color.g = int(_input_dict["g"])
        new_color.b = int(_input_dict["b"])
        
        return new_color

    def __repr__(self):
        #type: () -> str
        return str(self)
    
    def __str__(self):
        #type: () -> str
        return "Color(a={}, r={}, g={}, b={})".format(self.a, self.r, self.g, self.b)
    
    def __eq__(self, other):
        # type: (PhColor) -> bool
        return self.a == other.a and self.r == other.r and self.g == other.g and self.b == other.b
    
    def ToString(self):
        #type: () -> str
        return str(self)
    
    def __copy__(self):
        #type: () -> PhColor
        new_obj = PhColor()
        new_obj.a = copy(self.a)
        new_obj.r = copy(self.r)
        new_obj.g = copy(self.g)
        new_obj.b = copy(self.b)
        return new_obj
    
    def duplicate(self):
        #type: () -> PhColor
        return self.__copy__()