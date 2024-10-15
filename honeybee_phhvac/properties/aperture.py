# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-PH-HVAC Aperture Properties."""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # Python 2.7

try:
    from honeybee.properties import ApertureProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))


class AperturePhHvacProperties(object):
    def __init__(self, _host):
        # type: (Optional[ApertureProperties]) -> None
        self._host = _host

    @property
    def host(self):
        # type: () -> Optional[ApertureProperties]
        return self._host

    def __copy__(self, new_host=None):
        # type: (Optional[ApertureProperties]) -> AperturePhHvacProperties
        _host = new_host or self._host
        new_properties_obj = AperturePhHvacProperties(_host)
        return new_properties_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> AperturePhHvacProperties
        return self.__copy__(new_host=new_host)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged == False:
            d["type"] = "AperturePhHvacProperties"
        else:
            d["type"] = "AperturePhHvacPropertiesAbridged"
        return {"ph_hvac": d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict[str, Any], Any) -> AperturePhHvacProperties
        if _dict["type"] not in ("AperturePhHvacProperties", "AperturePhHvacPropertiesAbridged"):
            raise ValueError(
                "Expected AperturePhHvacProperties or AperturePhHvacPropertiesAbridged. Got {}.".format(_dict["type"])
            )
        new_prop = cls(host)
        return new_prop

    def apply_properties_from_dict(self, data):
        # type: (Dict[str, Any]) -> None
        return None
