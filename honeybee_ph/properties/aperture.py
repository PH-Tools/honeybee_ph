# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Aperture Passive House (PH) Properties."""

try:
    from typing import Any
except ImportError:
    # IronPython
    pass


class AperturePhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.inset_dist = 0.1
        self.winter_shading_factor = 0.75
        self.summer_shading_factor = 0.75

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> AperturePhProperties
        _host = new_host or self._host
        new_properties_obj = AperturePhProperties(_host)
        new_properties_obj.id_num = self.id_num
        new_properties_obj.inset_dist = self.inset_dist
        new_properties_obj.winter_shading_factor = self.winter_shading_factor
        new_properties_obj.summer_shading_factor = self.summer_shading_factor

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Aperture Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        t = "AperturePhProperties" if not abridged else "AperturePhPropertiesAbridged"
        d.update({"type": t})
        d.update({"id_num": self.id_num})
        d.update({"inset_dist": self.inset_dist})
        d.update({"winter_shading_factor": self.winter_shading_factor})
        d.update({"summer_shading_factor": self.summer_shading_factor})

        return {"ph": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> AperturePhProperties
        assert data["type"] == "AperturePhProperties", "Expected AperturePhProperties. Got {}.".format(
            data["type"])

        new_prop = cls(host)
        new_prop.id_num = data["id_num"]
        new_prop.id_num = data["inset_dist"]
        new_prop.winter_shading_factor = data["winter_shading_factor"]
        new_prop.summer_shading_factor = data["summer_shading_factor"]

        return new_prop
