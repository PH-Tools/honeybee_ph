# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Component Interface for Building Segments"""

try:
    from typing import List
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import bldg_segment, location, phi, phius
from honeybee_ph_standards.sourcefactors import factors, phius_CO2_factors, phius_source_energy_factors
from honeybee_ph_rhino.gh_compo_io import ghio_validators


class ISetPoints(object):
    """Interface to collect and clean SetPoint user-inputs"""

    winter = ghio_validators.IntegerNonZero("winter")
    summer = ghio_validators.IntegerNonZero("summer")

    def __init__(self):
        self.winter = 20
        self.summer = 25


class IBldgSegment(object):
    """Interface to collect and clean BldgSegment user-inputs."""

    display_name = ghio_validators.HBName("display_name")
    num_floor_levels = ghio_validators.IntegerNonZero("num_floor_levels")
    num_dwelling_units = ghio_validators.IntegerNonZero("num_dwelling_units")
    climate = ghio_validators.NotNone("climate")
    phius_certification = ghio_validators.NotNone("phius_certification")
    phi_certification = ghio_validators.NotNone("phi_certification")

    def __init__(self):
        self.display_name = '_unnamed_bldg_segment_'
        self.num_floor_levels = 1
        self.num_dwelling_units = 1
        self.climate = location.Climate()
        self.phius_certification = phius.PhiusCertification()
        self.phi_certification = phi.PhiCertification()
        self.set_points = ISetPoints()
        self._source_energy_factors = factors.FactorCollection(
            'Source_Energy', self._default_phius_source_energy_factors)
        self._co2e_factors = factors.FactorCollection(
            'CO2', self._default_phius_CO2_factors)

    @property
    def source_energy_factors(self):
        return self._source_energy_factors

    @source_energy_factors.setter
    def source_energy_factors(self, _input_list):
        # type: (List[factors.Factor]) -> None
        for factor in _input_list:
            self._source_energy_factors.add_factor(factor)

    @property
    def co2e_factors(self):
        return self._co2e_factors

    @co2e_factors.setter
    def co2e_factors(self, _input_list):
        # type: (List[factors.Factor]) -> None
        for factor in _input_list:
            self._source_energy_factors.add_factor(factor)

    @property
    def _default_phius_source_energy_factors(self):
        # type: () -> List[factors.Factor]
        """Return a list of default source-energy factors."""
        return factors.build_factors_from_library(phius_source_energy_factors.factors_2021)

    @property
    def _default_phius_CO2_factors(self):
        # type: () -> List[factors.Factor]
        return factors.build_factors_from_library(phius_CO2_factors.factors_2021)

    def create_hbph_bldg_segment(self):
        # type: () -> bldg_segment.BldgSegment
        """Returns a new HBPH BldgSegment object with attribute value set."""

        obj = bldg_segment.BldgSegment()
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            setattr(obj, attr_name, getattr(self, attr_name))
        return obj

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.display_name)
