import pytest

from honeybee_ph_utils.aisi_s250_21 import (
    OTZ_COEFFICIENTS,
    StudSpacingInches,
    StudThicknessMil,
    calculate_stud_cavity_effective_u_value,
    framing_factor,
    overall_thermal_zone,
    overall_thermal_zone_framing_factor,
    r_value_series_cavity_path,
    r_value_series_stud_path,
    stud_web_r_value,
    u_value_at_stud,
    u_value_total,
)


def test_calculation_steps_no_ext_insulation():
    # Steel Stud Attributes
    STUD_FLANGE_WIDTH_INCH = 1.625
    STUD_DEPTH_INCH = 8
    STUD_THICKNESS_MILS = 43
    STUD_SPACING_INCH = 16
    K = 495  # BTU/hr-ft2-F

    # Assembly Attributes
    R_SE = 0.17
    R_EXT_CLADDING = 0.07
    R_EXT_INSULATION = 0.0
    R_EXT_SHEATHING = 0.56
    R_INT_SHEATHING = 0.56
    R_SI = 0.68
    R_STUD_CAVITY_INSULATION = 25

    # Factors
    spacing = StudSpacingInches(STUD_SPACING_INCH)
    thickness = StudThicknessMil(STUD_THICKNESS_MILS)
    C0, C1, C2, C3, C4, C5 = OTZ_COEFFICIENTS[spacing][thickness]

    # ---------
    otz = overall_thermal_zone(C0, C1, C2, C3, C4, C5, R_STUD_CAVITY_INSULATION, R_EXT_INSULATION)
    assert otz == 2.6392749999999996

    ff = framing_factor(STUD_FLANGE_WIDTH_INCH, STUD_THICKNESS_MILS)
    assert ff == 0.02646153846153846

    web_r_value = stud_web_r_value(STUD_DEPTH_INCH, K)
    assert web_r_value == 0.01616161616161616

    stud_u_value = u_value_at_stud(ff, R_STUD_CAVITY_INSULATION, web_r_value)
    assert stud_u_value == 1.6762492307692305

    r_1 = 1 / stud_u_value
    assert r_1 == 0.5965699978523481

    r_2 = 0  #  <----- TODO: Calculate this properly calc U_2
    r_3 = r_1 + r_2
    assert r_3 == 0.5965699978523481

    r_stud_path = r_value_series_stud_path(
        R_EXT_CLADDING, R_EXT_INSULATION, R_EXT_SHEATHING, r_3, R_INT_SHEATHING, R_SE, R_SI
    )
    assert r_stud_path == 2.6365699978523485

    r_cavity_path = r_value_series_cavity_path(
        R_EXT_CLADDING, R_EXT_INSULATION, R_EXT_SHEATHING, R_STUD_CAVITY_INSULATION, R_INT_SHEATHING, R_SE, R_SI
    )
    assert r_cavity_path == 27.04

    otz_ff = overall_thermal_zone_framing_factor(otz, STUD_SPACING_INCH)
    assert otz_ff == 0.16495468749999997

    u_overall = u_value_total(otz_ff, r_cavity_path, r_stud_path)
    assert u_overall == 0.09344597545984833

    r_overall = 1 / u_overall
    assert r_overall == 10.7013704451047


def test_calculation_steps_with_ext_insulation():
    # Steel Stud Attributes
    STUD_FLANGE_WIDTH_INCH = 1.625
    STUD_DEPTH_INCH = 8
    STUD_THICKNESS_MILS = 43
    STUD_SPACING_INCH = 16
    K = 495  # BTU/hr-ft2-F

    # Assembly Attributes
    R_SE = 0.17
    R_EXT_CLADDING = 0.07
    R_EXT_INSULATION = 1.0
    R_EXT_SHEATHING = 0.56
    R_INT_SHEATHING = 0.56
    R_SI = 0.68
    R_STUD_CAVITY_INSULATION = 25

    # Factors
    spacing = StudSpacingInches(STUD_SPACING_INCH)
    thickness = StudThicknessMil(STUD_THICKNESS_MILS)
    C0, C1, C2, C3, C4, C5 = OTZ_COEFFICIENTS[spacing][thickness]

    # ---------
    otz = overall_thermal_zone(C0, C1, C2, C3, C4, C5, R_STUD_CAVITY_INSULATION, R_EXT_INSULATION)
    assert otz == 2.9275479999999994

    ff = framing_factor(STUD_FLANGE_WIDTH_INCH, STUD_THICKNESS_MILS)
    assert ff == 0.02646153846153846

    web_r_value = stud_web_r_value(STUD_DEPTH_INCH, K)
    assert web_r_value == 0.01616161616161616

    stud_u_value = u_value_at_stud(ff, R_STUD_CAVITY_INSULATION, web_r_value)
    assert stud_u_value == 1.6762492307692305

    r_1 = 1 / stud_u_value
    assert r_1 == 0.5965699978523481

    r_2 = 0  #  <----- TODO: Calculate this properly calc U_2
    r_3 = r_1 + r_2
    assert r_3 == 0.5965699978523481

    r_stud_path = r_value_series_stud_path(
        R_EXT_CLADDING, R_EXT_INSULATION, R_EXT_SHEATHING, r_3, R_INT_SHEATHING, R_SE, R_SI
    )
    assert r_stud_path == 3.6365699978523485

    r_cavity_path = r_value_series_cavity_path(
        R_EXT_CLADDING, R_EXT_INSULATION, R_EXT_SHEATHING, R_STUD_CAVITY_INSULATION, R_INT_SHEATHING, R_SE, R_SI
    )
    assert r_cavity_path == 28.04

    otz_ff = overall_thermal_zone_framing_factor(otz, STUD_SPACING_INCH)
    assert otz_ff == 0.18297174999999996

    u_overall = u_value_total(otz_ff, r_cavity_path, r_stud_path)
    assert u_overall == 0.07945233064644197

    r_overall = 1 / u_overall
    assert r_overall == 12.586163198282238


# Pre-Computed Values from:
# AISI North American Standard for Thermal Transmittance of Building Envelopes with Cold-Formed Steel Framing, 2021 Edition With Supplement 1
# Table 1-1(a) Framing Spacing = 16 inches
# Table 1-2(a) Framing Spacing = 24 inches
U_VALUE_TEST_CASES_DICT = {
    16: {  # Inched OC
        3.5: {  # Depth
            13: {0: 0.129, 1: 0.107, 4: 0.076, 8: 0.058},  # R-Values (cavity / ext)
            15: {0: 0.122, 1: 0.101, 4: 0.073, 8: 0.056},
        },
        6.0: {
            19: {0: 0.108, 1: 0.090, 4: 0.066, 8: 0.052},
            21: {0: 0.104, 1: 0.087, 4: 0.064, 8: 0.050},
        },
        8.0: {
            25: {0: 0.093, 1: 0.079, 4: 0.060, 8: 0.0474},
        },
    },
    24: {
        3.5: {13: {0: 0.109, 1: 0.093, 4: 0.069, 8: 0.053}, 15: {0: 0.102, 1: 0.087, 4: 0.065, 8: 0.051}},
        6.0: {19: {0: 0.088, 1: 0.076, 4: 0.058, 8: 0.046}, 21: {0: 0.083, 1: 0.072, 4: 0.056, 8: 0.045}},
        8.0: {25: {0: 0.074, 1: 0.065, 4: 0.051, 8: 0.042}},
    },
}

# Flatten the nested dict for parametrize
U_VALUE_TEST_CASES = []
for spacing, depths in U_VALUE_TEST_CASES_DICT.items():
    for depth, cavities in depths.items():
        for r_cavity, r_exts in cavities.items():
            for r_ext, result in r_exts.items():
                U_VALUE_TEST_CASES.append(
                    ({"spacing": spacing, "stud_depth": depth, "r_cavity": r_cavity, "r_ext": r_ext}, result)
                )


@pytest.mark.parametrize("inputs, result", U_VALUE_TEST_CASES)
def test_calculate_16in_OC_no_ext_insulation(inputs, result):
    u_value = calculate_stud_cavity_effective_u_value(
        _r_ext_cladding=0.07,
        _r_ext_insulation=inputs["r_ext"],
        _r_ext_sheathing=0.56,
        _r_cavity_insulation=inputs["r_cavity"],
        _stud_spacing_inch=StudSpacingInches(str(inputs["spacing"])),
        _stud_thickness_mil=StudThicknessMil("43"),
        _stud_flange_width_inch=1.625,
        _stud_depth_inch=inputs["stud_depth"],
        _steel_conductivity=495,
        _r_int_sheathing=0.56,
        _r_se=0.17,
        _r_si=0.68,
    )
    whole_assembly_u_value = 1 / ((1 / u_value) + 0.07 + inputs["r_ext"] + 0.56 + 0.56 + 0.17 + 0.68)
    assert result == pytest.approx(whole_assembly_u_value, rel=0.01)
