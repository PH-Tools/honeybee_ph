# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Aperture Passive House (PH) Properties."""


try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_energy_ph.construction.window import PhApertureInstallType
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph:\n\t{}".format(e))


class AperturePsiInstalls(object):
    """Per-edge Psi-Install 'Install Type' assignments for a single Aperture.

    Each side (top / right / bottom / left, matching PhWindowFrame element order)
    optionally holds a PhApertureInstallType. A side left as None inherits the
    psi-install value from the Aperture construction's frame element for that side.
    """

    SIDES = ("top", "right", "bottom", "left")

    def __init__(self):
        self.top = None  # type: Optional[PhApertureInstallType]
        self.right = None  # type: Optional[PhApertureInstallType]
        self.bottom = None  # type: Optional[PhApertureInstallType]
        self.left = None  # type: Optional[PhApertureInstallType]

    @property
    def any_assigned(self):
        # type: () -> bool
        """Return True if any side has an Install Type assigned."""
        return any(getattr(self, side) is not None for side in self.SIDES)

    def get_side(self, _side):
        # type: (str) -> Optional[PhApertureInstallType]
        """Return the Install Type assigned to a side ('top' | 'right' | 'bottom' | 'left'), or None."""
        if _side not in self.SIDES:
            raise ValueError("Side must be one of {}. Got: '{}'".format(self.SIDES, _side))
        return getattr(self, _side)

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        for side in self.SIDES:
            install_type = getattr(self, side)
            if install_type is not None:
                d[side] = install_type.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> AperturePsiInstalls
        new_obj = cls()
        for side in cls.SIDES:
            install_type_dict = _input_dict.get(side, None)
            if install_type_dict:
                setattr(new_obj, side, PhApertureInstallType.from_dict(install_type_dict))
        return new_obj

    def duplicate(self):
        # type: () -> AperturePsiInstalls
        return self.__copy__()

    def __copy__(self):
        # type: () -> AperturePsiInstalls
        new_obj = self.__class__()
        for side in self.SIDES:
            install_type = getattr(self, side)
            if install_type is not None:
                setattr(new_obj, side, install_type.duplicate())
        return new_obj

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={!r}".format(side, getattr(self, side)) for side in self.SIDES),
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class ShadingDimensions(object):
    """PHPP Style shading dimension info"""

    def __init__(self):
        # Horizon Shading
        self.h_hori = None  # type: Optional[float]
        self.d_hori = None  # type: Optional[float]

        # Side Reveal
        self.o_reveal = None  # type: Optional[float]
        self.d_reveal = None  # type: Optional[float]

        # Overhangs
        self.o_over = None  # type: Optional[float]
        self.d_over = None  # type: Optional[float]

    def __copy__(self, new_host=None):
        # type: (Any) -> ShadingDimensions

        new_obj = ShadingDimensions()

        new_obj.d_hori = self.d_hori
        new_obj.h_hori = self.h_hori
        new_obj.d_reveal = self.d_reveal
        new_obj.o_reveal = self.o_reveal
        new_obj.d_over = self.d_over
        new_obj.o_over = self.o_over

        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> ShadingDimensions
        return self.__copy__(new_host=new_host)

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["d_hori"] = self.d_hori
        d["h_hori"] = self.h_hori
        d["d_reveal"] = self.d_reveal
        d["o_reveal"] = self.o_reveal
        d["d_over"] = self.d_over
        d["o_over"] = self.o_over

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> ShadingDimensions
        new_obj = cls()

        new_obj.d_hori = _input_dict["d_hori"]
        new_obj.h_hori = _input_dict["h_hori"]
        new_obj.d_reveal = _input_dict["d_reveal"]
        new_obj.o_reveal = _input_dict["o_reveal"]
        new_obj.d_over = _input_dict["d_over"]
        new_obj.o_over = _input_dict["o_over"]

        return new_obj


class AperturePhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.winter_shading_factor = 0.75
        self.summer_shading_factor = 0.75
        self.shading_dimensions = None  # type: Optional[ShadingDimensions]
        self.variant_type = "_unnamed_type_"
        self.install_depth = 0.1016  # m
        self.default_monthly_shading_correction_factor = 1.0
        self.install_types = AperturePsiInstalls()

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> AperturePhProperties
        _host = new_host or self._host
        new_properties_obj = AperturePhProperties(_host)
        new_properties_obj.id_num = self.id_num

        new_properties_obj.winter_shading_factor = self.winter_shading_factor
        new_properties_obj.summer_shading_factor = self.summer_shading_factor
        if self.shading_dimensions:
            new_properties_obj.shading_dimensions = self.shading_dimensions.duplicate(self)
        new_properties_obj.variant_type = self.variant_type
        new_properties_obj.install_depth = self.install_depth
        new_properties_obj.default_monthly_shading_correction_factor = self.default_monthly_shading_correction_factor
        new_properties_obj.install_types = self.install_types.duplicate()

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Aperture Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Dict[str, Any]]
        d = {}
        d["type"] = "AperturePhProperties" if not abridged else "AperturePhPropertiesAbridged"
        d["id_num"] = self.id_num
        d["winter_shading_factor"] = self.winter_shading_factor
        d["summer_shading_factor"] = self.summer_shading_factor
        if self.shading_dimensions:
            d["shading_dims"] = self.shading_dimensions.to_dict()
        d["variant_type"] = self.variant_type
        d["install_depth"] = self.install_depth
        d["default_monthly_shading_correction_factor"] = self.default_monthly_shading_correction_factor
        if self.install_types.any_assigned:
            d["install_types"] = self.install_types.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], Any) -> AperturePhProperties
        assert _input_dict["type"] == "AperturePhProperties", "Expected AperturePhProperties. Got {}.".format(
            _input_dict["type"]
        )

        new_prop = cls(host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop.winter_shading_factor = _input_dict["winter_shading_factor"]
        new_prop.summer_shading_factor = _input_dict["summer_shading_factor"]
        new_prop.variant_type = _input_dict["variant_type"]

        # Use get to ensure backwards compatibility for now
        new_prop.install_depth = _input_dict.get("install_depth", new_prop.install_depth)

        shading_dim_dict = _input_dict.get("shading_dims", None)
        if shading_dim_dict:
            new_prop.shading_dimensions = ShadingDimensions.from_dict(shading_dim_dict)

        new_prop.default_monthly_shading_correction_factor = _input_dict.get(
            "default_monthly_shading_correction_factor", 1.0
        )

        # Use get to ensure backwards compatibility: older HBJSON has no install_types
        install_types_dict = _input_dict.get("install_types", None)
        if install_types_dict:
            new_prop.install_types = AperturePsiInstalls.from_dict(install_types_dict)

        return new_prop

    def apply_properties_from_dict(self, _aperture_prop_dict):
        # type: (Dict[str, Any]) -> None
        """Apply properties from an AperturePhPropertiesAbridged dictionary.

        Arguments:
        ----------
            * _aperture_prop_dict (dict): An AperturePhPropertiesAbridged dictionary loaded from
                the Aperture object itself. Unabridged.
        """

        self.winter_shading_factor = _aperture_prop_dict["winter_shading_factor"]
        self.summer_shading_factor = _aperture_prop_dict["summer_shading_factor"]
        self.variant_type = _aperture_prop_dict["variant_type"]

        # Use get to ensure backwards compatibility for now
        self.install_depth = _aperture_prop_dict.get("install_depth", 0.1016)  # default = 4in.

        shading_dim_dict = _aperture_prop_dict.get("shading_dims", None)
        if shading_dim_dict:
            self.shading_dimensions = ShadingDimensions.from_dict(shading_dim_dict)

        self.default_monthly_shading_correction_factor = _aperture_prop_dict.get(
            "default_monthly_shading_correction_factor", 1.0
        )

        # Use get to ensure backwards compatibility: older HBJSON has no install_types
        install_types_dict = _aperture_prop_dict.get("install_types", None)
        if install_types_dict:
            self.install_types = AperturePsiInstalls.from_dict(install_types_dict)

        return None
