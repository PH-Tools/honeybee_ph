# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH Properties classes for Space objects."""

try:
    from typing import Any, Optional
except:
    pass  # IronPython

from honeybee import properties


class SpaceEnergyProperties(properties._Properties):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False, include=None):
        # type: (bool, Optional[list]) -> dict[str, Any]
        """Convert properties to dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
            include: A list of keys to be included in dictionary.
                If None all the available keys will be included.
        """
        d = {}

        if abridged:
            d["type"] = "SpaceEnergyPropertiesAbridged"
        else:
            d["type"] = "SpaceEnergyProperties"

        d["id_num"] = self.id_num

        return {"energy": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> SpaceEnergyProperties
        assert "SpaceEnergyProperties" in _input_dict["type"], "Expected SpaceEnergyProperties. Got {}.".format(
            _input_dict["type"]
        )

        new_prop = cls(_host)
        new_prop.id_num = _input_dict.get("id_num", 0)

        return new_prop

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
