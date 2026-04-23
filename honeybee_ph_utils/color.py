# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Basic A-RGB Color class."""

from copy import copy

try:
    from System import Drawing  # type: ignore
except ImportError:
    pass  # outside .NET

try:
    from typing import Dict, Optional
except ImportError:
    pass  # Python 2.7


class PhColor(object):
    """An ARGB color with integer channel values in the range 0-255.

    Attributes:
        a (int): Alpha channel (0 = fully transparent, 255 = fully opaque).
        r (int): Red channel.
        g (int): Green channel.
        b (int): Blue channel.
    """

    def __init__(self):
        self.a = 0
        self.r = 0
        self.g = 0
        self.b = 0

    @classmethod
    def from_argb(cls, a, r, g, b):
        # type: (int, int, int, int) -> PhColor
        """Create a PhColor from explicit alpha, red, green, and blue values.

        Arguments:
        ----------
            * a (int): Alpha channel value (clamped to 0-255).
            * r (int): Red channel value (clamped to 0-255).
            * g (int): Green channel value (clamped to 0-255).
            * b (int): Blue channel value (clamped to 0-255).

        Returns:
        --------
            * PhColor
        """
        new_color = cls()
        new_color.a = int(max(0, min(a, 255)))
        new_color.r = int(max(0, min(r, 255)))
        new_color.g = int(max(0, min(g, 255)))
        new_color.b = int(max(0, min(b, 255)))
        return new_color

    @classmethod
    def from_rgb(cls, r, g, b):
        # type: (int, int, int) -> PhColor
        """Create a fully opaque PhColor from red, green, and blue values.

        Arguments:
        ----------
            * r (int): Red channel value (clamped to 0-255).
            * g (int): Green channel value (clamped to 0-255).
            * b (int): Blue channel value (clamped to 0-255).

        Returns:
        --------
            * PhColor
        """
        return cls.from_argb(255, r, g, b)

    @classmethod
    def from_system_color(cls, color):
        # type: (Drawing.Color) -> PhColor
        """Create a PhColor from a .NET System.Drawing.Color.

        Arguments:
        ----------
            * color (System.Drawing.Color): The .NET color to convert.

        Returns:
        --------
            * PhColor
        """
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
        # type: () -> str
        return str(self)

    def __str__(self):
        # type: () -> str
        return "Color(a={}, r={}, g={}, b={})".format(self.a, self.r, self.g, self.b)

    def __eq__(self, other):
        # type: (PhColor) -> bool
        return self.a == other.a and self.r == other.r and self.g == other.g and self.b == other.b

    def ToString(self):
        # type: () -> str
        return str(self)

    def __copy__(self):
        # type: () -> PhColor
        new_obj = PhColor()
        new_obj.a = copy(self.a)
        new_obj.r = copy(self.r)
        new_obj.g = copy(self.g)
        new_obj.b = copy(self.b)
        return new_obj

    def duplicate(self):
        # type: () -> PhColor
        return self.__copy__()
