# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.construction.opaque.OpaqueConstruction Objects"""

try:
    from typing import Any
except ImportError:
    pass  # Python 2.7

try:
    from honeybee_ph_utils import iso_6946
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_utils:\n\t{}".format(e))


class OpaqueConstructionPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(OpaqueConstructionPhProperties_FromDictError, self).__init__(self.msg)


class OpaqueConstructionPhProperties_NoHostError(Exception):
    def __init__(self, _property_name):
        self.msg = (
            "Error: Cannot calculate '{}' without a host OpaqueConstruction. The ISO 6946 limits "
            "are a property of the whole layer-stack.".format(_property_name)
        )
        super(OpaqueConstructionPhProperties_NoHostError, self).__init__(self.msg)


class OpaqueConstructionPhProperties(object):
    def __init__(self, _host=None):
        # type (Any) -> None
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def _get_host(self, _property_name):
        # type: (str) -> Any
        """Return the host OpaqueConstruction, or raise if there is none."""
        if self._host is None:
            raise OpaqueConstructionPhProperties_NoHostError(_property_name)
        return self._host

    def _get_host_materials(self, _property_name):
        # type: (str) -> Any
        """Return the host construction's materials, or raise if there is no host."""
        return self._get_host(_property_name).materials

    @property
    def r_value_upper_limit(self):
        # type: () -> float
        """The ISO 6946 UPPER-limit (parallel-path) R-value of the construction (m2k/W).

        Materials only: add Rsi/Rse for the exposure, or call `honeybee_ph_utils.iso_6946`
        directly to carry them inside each path as ISO 6946 6.7.1 does. Framing in different
        layers is read as staggered.
        """
        return iso_6946.get_r_value_upper_limit(self._get_host_materials("r_value_upper_limit"))

    @property
    def r_value_lower_limit(self):
        # type: () -> float
        """The ISO 6946 LOWER-limit (isothermal-planes) R-value of the construction (m2k/W).

        Materials only. This is the value a consumer gets by reading each hybrid layer's
        equivalent conductivity and summing the layers, and it is the pessimistic bound.
        """
        return iso_6946.get_r_value_lower_limit(self._get_host_materials("r_value_lower_limit"))

    @property
    def r_value_mean_of_limits(self):
        # type: () -> float
        """The ISO 6946 mean-of-limits R-value of the construction (m2k/W).

        Materials only. This is the reading designPH and PHPP report for a construction with framed layers.
        """
        return iso_6946.get_r_value_mean_of_limits(self._get_host_materials("r_value_mean_of_limits"))

    @property
    def u_value_mean_of_limits(self):
        # type: () -> float
        """The ISO 6946 mean-of-limits U-value of the construction (W/m2k).

        Materials only (no air films), matching honeybee's 'u_value' convention.
        """
        r_value = self.r_value_mean_of_limits
        if r_value <= 0:
            return 0.0
        return 1.0 / r_value

    @property
    def iso_6946_error_percent(self):
        # type: () -> float
        """The spread between the two ISO 6946 limits, as the percentage designPH prints.

        Zero for a construction with no thermally inhomogeneous layers.
        """
        return iso_6946.get_error_percent(self._get_host_materials("iso_6946_error_percent"))

    @property
    def equivalent_conductivity_mean_of_limits(self):
        # type: () -> float
        """The conductivity (W/mk) of a single layer which carries the whole construction.

        The construction's own total thickness at the mean-of-limits R-value. Used to push a
        construction into a tool which cannot hold the real layers (designPH beyond three paths).
        """
        host = self._get_host("equivalent_conductivity_mean_of_limits")
        return iso_6946.get_equivalent_conductivity(self.r_value_mean_of_limits, host.thickness)

    def duplicate(self, new_host=None):
        # type: (Any) -> OpaqueConstructionPhProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Any) -> OpaqueConstructionPhProperties
        host = new_host or self.host

        new_obj = self.__class__(host)
        new_obj.id_num = self.id_num
        return new_obj

    def to_dict(self, abridged=False):
        # type: (bool) -> dict
        d = {}

        if abridged:
            d["type"] = "OpaqueConstructionPhPropertiesAbridged"
        else:
            d["type"] = "OpaqueConstructionPhProperties"

        d["id_num"] = self.id_num
        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (dict, Any) -> OpaqueConstructionPhProperties
        valid_types = (
            "OpaqueConstructionPhProperties",
            "OpaqueConstructionPhPropertiesAbridged",
        )
        if _input_dict["type"] not in valid_types:
            raise OpaqueConstructionPhProperties_FromDictError(valid_types, _input_dict["type"])

        new_obj = cls(host)
        new_obj.id_num = _input_dict["id_num"]
        return new_obj

    def __str__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
