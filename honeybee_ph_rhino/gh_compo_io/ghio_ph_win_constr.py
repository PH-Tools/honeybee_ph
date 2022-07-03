# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Component Interface for HBPH Window Construction."""

try:  # import the honeybee-energy dependencies
    from honeybee_energy.material.glazing import EnergyWindowMaterialSimpleGlazSys
    from honeybee_energy.construction.window import WindowConstruction
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy:\n\t{}'.format(e))

try:  # import the core honeybee dependencies
    from honeybee.typing import clean_and_id_ep_string
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:
    from honeybee_ph_rhino.gh_compo_io import ghio_validators
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_ph_rhino:\n\t{}'.format(e))

try:
    from honeybee_ph_utils import iso_10077_1
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_ph_utils:\n\t{}'.format(e))


class IPhWindowConstruction(object):

    display_name = ghio_validators.HBName("display_name")
    frame = ghio_validators.NotNone("frame")
    glazing = ghio_validators.NotNone("glazing")
    t_vis = ghio_validators.Float("t_vis")

    def __init__(self):
        self.display_name = clean_and_id_ep_string('PhWindowConstruction')
        self.nfrc_u_factor = None
        self.nfrc_shgc = None
        self.t_vis = 0.6

    def create_HBPH_Object(self):
        # type: () -> WindowConstruction
        """Return a new HB-Window-Construction with values set by the PH Elements."""

        # ---------------------------------------------------------------------
        # -- Create a new HB Simple Window Material and set the NFRC/HBmaterial properties
        nfrc_u_factor = self.nfrc_u_factor or iso_10077_1.calculate_window_uw(
            self.frame, self.glazing)
        nfrc_shgc = self.nfrc_shgc or self.glazing.g_value
        t_vis = self.t_vis
        window_mat = EnergyWindowMaterialSimpleGlazSys(
            self.display_name, nfrc_u_factor, nfrc_shgc, t_vis)
        window_mat.display_name = self.display_name

        # -------------------------------------------------------------------------------------
        # -- Create a new HB Window Construction
        hb_win_construction_ = WindowConstruction(self.display_name, [window_mat])

        # -------------------------------------------------------------------------------------
        # -- Set the PH Properties on the WindowConstructionProperties
        hb_win_construction_.properties.ph.ph_frame = self.frame
        hb_win_construction_.properties.ph.ph_glazing = self.glazing

        return hb_win_construction_

    def __str__(self):
        return '{}(display_name={})'.format(self.__class__.__name__, self.display_name)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
