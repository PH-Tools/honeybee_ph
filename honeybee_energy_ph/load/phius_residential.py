# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Calculations for Phius Residential Electrical Energy Consumption."""


def cooktop(_num_occupants, _energy_demand):
    # type: (float, float) -> float
    """Return the Phius Cooktop annual energy consumption [kWh] for a single dwelling.

    Assuming a number of meals as per Phius Guidebook V3.02, pg 73 footnote #31
    """
    ANNUAL_MEALS_PER_OCCUPANT = 500
    num_meals = _num_occupants * ANNUAL_MEALS_PER_OCCUPANT
    return _energy_demand * num_meals


def misc_electrical(_num_bedrooms, _floor_area_ft2, _num_dwellings=1):
    # type: (float, float, int) -> float
    """Return Phius Misc. Electrical Loads (MEL) annual energy consumption [kWh] for a single dwelling.

    ### Resnet 2014
    - https://codes.iccsafe.org/content/RESNET3012014P1/4-home-energy-rating-calculation-procedures-
    - Section 4.2.2.5(1): Energy Rating Reference Home
    - kWh = 413 + 0.91 * CFA + 69 * Nbr

    ### Phius Certification Guidebook v24.1.1 | Appendix N | N-7
    - https://www.phius.org/phius-certification-guidebook
    - "The basic protocol for lighting and miscellaneous electric loads is that they are calculated at
    80% of RESNET (2013) levels for the 'Rated Home'."
    - kWh = ((413 * Ndw) + (69 * Nbr) + 0.91 * CFA) * 0.8
    """
    DWELLING_TV_KWH_YR = 413
    BEDROOM_TV_KWH_YR = 69
    MELS_KWH_YR_FT2 = 0.91
    PHIUS_RESNET_FRACTION = 0.8

    a = DWELLING_TV_KWH_YR * _num_dwellings
    b = BEDROOM_TV_KWH_YR * _num_bedrooms
    c = MELS_KWH_YR_FT2 * _floor_area_ft2

    return (a + b + c) * PHIUS_RESNET_FRACTION


def lighting_interior(_floor_area_ft2, _frac_high_efficiency, _num_dwellings=1):
    # type: (float, float, int) -> float
    """Return the Phius Interior Lighting annual energy consumption [kWh] for a single dwelling.

    ### Resnet 2014
    - https://codes.iccsafe.org/content/RESNET3012014P1/4-home-energy-rating-calculation-procedures-
    - Section 4.2.2.5.2.2: Interior Lighting
    - kWh/yr = 0.8 * [(4 - 3 * q_FFIL) / 3.7] * (455 + 0.8 * CFA) + 0.2 * (455 + 0.8 * CFA)

    ### Phius Certification Guidebook v24.1.1 | Appendix N | N-7
    - https://www.phius.org/phius-certification-guidebook
    - "The basic protocol for lighting and miscellaneous electric loads is that they are calculated at
    80% of RESNET (2013) levels for the 'Rated Home'. ... The RESNET lighting formulas have been expressed more
    compactly here but are algebraically equivalent to the published versions."
    - kWh/yr = (0.2 + 0.8 * (4 - 3 * q_FFIL) / 3.7) * ((455 * Ndw) + 0.8 * iCFA) * 0.8
    """

    INT_LIGHTING_W_PER_DWELLING = 455
    INT_LIGHTING_W_FT2 = 0.8
    PHIUS_RESNET_FRACTION = 0.8

    a = 0.2 + 0.8 * (4 - 3 * _frac_high_efficiency) / 3.7
    b = (INT_LIGHTING_W_PER_DWELLING * _num_dwellings) + (INT_LIGHTING_W_FT2 * _floor_area_ft2)

    return a * b * PHIUS_RESNET_FRACTION


def lighting_exterior(_floor_area_ft2, _frac_high_efficiency, _num_dwellings=1):
    # type: (float, float, int) -> float
    """Return the Phius Exterior Lighting annual energy consumption [kWh] for a single dwelling.

    ### Resnet 2014
    - https://codes.iccsafe.org/content/RESNET3012014P1/4-home-energy-rating-calculation-procedures-
    - Section 4.2.2.5.2.3: Exterior Lighting
    - kWh = (100+0.05*FCA)*(1-FF_El)+0.25*(100+0.05*CFA)*FF_EL

    ### Phius Certification Guidebook v24.1.1 | Appendix N | N-7
    - https://www.phius.org/phius-certification-guidebook
    - "The basic protocol for lighting and miscellaneous electric loads is that they are calculated at
    80% of RESNET (2013) levels for the 'Rated Home'. ... The RESNET lighting formulas have been expressed more
    compactly here but are algebraically equivalent to the published versions."
    - kWh/yr = (1 - 0.75 * q_FFIL) * ((100 * Ndw) + (0.05 * iCFA)) * 0.8
    """

    EXT_LIGHTING_KWH_YR_PER_DWELLING = 100
    EXT_LIGHTING_KWH_YR_FT2 = 0.05
    PHIUS_RESNET_FRACTION = 0.8

    a = EXT_LIGHTING_KWH_YR_PER_DWELLING * _num_dwellings
    b = EXT_LIGHTING_KWH_YR_FT2 * _floor_area_ft2
    c = 1 - 0.75 * _frac_high_efficiency

    return c * (a + b) * PHIUS_RESNET_FRACTION


def lighting_garage(_frac_high_efficiency, _num_dwellings=1):
    # type: (float, int) -> float
    """Return the Phius Garage Lighting annual energy consumption [kWh] for a single dwelling .

    ### Resnet 2014
    - https://codes.iccsafe.org/content/RESNET3012014P1/4-home-energy-rating-calculation-procedures-
    - Section 4.2.2.5.1.3: Garage Lighting
    - kWh = 100/dwelling

    ### Phius Certification Guidebook v24.1.1 | Appendix N | N-7
    - https://www.phius.org/phius-certification-guidebook
    - "The basic protocol for lighting and miscellaneous electric loads is that they are calculated at
    80% of RESNET (2013) levels for the 'Rated Home'. ... The RESNET lighting formulas have been expressed more
    compactly here but are algebraically equivalent to the published versions."
    - kWh/yr = 100 * (1 - 0.75 * FFGL) * 0.8

    ### Phius MultiFamily Calculator (v24.0.2) | Nov. 2024
    - kWh/yr = Ndw * (100 * (1 - FFGL) + 25 * FFGL) * 0.8
    """

    GARAGE_LIGHTING_KWH_YR_PER_DWELLING = 100
    PHIUS_RESNET_FRACTION = 0.8
    a = 1 - _frac_high_efficiency
    b = 25 * _frac_high_efficiency

    return _num_dwellings * (GARAGE_LIGHTING_KWH_YR_PER_DWELLING * a + b) * PHIUS_RESNET_FRACTION
