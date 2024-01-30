# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Shade Passive House (PH) Properties."""
try:
    from typing import Any
except ImportError:
    pass  # Python 2.7


class ShadePhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> ShadePhProperties
        _host = new_host or self._host
        new_properties_obj = ShadePhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "Shade Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        t = "ShadePhProperties" if not abridged else "ShadePhPropertiesAbridged"
        d.update({"type": t})
        d.update({"id_num": self.id_num})

        return {"ph": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> ShadePhProperties
        assert (
            data["type"] == "ShadePhProperties"
        ), "Expected ShadePhProperties. Got {}.".format(data["type"])

        new_prop = cls(host)
        new_prop.id_num = data.get("id_num", 0)

        return new_prop
