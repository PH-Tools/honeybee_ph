# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties class for PH-HVAC HeatCool Systems"""

try:
    from typing import Any
except:
    pass  # IronPython


class HeatCoolSystemPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(HeatCoolSystemPhProperties_FromDictError, self).__init__(self.msg)


class HeatCoolSystemPhProperties(object):
    """Honeybee-PH Properties for storing PH-style data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged:
            d["type"] = "HeatCoolSystemPhPropertiesAbridged"
        else:
            d["type"] = "HeatCoolSystemPhProperties"

        d["id_num"] = self.id_num
        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (dict, Any) -> HeatCoolSystemPhProperties
        valid_types = ("HeatCoolSystemPhProperties", "HeatCoolSystemPhPropertiesAbridged")
        if _input_dict["type"] not in valid_types:
            raise HeatCoolSystemPhProperties_FromDictError(
                valid_types, _input_dict["type"]
            )

        new_prop = cls(host)
        new_prop.id_num = _input_dict["id_num"]
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return "{}".format(self.__class__.__name__)
