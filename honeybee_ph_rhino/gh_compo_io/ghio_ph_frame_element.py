# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Component Interface for HBPH Frame Element"""

try:  # import the core honeybee dependencies
    from honeybee.typing import clean_and_id_ep_string
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:
    from honeybee_energy_ph.construction import window
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy_ph:\n\t{}'.format(e))

try:
    from honeybee_ph_rhino.gh_compo_io import ghio_validators
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_ph_rhino:\n\t{}'.format(e))


class IPhWindowFrameElement(object):
    """Interface to collect and clean PhWindowFrameElement user-inputs."""

    display_name = ghio_validators.HBName("display_name")
    width = ghio_validators.FloatPositiveValue("width")
    u_factor = ghio_validators.FloatPositiveValue("u_factor")
    psi_glazing = ghio_validators.FloatPositiveValue("psi_glazing")
    psi_install = ghio_validators.Float("psi_install")
    chi_value = ghio_validators.Float("chi_value")

    def __init__(self):
        self.display_name = clean_and_id_ep_string('PhWindowFrameElement')
        self.width = 0.1
        self.u_factor = 1.0
        self.psi_glazing = 0.04
        self.psi_install = 0.04
        self.chi_value = 0.0

    def create_HBPH_Object(self):
        # type: () -> window.PhWindowFrameElement
        """Returns a new HBPH PhWindowFrameElement object."""

        obj = window.PhWindowFrameElement(self.display_name)
        obj.display_name = self.display_name
        obj.width = self.width
        obj.u_factor = self.u_factor
        obj.psi_glazing = self.psi_glazing
        obj.psi_install = self.psi_install
        obj.chi_value = self.chi_value

        return obj

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.display_name)
