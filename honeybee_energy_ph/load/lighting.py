# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing Honeybee-Energy | Load | Lighting"""

try:
    from typing import Any
except ImportError:
    # Python 2.7
    pass

from honeybee.properties import _Properties
from honeybee_energy.load.lighting import Lighting


class LightingPhProperties(object):
    """PH Properties Object for LBT Point3D Objects"""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    def duplicate(self, new_host=None):
        # type: (LightingPhProperties, Any) -> LightingPhProperties
        _host = new_host or self._host
        new_properties_obj = self.__class__(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "LBT-Point3D Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (LightingPhProperties, bool) -> dict[str, dict]
        base = {"_PH": {}}
        base["_PH"]["type"] = "LightingPhProperties" if not abridged else "LightingPhPropertiesAbridged"

        return base

    @classmethod
    def from_dict(cls, data, host):
        # type: (LightingPhProperties, dict, Any) -> LightingPhProperties
        assert data["type"] == "LightingPhProperties", "Expected LightingPhProperties. Got {}.".format(
            data["type"])

        new_prop = cls(host)
        new_prop.id_num = data.get("id_num", 0)

        return new_prop


class LightingProperties(_Properties):
    """Properties for HBE Lighting Objects"""

    def __repr__(self):
        return "LightingProperties: {!r}".format(self.host)

    def to_dict(self, abridged=False):
        # type: (LightingProperties, bool) -> LightingProperties
        """Convert properties to dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
        """
        base = {'type': 'LightingProperties'} if not abridged else \
            {'type': 'LightingPropertiesAbridged'}

        return base


class PH_Lighting(Lighting):
    __slots__ = ("_properties",)

    def __init__(self, *args, **kwargs):
        super(PH_Lighting, self).__init__(*args, **kwargs)
        self._properties = LightingProperties(self)

    @property
    def properties(self):
        return self._properties

    @classmethod
    def from_hb_lighting(cls, _hb_lighting):
        # type: (PH_Lighting, Lighting) -> PH_Lighting
        new_ph_obj = cls(
            identifier=_hb_lighting.identifier,
            watts_per_area=_hb_lighting.watts_per_area,
            schedule=_hb_lighting.schedule,
            return_air_fraction=_hb_lighting.return_air_fraction,
            radiant_fraction=_hb_lighting.radiant_fraction,
            visible_fraction=_hb_lighting.visible_fraction,
        )

        return new_ph_obj

    def __setattr__(self, attr_name, value):
        # type: (PH_Lighting, str, Any) -> None
        """Override in order to intercept any attribute setting on the 
        base LBT object. Use the following syntax to catch any calls and 
        pass them to the PH .properties as approprate. Be sure to include the 
        super() at the end to also set the attr on the base LBT object.

        > if attr_name == "watts_per_area":
        >    self._properties.ph.watts_per_area = value
        >    ...
        > super(PH_Lighting, self).__setattr__(attr_name, value)
        """

        super(PH_Lighting, self).__setattr__(attr_name, value)
        return None

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

    def __copy__(self):
        # type: (PH_Lighting) -> PH_Lighting
        new_hb_obj = super(PH_Lighting, self).__copy__()
        new_ph_obj = PH_Lighting.from_hb_lighting(new_hb_obj)
        new_ph_obj._properties = self._properties
        return new_ph_obj

    def to_dict(self, abridged=False):
        # type: (PH_Lighting, bool) -> dict
        base = super(PH_Lighting, self).to_dict(abridged=abridged)
        base.update({"_properties": self.properties.to_dict(abridged)})
        return base
