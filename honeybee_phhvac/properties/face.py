# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-PH-HVAC Face Properties."""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # Python 2.7

try:
    from honeybee.properties import FaceProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))


class FacePhHvacProperties(object):
    def __init__(self, _host):
        # type: (Optional[FaceProperties]) -> None
        self._host = _host

    @property
    def host(self):
        # type: () -> Optional[FaceProperties]
        return self._host

    def __copy__(self, new_host=None):
        # type: (Optional[FaceProperties]) -> FacePhHvacProperties
        _host = new_host or self._host
        new_properties_obj = FacePhHvacProperties(_host)
        return new_properties_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> FacePhHvacProperties
        return self.__copy__(new_host=new_host)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged == False:
            d["type"] = "FacePhHvacPropertiesAbridged"
        else:
            d["type"] = "FacePhHvacProperties"
        return {"ph_hvac": d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict[str, Any], Any) -> FacePhHvacProperties
        assert _dict["type"] == "FacePhHvacProperties", "Expected FacePhHvacProperties. Got {}.".format(_dict["type"])
        new_prop = cls(host)
        return new_prop

    def apply_properties_from_dict(self, data):
        # type: (Dict[str, Any]) -> None
        return None
