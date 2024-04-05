# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.construction.window.WindowConstruction Objects"""

try:
    from typing import Any, Optional
except ImportError:
    pass  # Python 2.7

from honeybee_energy_ph.construction import window


class WindowConstructionPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(WindowConstructionPhProperties_FromDictError, self).__init__(self.msg)


class WindowConstructionPhProperties(object):
    def __init__(self, _host):
        # type: (Any) -> None
        self._host = _host
        self.id_num = 0
        self.ph_frame = None  # type: Optional[window.PhWindowFrame]
        self.ph_glazing = None  # type: Optional[window.PhWindowGlazing]

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> WindowConstructionPhProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Any) -> WindowConstructionPhProperties
        host = new_host or self.host

        new_obj = self.__class__(host)
        new_obj.id_num = self.id_num
        if self.ph_frame:
            new_obj.ph_frame = self.ph_frame.duplicate()
        if self.ph_glazing:
            new_obj.ph_glazing = self.ph_glazing.duplicate()

        return new_obj

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}

        if abridged:
            d["type"] = "WindowConstructionPhPropertiesAbridged"
        else:
            d["type"] = "WindowConstructionPhProperties"

        d["id_num"] = self.id_num
        if self.ph_frame:
            d["ph_frame"] = self.ph_frame.to_dict()
        if self.ph_glazing:
            d["ph_glazing"] = self.ph_glazing.to_dict()
        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (dict[str, Any], Any) -> WindowConstructionPhProperties
        valid_types = (
            "WindowConstructionPhProperties",
            "WindowConstructionPhPropertiesAbridged",
        )
        if _input_dict["type"] not in valid_types:
            raise WindowConstructionPhProperties_FromDictError(valid_types, _input_dict["type"])

        new_obj = cls(host)
        new_obj.id_num = _input_dict["id_num"]
        if "ph_frame" in _input_dict:
            new_obj.ph_frame = window.PhWindowFrame.from_dict(_input_dict["ph_frame"])
        if "ph_glazing" in _input_dict:
            new_obj.ph_glazing = window.PhWindowGlazing.from_dict(_input_dict["ph_glazing"])
        return new_obj

    def __str__(self):
        return "{}(frame={!r}, glazing={!r})".format(self.__class__.__name__, self.ph_frame, self.ph_glazing)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
