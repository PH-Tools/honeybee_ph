# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
AISI S250-21 | “North American Standard for Thermal Transmittance of Building Envelopes With Cold-Formed Steel Framing, 2021 Edition”

https://www.steel.org/2021/09/aisi-publishes-aisi-s250-21-north-american-standard-for-thermal-transmittance-of-building-envelopes-with-cold-formed-steel-framing-2021-edition/

Thermal transmittance (U-factors) of above-grade wall assemblies constructed with standard Cshape studs and track,
where the framing spacing is 6, 12, 16 or 24 inches on-center, shall be determined in accordance with Equation
B3.1.8-1 using Sections B3.1.1 through B3.1.8 or shall be determined in accordance with Appendix 1. Where a
non-standard designation thickness for the cold-formed steel framing member is applicable, values for the OTZ coefficients
from Table B3.1.11 and thermal conductivity from Table B3.1.3-1 shall be based on linear interpolation for the
intermediate value of designation thickness or shall be based on the next larger standard designation thickness.
Extrapolation is not permitted.

NOTE: AISI does not provide an 'SI' version of the coefficients in Table B3.1.11. therefor
ALL values in this module are in imperial units. This includes R-Values, U-Values, and dimensions.
"""

from honeybee_ph_utils.enumerables import CustomEnum


class StudSpacingInches(CustomEnum):
    allowed = [
        "6",
        "12",
        "16",
        "24",
    ]

    def __init__(self, _value=1):
        # type: (str | int) -> None
        super(StudSpacingInches, self).__init__(_value)


class StudThicknessMil(CustomEnum):
    allowed = [
        "33",
        "43",
        "54",
        "68",
    ]

    def __init__(self, _value=1):
        # type: (str | int) -> None
        super(StudThicknessMil, self).__init__(_value)


# [AISI S250-21w/S1-22] Table B3.1.1-1 | OTZ Coefficients
OTZ_COEFFICIENTS = {
    StudSpacingInches("6"): {
        StudThicknessMil("33"): [1.8583, 0.07478, 0.1488, -0.001859, -0.005103, 0.002013],
        StudThicknessMil("43"): [1.9826, 0.0736, 0.1501, -0.001816, -0.005314, 0.002149],
        StudThicknessMil("54"): [2.0814, 0.07131, 0.1522, -0.001713, -0.005295, 0.00205],
        StudThicknessMil("68"): [2.211, 0.06816, 0.1508, -0.001652, -0.005576, 0.0023],
    },
    StudSpacingInches("12"): {
        StudThicknessMil("33"): [2.1584, 0.05118, 0.2079, -0.001384, -0.005367, 0.002253],
        StudThicknessMil("43"): [2.2077, 0.06381, 0.1992, -0.001713, -0.006235, 0.003499],
        StudThicknessMil("54"): [2.2974, 0.06439, 0.2043, -0.001686, -0.006908, 0.003943],
        StudThicknessMil("68"): [2.4136, 0.05185, 0.2166, -0.001216, -0.00684, 0.003748],
    },
    StudSpacingInches("16"): {
        StudThicknessMil("33"): [2.2771, 0.03843, 0.1964, -0.001141, -0.005237, 0.003197],
        StudThicknessMil("43"): [2.3769, 0.04037, 0.2011, -0.001195, -0.005677, 0.003714],
        StudThicknessMil("54"): [2.4945, 0.04089, 0.1996, -0.001161, -0.005719, 0.003927],
        StudThicknessMil("68"): [2.5917, 0.04614, 0.1922, -0.001391, -0.005884, 0.004606],
    },
    StudSpacingInches("24"): {
        StudThicknessMil("33"): [3.182, -0.02946, 0.2432, 0, -0.00752, 0.003572],
        StudThicknessMil("43"): [2.751, 0.0128, 0.1965, -0.00074, -0.006709, 0.005169],
        StudThicknessMil("54"): [2.572, 0.00426, 0.2285, 0, -0.0061, 0.003509],
        StudThicknessMil("68"): [2.936, -0.00324, 0.2256, 0, -0.00643, 0.00419],
    },
}  # type: dict[StudSpacingInches, dict[StudThicknessMil, list[float]]]


# [AISI S250-21w/S1-22] Table B3.1.3-1 | Cold-Formed Steel Thermal Conductivity (Btu/hr-ft2-F)
STEEL_CONDUCTIVITY = {
    StudThicknessMil("33"): 381.0,
    StudThicknessMil("43"): 495.0,
    StudThicknessMil("54"): 622.0,
    StudThicknessMil("68"): 783.0,
}


def overall_thermal_zone(
    c_0,
    c_1,
    c_2,
    c_3,
    c_4,
    c_5,
    r_cavity,
    r_ext_insulation,
):
    # type: (float, float, float, float, float, float, float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.1 Overall Thermal Zone.

    The overall thermal zone (OTZ) shall be determined in accordance with Equation B3.1.1-1.
    The appropriate coefficients for use in Equation B3.1.1-1 shall be obtained from Table B3.1.11
    with the given on-center spacing of framing members and C-shape designation thickness.

        Eq. B3.1.1-1: OTZ = C_0 + C_1 * R_cav + C_2 * R_she + C_3 * R_cav^2 + C_4 * R_she^2 + C_5 * R_cav * R_she

    r_cavity (r_cav) = R_air + R_ins
        * R_ins: Thermal resistance (R-value) of cavity insulation (h-ft2-F/Btu)
            * = 0 where wall cavity contains no insulation
        * R_air: Thermal resistance (R-value) of the cavity air space (h-ft2-F/Btu)
            * = 0.91 where wall cavity contains an air space
            * = 0 where wall cavity contains no air space

    Args:
        C_0: Coefficient from Table B3.1.1-1
        C_1: Coefficient from Table B3.1.1-1
        C_2: Coefficient from Table B3.1.1-1
        C_3: Coefficient from Table B3.1.1-1
        C_4: Coefficient from Table B3.1.1-1
        C-5: Coefficient from Table B3.1.1-1
        r_cavity (R_cav): Total thermal resistance (R-value) of the wall cavity (h-ft2-F/Btu)
        r_ext_insulation (R_she): Thermal resistance (R-value) of exterior continuous insulation (hr-ft2-F/Btu). R_she does
            not include wood or gypsum panels.
    Returns:
        OTZ: Overall thermal zone (inch)
    """

    return (
        c_0
        + c_1 * r_cavity
        + c_2 * r_ext_insulation
        + c_3 * r_cavity**2
        + c_4 * r_ext_insulation**2
        + c_5 * r_cavity * r_ext_insulation
    )


def framing_factor(stud_flange_width_inch, stud_thickness_mils):
    # type: (float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.2 C-Shape Framing Factor.

    The C-shape framing factor (FFcs) for the cold-formed steel framing shall be determined in
    accordance with Equation B3.1.2-1:

        Eq. B3.1.2-1: FF_cs = (CFS_t / 1000) / CFS_flange

    Args:
        stud_thickness_mils (CFS_t): Designation thickness of cold-formed steel framing member (mils)
        stud_flange_width_inch (CFS_flange): Flange width of cold-formed steel framing member (inches)
    Returns:
        float: (FF_cs) C-shape framing factor (unitless)
    """

    return ((stud_thickness_mils) / 1000) / stud_flange_width_inch


def stud_web_r_value(stud_depth_inch, conductivity):
    # type: (float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.3.1 Thermal Resistance of C-Shape Web.

    The thermal resistance (R-value) of the web of the cold-formed steel framing member (Rs-  wall )
    shall be determined in accordance with Equation B3.1.3-1:

        * R_s-wall = CFS_depth / k

    Args:
        stud_depth (CFS_depth): Web depth of cold-formed steel framing member that is in contact with cavity insulation (inches)
            as illustrated by Figure B3.1.3-1 without cavity air space and Figure B3.1.3-2 with cavity air space
        conductivity (k): Thermal conductivity of cold-formed steel as selected from Table B3.1.3-1 (Btu/h-ft2-F)
    Returns:
        float: (R_s-wall) Thermal resistance (R-value) of the web of the cold-formed steel framing member (h-ft2-F/Btu)
    """

    return stud_depth_inch / conductivity


def u_value_at_stud(framing_factor, r_value_cavity_insulation, r_value_stud_web):
    # type: (float, float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.3.2 Thermal Transmittance of Cavity with Insulation.

    The parallel path thermal transmittance (U-factor) of the assembly where insulation(s) are in contact with
    cold-formed steel framing member (U1 ) shall be determined in accordance with Equation B3.1.3-2. Where there is
    no insulation in the wall cavity, Equation B3.1.3-2 shall not be used and the resultant value of R 1 in
    Equation B3.1.3-3 shall be “zero” (0).

        * U_1 = (1 - FFcs) / R_ins + FFcs / Rs-wall

    Args:
        framing_factor (FF_cs): C-shape framing factor determined from Equation B3.1.2-1
        r_value_cavity_insulation (R_ins): Thermal resistance (R-value) of cavity insulation (h-ft2-F/Btu)
        r_value_stud_web (R_s-wall): Thermal resistance (R-value) of the wall assembly at the web of the cold-formed steel framing
            member determined from Equation B3.1.3-1 (h-ft2-F/Btu)
    Returns:
        float: (U_1) Parallel path thermal transmittance (U-factor) of the assembly where insulation(s) are
            in contact with cold-formed steel framing member (Btu/hr-ft2-F)
    """

    return (1 - framing_factor) / r_value_cavity_insulation + framing_factor / r_value_stud_web


def r_value_series_stud_path(
    r_ext_cladding,
    r_ext_insulation,
    r_ext_sheathing,
    r_3,
    r_int_sheathing,
    r_se=0.17,
    r_si=0.68,
):
    # type: (float, float, float, float, float, float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.6.1 Thermal Resistance (R-value) of Series Paths | C-Shape Path.

    The effective thermal resistance (R-value) of all materials in the design assembly in series for the
    path containing cold-formed steel (R_sps), illustrated as the C-shape path in Figure B3.1.3-1 or
    Figure B3.1.3-2, shall be determined using Equation B3.1.6-1:

        * R_sps = R_o + Side_ext + R_she + Sheath_ext + R_3 + Sheath_int + R_i

    Args:
        r_ext_cladding (Side_ext): Thermal resistance (R-value) of exterior siding (h-ft2-F/Btu)
        r_ext_insulation (R_she): Thermal resistance (R-value) of exterior continuous insulation (h-ft2-F/Btu)
        r_ext_sheathing (Sheath_ext): Thermal resistance (R-value) of all exterior sheathing(s) (h-ft2-F/Btu)
        R_3: Thermal resistance (R-value) determined from Equation B3.1.5-1 (h-ft2-F/Btu)
        r_int_sheathing (Sheath_int): Thermal resistance (R-value) of all interior sheathing(s) (h-ft2-F/Btu)
        r_se (R_o): [Default=0.17] Thermal resistance (R-value) of outside air film (h-ft2-F/Btu)
        r_si (R_i): [Default=0.68] Thermal resistance (R-value) of inside air film (h-ft2-F/Btu)
    Returns:
        float: (R_sps) Effective thermal resistance (R-value) of all materials in the design assembly
            in series for the path containing cold-formed steel (h-ft2-F/Btu)
    """
    return r_se + r_ext_cladding + r_ext_insulation + r_ext_sheathing + r_3 + r_int_sheathing + r_si


def r_value_series_cavity_path(
    r_ext_cladding,
    r_ext_insulation,
    r_ext_sheathing,
    r_cavity_insulation,
    r_int_sheathing,
    r_se=0.17,
    r_si=0.68,
):
    # type: (float, float, float, float, float, float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.6.1 Thermal Resistance (R-value) of Series Paths | Cavity Path.

    B3.1.6.2 Cavity Path The thermal resistance (R-value) of all materials in the design assembly in series for the path
    containing only cavity insulation (R_spc), illustrated as the cavity path in Figure B3.1.31 or Figure B3.1.3-2,
    shall be determined using Equation B3.1.6-2:

        * R_spc = R_o + Side_ext + R_she + Sheath_ext + R_ins + R_air + Sheath_int + R_i

    Args:
        R_o: Thermal resistance (R-value) of outside air film (h-ft2F/Btu)
        r_ext_cladding (Side_ext): Thermal resistance (R-value) of exterior siding (h-ft2F/Btu)
        r_ext_insulation (R_she): Thermal resistance (R-value) of exterior continuous insulation (h-ft2F/Btu)
        r_ext_sheathing (Sheath_ext): Thermal resistance (R-value) of all exterior sheathing(s) (h-ft2F/Btu)
        r_cavity_insulation (R_ins): Thermal resistance (R-value) of cavity insulation (h-ft2F/Btu)
        R_air: Thermal resistance (R-value) of the cavity air space (h-ft2F/Btu)
           : 0.91 where wall cavity contains an air space
           : 0.00 where wall cavity contains no air space
        r_int_sheathing (Sheath_int): Thermal resistance (R-value) of all interior sheathing(s) (h-ft2F/Btu)
        R_i: Thermal resistance (R-value) of inside air film (h-ft2F/Btu)
    Returns:
        float: (R_spc) Effective thermal resistance (R-value) of all materials in the design assembly
            in series for the path containing only cavity insulation (h-ft2-F/Btu)
    """

    return r_se + r_ext_cladding + r_ext_insulation + r_ext_sheathing + r_cavity_insulation + r_int_sheathing + r_si


def overall_thermal_zone_framing_factor(_overall_thermal_zone, _stud_spacing_inch):
    # type: (float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.7 OTZ Framing Factor.

    The OTZ Framing Factor (FF_otz) shall be determined using Equation B3.1.7-1:
        * FF_otz = OTZ / FS

    Args:
        _overall_thermal_zone (OTZ): Overall thermal zone (inch)
        _stud_spacing_inch (fs): Spacing of cold-formed steel framing members (inches)
    Returns:
        float: (FF_otz) OTZ Framing Factor (unitless)
    """

    return _overall_thermal_zone / _stud_spacing_inch


def u_value_total(_overall_thermal_zone_framing_factor, _r_value_series_cavity_path, _r_value_series_stud_path):
    # type: (float, float, float) -> float
    """
    [AISI S250-21w/S1-22] B3.1.8 Overall Thermal Transmittance (U-Factor).

    The overall thermal transmittance (U-factor) of the above-grade wall assembly (U_o)
    shall be determined using Equation B3.1.8-1:

        * U_o = (1 - FF_otz) / R_spc + FF_otz / R_sps

    Args:
        _overall_thermal_zone_framing_factor (FF_otz) : OTZ Framing Factor determined from Equation B3.1.7-1 (dimensionless)
        _r_value_series_cavity_path (R_spc) : Thermal resistance (R-value) of all materials in the design assembly
            in series for the cavity path determined from Equation B3.1.6-2 (h-ft2-F/Btu)
        _r_value_series_stud_path (R_sps) : Thermal resistance (R-value) of all materials in the design assembly
            in series for the C-shape path determined from Equation B3.1.6-1 (h-ft2-F/Btu)
    Returns:
        float: (U_o) Overall thermal transmittance (U-factor) of the above-grade wall assembly (Btu/hr-ft2-F)
    """
    return (
        1 - _overall_thermal_zone_framing_factor
    ) / _r_value_series_cavity_path + _overall_thermal_zone_framing_factor / _r_value_series_stud_path


def calculate_stud_cavity_effective_u_value(
    _r_ext_cladding,
    _r_ext_insulation,
    _r_ext_sheathing,
    _r_cavity_insulation,
    _stud_spacing_inch,
    _stud_thickness_mil,
    _stud_flange_width_inch,
    _stud_depth_inch,
    _steel_conductivity,
    _r_int_sheathing,
    _r_se=0.17,
    _r_si=0.68,
):
    # type: (float, float, float, float, StudSpacingInches, StudThicknessMil, float, float, float, float, float, float) -> float
    try:
        C0, C1, C2, C3, C4, C5 = OTZ_COEFFICIENTS[_stud_spacing_inch][_stud_thickness_mil]
    except KeyError as e:
        msg = "The given stud spacing: '{}' and stud-thickness '{}' is not supported. ".format(
            _stud_spacing_inch.value, _stud_thickness_mil.value
        )
        msg += "Please use one of the following combinations:\n"
        msg += "\tStud Spacing: {}\n".format(", ".join(StudSpacingInches.allowed))
        msg += "\tStud Thickness: {}\n".format(", ".join(StudThicknessMil.allowed))
        msg += "Error: {}".format(e)
        raise KeyError(msg)

    otz = overall_thermal_zone(C0, C1, C2, C3, C4, C5, _r_cavity_insulation, _r_ext_insulation)
    ff = framing_factor(_stud_flange_width_inch, float(_stud_thickness_mil.value))
    web_r_value = stud_web_r_value(_stud_depth_inch, _steel_conductivity)
    stud_u_value = u_value_at_stud(ff, _r_cavity_insulation, web_r_value)

    r_1 = 1 / stud_u_value
    r_2 = 0  #  <----- TODO: Calculate this properly calc U_2
    r_3 = r_1 + r_2

    r_stud_path = r_value_series_stud_path(
        _r_ext_cladding, _r_ext_insulation, _r_ext_sheathing, r_3, _r_int_sheathing, _r_se, _r_si
    )
    r_cavity_path = r_value_series_cavity_path(
        _r_ext_cladding, _r_ext_insulation, _r_ext_sheathing, _r_cavity_insulation, _r_int_sheathing, _r_se, _r_si
    )
    otz_ff = overall_thermal_zone_framing_factor(otz, float(_stud_spacing_inch.value))

    u_overall = u_value_total(otz_ff, r_cavity_path, r_stud_path)
    r_overall = 1 / u_overall

    # Get the stud cavity U-Value by itself
    r_stud_cavity = (
        r_overall - _r_ext_cladding - _r_ext_insulation - _r_ext_sheathing - _r_int_sheathing - _r_se - _r_si
    )
    u_stud_cavity = 1 / r_stud_cavity
    return u_stud_cavity
