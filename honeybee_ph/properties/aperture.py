# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Aperture Passive House (PH) Properties."""


try:
    from typing import Any, Dict, Optional
except ImportError:
    pass # IronPython 2.7


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

    def duplicate(self, new_host):
        # type: (Any) -> ShadingDimensions

        new_obj = ShadingDimensions()

        new_obj.d_hori = self.d_hori
        new_obj.h_hori = self.h_hori
        new_obj.d_reveal = self.d_reveal
        new_obj.o_reveal = self.o_reveal
        new_obj.d_over = self.d_over
        new_obj.o_over = self.o_over

        return new_obj

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
        self.variant_type = '_unnamed_type_'
        self.install_depth = 0.1016 #m

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
            new_properties_obj.shading_dimensions = self.shading_dimensions.duplicate(
                self)
        new_properties_obj.variant_type = self.variant_type
        new_properties_obj.install_depth = self.install_depth

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Aperture Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, dict]
        d = {}
        d["type"] = "AperturePhProperties" if not abridged else "AperturePhPropertiesAbridged"
        d["id_num"] = self.id_num
        d["winter_shading_factor"] = self.winter_shading_factor
        d["summer_shading_factor"] = self.summer_shading_factor
        if self.shading_dimensions:
            d['shading_dims'] = self.shading_dimensions.to_dict()
        d["variant_type"] = self.variant_type
        d["install_depth"] = self.install_depth

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict, Any) -> AperturePhProperties
        assert _input_dict["type"] == "AperturePhProperties", "Expected AperturePhProperties. Got {}.".format(
            _input_dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop.winter_shading_factor = _input_dict["winter_shading_factor"]
        new_prop.summer_shading_factor = _input_dict["summer_shading_factor"]
        new_prop.variant_type = _input_dict["variant_type"]
        
        # Use get to ensure backwards compatibility for now
        new_prop.install_depth = _input_dict.get("install_depth", 0.1)

        shading_dim_dict = _input_dict.get("shading_dims", None)
        if shading_dim_dict:
            new_prop.shading_dimensions = ShadingDimensions.from_dict(shading_dim_dict)

        return new_prop

    def apply_properties_from_dict(self, _aperture_prop_dict):
        # type: (Dict[str, Any]) -> None
        """Apply properties from an AperturePhPropertiesAbridged dictionary.

        Arguments:
        ----------
            * _aperture_prop_dict (dict): An AperturePhPropertiesAbridged dictionary loaded from 
                the Aperture object itself. Unabridged.

        Returns:
        --------
            * None
        """

        self.winter_shading_factor = _aperture_prop_dict["winter_shading_factor"]
        self.summer_shading_factor = _aperture_prop_dict["summer_shading_factor"]
        self.variant_type = _aperture_prop_dict["variant_type"]

        # Use get to ensure backwards compatibility for now
        self.install_depth = _aperture_prop_dict.get('install_depth', 0.1016) # default = 4in.

        shading_dim_dict = _aperture_prop_dict.get("shading_dims", None)
        if shading_dim_dict:
            self.shading_dimensions = ShadingDimensions.from_dict(shading_dim_dict)
        
        return None
