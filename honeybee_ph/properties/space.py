# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

try:
    from typing import TYPE_CHECKING, Any, Dict, Optional
except ImportError:
    TYPE_CHECKING = False
    pass  # Python 2.7

try:
    from ladybug_geometry import geometry3d
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee import properties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    if TYPE_CHECKING:
        from honeybee_ph import space
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))

"""
space.Space
  ├─ properties: SpaceProperties
      ├─ ph: SpacePhProperties
      ├─ energy: SpaceEnergyProperties
      ├─...
"""


class SpaceProperties(properties._Properties):
    """Honeybee-PH Space Properties.

    Space properties. This class will be extended by extensions.

    Usage:

    .. code-block:: python

        space = Space()
        space.properties -> SpaceProperties
        space.properties.ph -> SpacePhProperties
        space.properties.energy -> SpaceEnergyProperties
    """

    def __init__(self, host):
        # type: (Optional[space.Space]) -> None
        self._host = host

    @property
    def host(self):
        # type: () -> Optional[space.Space]
        return self._host

    @property
    def host_name(self):
        # type: () -> str
        if self.host:
            return self.host.display_name
        else:
            return "None"

    def to_dict(self, abridged=False, include=None):
        """Convert properties to dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
            include: A list of keys to be included in dictionary.
                If None all the available keys will be included.
        """
        d = {}
        if abridged == False:
            d["type"] = "SpaceProperties"
        else:
            d["type"] = "SpacePropertiesAbridged"
        d = self._add_extension_attr_to_dict(d, abridged, include)
        return d

    @classmethod
    def from_dict(cls, _dict={}, _host=None):
        # type: (Dict, Any) -> SpaceProperties
        assert _dict["type"] == "SpaceProperties", "Expected SpaceProperties. Got {}.".format(_dict["type"])
        obj = cls(_host)
        return obj

    def add_prefix(self, prefix):
        """Change the identifier extension attributes unique to this object by adding a prefix.

        Notably, this method only adds the prefix to extension attributes that must
        be unique to the Space (eg. single-room HVAC systems) and does not add the
        prefix to attributes that are shared across several Spaces (eg. ConstructionSets).

        Args:
            prefix: Text that will be inserted at the start of extension attribute identifiers.
        """
        self._add_prefix_extension_attr(prefix)

    def reset_to_default(self):
        """Reset the extension properties assigned at the level of this Room to default.

        This typically means erasing any ConstructionSets or ModifierSets assigned
        to this Space among other properties.
        """
        self._reset_extension_attr_to_default()

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Apply a scale transform to extension attributes.

        This is useful in cases where extension attributes possess geometric data
        that should be scaled alongside the host object. For example, dynamic
        geometry within the honeybee-radiance state of an aperture should be
        scaled if the host aperture is scaled.

        Arguments:
        ----------
            * factor (float): The scale factor
            * origin (Optional[geometry3d.Point3D]): default=None, A ladybug_geometry
                Point3D representing the origin from which to scale. If None,
                it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * None
        """
        for atr in self._extension_attributes:
            var = getattr(self, atr)
            if not hasattr(var, "scale"):
                continue
            try:
                var.scale(factor, origin)
            except Exception as e:
                import traceback

                traceback.print_exc()
                raise Exception("Failed to scale {}: {}".format(var, e))

    def __repr__(self):
        """Properties representation."""
        return "{}(host={})".format(self.__class__.__name__, self.host_name)


class SpacePhProperties(object):
    def __init__(self, _host):
        # type: (Optional[SpaceProperties]) -> None
        self._host = _host
        self.id_num = 0

        # TODO: Temporary override until I figure out right right way
        self._v_sup = None
        self._v_eta = None
        self._v_tran = None

    @property
    def host(self):
        # type: () -> Optional[SpaceProperties]
        return self._host

    @property
    def host_name(self):
        # type: () -> str
        if self.host:
            return self.host.host_name
        else:
            return "None"

    @property
    def has_ventilation_flow_rates(self):
        # type: () -> bool
        return any([self._v_sup, self._v_eta, self._v_tran])

    @property
    def honeybee_flow_rate(self):
        # type: () -> Optional[float]
        if not self.has_ventilation_flow_rates:
            return None
        return max([self._v_sup or 0, self._v_eta or 0, self._v_tran or 0])

    def duplicate(self, new_host=None):
        # type: (Any) -> SpacePhProperties
        _host = new_host or self._host
        new_properties_obj = SpacePhProperties(_host)

        new_properties_obj.id_num = self.id_num
        new_properties_obj._v_sup = self._v_sup
        new_properties_obj._v_eta = self._v_eta
        new_properties_obj._v_tran = self._v_tran

        return new_properties_obj

    def __str__(self):
        return "{}(host={}, v_eta={}, v_sup={}, v_tran={})".format(
            self.__class__.__name__,
            self.host_name,
            self._v_eta,
            self._v_sup,
            self._v_tran,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}

        if abridged:
            d["type"] = "SpacePhPropertiesAbridged"
        else:
            d["type"] = "SpacePhProperties"

        d["id_num"] = self.id_num
        d["_v_sup"] = self._v_sup
        d["_v_eta"] = self._v_eta
        d["_v_tran"] = self._v_tran

        return {"ph": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> SpacePhProperties
        assert "SpacePhProperties" in data["type"], "Expected SpacePhProperties. Got {}.".format(data["type"])
        new_prop = cls(host)

        new_prop.id_num = data["id_num"]
        new_prop._v_sup = data["_v_sup"]
        new_prop._v_eta = data["_v_eta"]
        new_prop._v_tran = data["_v_tran"]

        return new_prop


def get_ph_prop_from_space(_space):
    # type: (space.Space) -> SpacePhProperties
    """Get the space's PH-Properties."""
    return getattr(_space.properties, "ph")
