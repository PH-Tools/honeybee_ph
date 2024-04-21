# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-Energy-PH Properties Extension for ServiceHotWater (Program) objects."""

try:
    from typing import Any, Optional
except:
    pass  # IronPython

try:
    from honeybee_energy.properties.extension import ServiceHotWaterProperties
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy.", e)


class ServiceHotWaterPhProperties(object):
    """Honeybee-PH Properties for logging PH-style data."""

    def __init__(self, _host):
        # type: (Optional[ServiceHotWaterProperties]) -> None
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        # type: () -> Optional[ServiceHotWaterProperties]
        return self._host

    def to_dict(self, abridged=False, include=None):
        # type: (bool, Optional[list]) -> dict[str, Any]

        return {}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Optional[ServiceHotWaterProperties]) -> ServiceHotWaterPhProperties
        new_prop = cls(_host)

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        # type: (Any) -> None
        return

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        """Properties representation."""
        return "{}".format(self.__class__.__name__)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()
