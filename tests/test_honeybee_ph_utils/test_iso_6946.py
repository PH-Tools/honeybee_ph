import pytest
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass

from honeybee_energy_ph.properties.materials.opaque import EnergyMaterialPhProperties
from honeybee_ph_utils.iso_6946 import (
    MAX_HEAT_FLOW_PATHS,
    TooManyHeatFlowPathsError,
    get_equivalent_conductivity,
    get_error_percent,
    get_layer_paths,
    get_r_value_lower_limit,
    get_r_value_mean_of_limits,
    get_r_value_upper_limit,
)

# -- A 38mm wood stud at 406.4mm o.c. in 140mm of mineral wool
STUD_WIDTH_MM = 38.0
STUD_SPACING_MM = 406.4
CAVITY_THICKNESS_M = 0.140
STUD_CONDUCTIVITY = 0.130
INSULATION_CONDUCTIVITY = 0.038

R_SI = 0.13
R_SE = 0.04


def _material(_name, _thickness, _conductivity):
    # type: (str, float, float) -> EnergyMaterial
    return EnergyMaterial(_name, thickness=_thickness, conductivity=_conductivity, density=999, specific_heat=999)


def _framed_material(_columns, _conductivities, _thickness=CAVITY_THICKNESS_M, _rows=None):
    # type: (list, list, float, list) -> EnergyMaterial
    """Build a single 'hybrid' EnergyMaterial with a division-grid one cell wide per conductivity."""
    total_width = sum(_columns)
    area_weighted_conductivity = sum(w * k for w, k in zip(_columns, _conductivities)) / total_width

    hybrid_material = _material("hybrid", _thickness, area_weighted_conductivity)
    prop_ph = getattr(hybrid_material.properties, "ph")  # type: EnergyMaterialPhProperties
    prop_ph.divisions.set_column_widths(_columns)
    prop_ph.divisions.set_row_heights(_rows or [1.0])
    for column_num, conductivity in enumerate(_conductivities):
        for row_num in range(prop_ph.divisions.row_count):
            cell_material = _material("cell_{}_{}".format(column_num, row_num), _thickness, conductivity)
            prop_ph.divisions.set_cell_material(column_num, row_num, cell_material)
    return hybrid_material


def _stud_cavity_material():
    # type: () -> EnergyMaterial
    return _framed_material(
        [STUD_WIDTH_MM, STUD_SPACING_MM - STUD_WIDTH_MM],
        [STUD_CONDUCTIVITY, INSULATION_CONDUCTIVITY],
    )


def _stud_wall_materials():
    # type: () -> list
    """The framed wall from the packet PRD: gypsum / stud-cavity / OSB / EPS."""
    return [
        _material("gypsum", 0.0127, 0.16),
        _stud_cavity_material(),
        _material("osb", 0.0127, 0.13),
        _material("eps", 0.050, 0.035),
    ]


def test_empty_material_list_returns_zero():
    assert get_r_value_upper_limit([]) == 0.0
    assert get_r_value_lower_limit([]) == 0.0
    assert get_r_value_mean_of_limits([]) == 0.0
    assert get_error_percent([]) == 0.0


def test_single_uniform_layer_limits_are_equal():
    materials = [_material("eps", 0.050, 0.035)]

    assert get_r_value_upper_limit(materials) == pytest.approx(0.050 / 0.035)
    assert get_r_value_lower_limit(materials) == pytest.approx(0.050 / 0.035)


def test_uniform_layer_stack_limits_equal_the_series_sum():
    materials = [_material("gypsum", 0.0127, 0.16), _material("eps", 0.050, 0.035)]
    series_sum = 0.0127 / 0.16 + 0.050 / 0.035

    assert get_r_value_upper_limit(materials) == pytest.approx(series_sum)
    assert get_r_value_lower_limit(materials) == pytest.approx(series_sum)
    assert get_r_value_mean_of_limits(materials) == pytest.approx(series_sum)
    assert get_error_percent(materials) == pytest.approx(0.0)

    # -- With no inhomogeneous layer the films cannot pull the two limits apart either.
    assert get_r_value_upper_limit(materials, R_SI, R_SE) == pytest.approx(series_sum + R_SI + R_SE)
    assert get_r_value_lower_limit(materials, R_SI, R_SE) == pytest.approx(series_sum + R_SI + R_SE)
    assert get_error_percent(materials, R_SI, R_SE) == pytest.approx(0.0)


def test_single_framed_layer_limits_are_equal_to_the_grid_equivalent_conductivity():
    """The fact that makes a grid-level 'mean of limits' impossible: for ONE layer, both ISO 6946
    limits are the area-weighted value the division-grid already reports (see issue #116)."""
    stud_cavity = _stud_cavity_material()
    prop_ph = getattr(stud_cavity.properties, "ph")  # type: EnergyMaterialPhProperties
    grid_r_value = CAVITY_THICKNESS_M / prop_ph.divisions.get_equivalent_conductivity()

    assert get_r_value_upper_limit([stud_cavity]) == pytest.approx(grid_r_value)
    assert get_r_value_lower_limit([stud_cavity]) == pytest.approx(grid_r_value)
    assert get_error_percent([stud_cavity]) == pytest.approx(0.0)


def test_framed_wall_matches_the_hand_computed_limits_with_films_inside():
    """The strict ISO 6946 6.7 reading: the surface resistances sit inside each upper-limit path."""
    materials = _stud_wall_materials()

    assert get_r_value_upper_limit(materials, R_SI, R_SE) == pytest.approx(5.029968, abs=1e-6)
    assert get_r_value_lower_limit(materials, R_SI, R_SE) == pytest.approx(4.779778, abs=1e-6)
    assert get_r_value_mean_of_limits(materials, R_SI, R_SE) == pytest.approx(4.904873, abs=1e-6)


def test_framed_wall_films_inside_and_films_added_are_not_the_same_number():
    """Films added to a film-free upper limit is the PH-Navigator editor's reading, and it is not
    the same as carrying them inside each path. Only the lower limit is unaffected."""
    materials = _stud_wall_materials()
    films = R_SI + R_SE

    assert get_r_value_upper_limit(materials) + films == pytest.approx(5.019157, abs=1e-6)
    assert get_r_value_lower_limit(materials) + films == pytest.approx(4.779778, abs=1e-6)
    assert get_r_value_mean_of_limits(materials) + films == pytest.approx(4.899468, abs=1e-6)


def test_framed_wall_error_percent():
    materials = _stud_wall_materials()
    r_value_upper = get_r_value_upper_limit(materials)
    r_value_lower = get_r_value_lower_limit(materials)
    r_value_mean = get_r_value_mean_of_limits(materials)

    expected = (r_value_upper - r_value_lower) / (2.0 * r_value_mean) * 100.0
    assert get_error_percent(materials) == pytest.approx(expected)
    assert get_error_percent(materials) > 0.0


def test_two_framed_layers_use_the_cartesian_product_of_paths():
    """Framing is read as staggered: 2 paths x 3 paths = 6 paths through the assembly."""
    layer_1 = _framed_material([1.0, 3.0], [0.13, 0.038], _thickness=0.140)
    layer_2 = _framed_material([1.0, 1.0, 2.0], [0.13, 0.05, 0.038], _thickness=0.040)
    materials = [layer_1, layer_2]

    paths_1 = get_layer_paths(layer_1)
    paths_2 = get_layer_paths(layer_2)
    assert len(paths_1) == 2
    assert len(paths_2) == 3

    expected_u_value = 0.0
    for fraction_1, r_value_1 in paths_1:
        for fraction_2, r_value_2 in paths_2:
            expected_u_value += (fraction_1 * fraction_2) / (r_value_1 + r_value_2)

    assert get_r_value_upper_limit(materials) == pytest.approx(1.0 / expected_u_value)


def test_no_mass_layer_contributes_its_r_value_to_both_limits():
    no_mass = EnergyMaterialNoMass("air_gap", r_value=0.18)
    materials = [_material("eps", 0.050, 0.035), no_mass]

    assert get_layer_paths(no_mass) == [(1.0, 0.18)]
    assert get_r_value_lower_limit(materials) == pytest.approx(0.050 / 0.035 + 0.18)
    assert get_r_value_upper_limit(materials) == pytest.approx(0.050 / 0.035 + 0.18)


def test_partly_populated_grid_reads_only_its_assigned_cells():
    hybrid_material = _material("hybrid", CAVITY_THICKNESS_M, INSULATION_CONDUCTIVITY)
    prop_ph = getattr(hybrid_material.properties, "ph")  # type: EnergyMaterialPhProperties
    prop_ph.divisions.set_column_widths([1.0, 1.0])
    prop_ph.divisions.set_row_heights([1.0])
    prop_ph.divisions.set_cell_material(0, 0, _material("stud", CAVITY_THICKNESS_M, STUD_CONDUCTIVITY))

    paths = get_layer_paths(hybrid_material)
    assert len(paths) == 1
    assert paths[0] == pytest.approx((1.0, CAVITY_THICKNESS_M / STUD_CONDUCTIVITY))


def test_grid_cell_with_no_conductivity_falls_back_to_the_host_material():
    hybrid_material = _material("hybrid", CAVITY_THICKNESS_M, INSULATION_CONDUCTIVITY)
    prop_ph = getattr(hybrid_material.properties, "ph")  # type: EnergyMaterialPhProperties
    prop_ph.divisions.set_column_widths([1.0, 1.0])
    prop_ph.divisions.set_row_heights([1.0])
    prop_ph.divisions.set_cell_material(0, 0, _material("stud", CAVITY_THICKNESS_M, STUD_CONDUCTIVITY))
    prop_ph.divisions.set_cell_material(1, 0, _material("void", CAVITY_THICKNESS_M, 0.0))

    paths = get_layer_paths(hybrid_material)
    assert len(paths) == 2
    assert paths[1] == pytest.approx((0.5, CAVITY_THICKNESS_M / INSULATION_CONDUCTIVITY))


def test_too_many_heat_flow_paths_raises():
    materials = [_framed_material([1.0, 1.0, 1.0, 1.0], [0.13, 0.05, 0.038, 0.03]) for _ in range(8)]

    with pytest.raises(TooManyHeatFlowPathsError):
        get_r_value_upper_limit(materials)

    assert 4**8 > MAX_HEAT_FLOW_PATHS


def test_equivalent_conductivity_reproduces_the_mean_of_limits():
    materials = _stud_wall_materials()
    total_thickness = sum(m.thickness for m in materials)
    r_value_mean = get_r_value_mean_of_limits(materials)

    equivalent_conductivity = get_equivalent_conductivity(r_value_mean, total_thickness)
    equivalent_layer = _material("equivalent", total_thickness, equivalent_conductivity)

    assert get_r_value_mean_of_limits([equivalent_layer]) == pytest.approx(r_value_mean)


def test_equivalent_conductivity_guards_non_positive_inputs():
    assert get_equivalent_conductivity(0.0, 0.150) == 0.0
    assert get_equivalent_conductivity(4.9, 0.0) == 0.0
