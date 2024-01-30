# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties for Honeybee-Energy-PH | Load | Lighting"""

try:
    from typing import Any
except ImportError:
    # Python 2.7
    pass


class LightingPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(LightingPhProperties_FromDictError, self).__init__(self.msg)


class LightingPhProperties(object):
    """Ph Properties for Honeybee-Energy Lighting"""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.target_lux = 300
        self.target_lux_height = 0.8  # m

    def duplicate(self, new_host=None):
        # type: (Any) -> LightingPhProperties
        _host = new_host or self._host

        new_prop_obj = self.__class__(_host)
        new_prop_obj.id_num = self.id_num
        new_prop_obj.target_lux = self.target_lux
        new_prop_obj.target_lux_height = self.target_lux_height

        return new_prop_obj

    @property
    def host(self):
        return self._host

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}

        if abridged:
            d["type"] = "LightingPhPropertiesAbridged"
        else:
            d["type"] = "LightingPhProperties"

        d["id_num"] = self.id_num
        d["target_lux"] = self.target_lux
        d["target_lux_height"] = self.target_lux_height

        return {"ph": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> LightingPhProperties
        valid_types = ("LightingPhProperties", "LightingPhPropertiesAbridged")
        if data["type"] not in valid_types:
            raise LightingPhProperties_FromDictError(valid_types, data["type"])

        new_prop = cls(host)
        new_prop.id_num = data["id_num"]
        new_prop.target_lux = data["target_lux"]
        new_prop.target_lux_height = data["target_lux_height"]

        return new_prop
