import pytest
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.material.opaque import EnergyMaterial

from honeybee_energy_ph.properties.construction import opaque


def test_default_opaque_construction_properties_dict_round_trip():
    s1 = opaque.OpaqueConstructionPhProperties("host")
    d1 = s1.to_dict()
    s2 = opaque.OpaqueConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_custom_opaque_construction_properties_dict_round_trip():
    s1 = opaque.OpaqueConstructionPhProperties("host")
    s1.id_num = 11223
    d1 = s1.to_dict()
    s2 = opaque.OpaqueConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_default_opaque_construction_properties_duplicate():
    s1 = opaque.OpaqueConstructionPhProperties("host")
    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_custom_opaque_construction_properties__wrong_type_from_dict():
    wrong_dict = {
        "type": "not_allowed_type",
    }
    with pytest.raises(opaque.OpaqueConstructionPhProperties_FromDictError):
        s1 = opaque.OpaqueConstructionPhProperties.from_dict(wrong_dict, None)


# -----------------------------------------------------------------------------
# -- ISO 6946 limits (issue #116)


def _material(_name, _thickness, _conductivity):
    # type: (str, float, float) -> EnergyMaterial
    return EnergyMaterial(_name, thickness=_thickness, conductivity=_conductivity, density=999, specific_heat=999)


def _stud_cavity_material():
    # type: () -> EnergyMaterial
    """A 38mm wood stud at 406.4mm o.c. in 140mm of mineral wool."""
    widths = [38.0, 406.4 - 38.0]
    conductivities = [0.130, 0.038]
    area_weighted = sum(w * k for w, k in zip(widths, conductivities)) / sum(widths)

    hybrid_material = _material("stud_cavity", 0.140, area_weighted)
    prop_ph = getattr(hybrid_material.properties, "ph")
    prop_ph.divisions.set_column_widths(widths)
    prop_ph.divisions.set_row_heights([1.0])
    for column_num, conductivity in enumerate(conductivities):
        prop_ph.divisions.set_cell_material(column_num, 0, _material("cell", 0.140, conductivity))
    return hybrid_material


def _framed_wall():
    # type: () -> OpaqueConstruction
    return OpaqueConstruction(
        "framed_wall",
        [
            _material("gypsum", 0.0127, 0.16),
            _stud_cavity_material(),
            _material("osb", 0.0127, 0.13),
            _material("eps", 0.050, 0.035),
        ],
    )


def test_uniform_construction_limits_match_the_honeybee_r_value():
    construction = OpaqueConstruction(
        "uniform_wall", [_material("gypsum", 0.0127, 0.16), _material("eps", 0.050, 0.035)]
    )
    prop_ph = getattr(construction.properties, "ph")

    assert prop_ph.r_value_upper_limit == pytest.approx(construction.r_value)
    assert prop_ph.r_value_lower_limit == pytest.approx(construction.r_value)
    assert prop_ph.r_value_mean_of_limits == pytest.approx(construction.r_value)
    assert prop_ph.u_value_mean_of_limits == pytest.approx(construction.u_value)
    assert prop_ph.iso_6946_error_percent == pytest.approx(0.0)


def test_framed_construction_limits():
    construction = _framed_wall()
    prop_ph = getattr(construction.properties, "ph")

    assert prop_ph.r_value_upper_limit == pytest.approx(4.849157, abs=1e-6)
    assert prop_ph.r_value_lower_limit == pytest.approx(4.609778, abs=1e-6)
    assert prop_ph.r_value_mean_of_limits == pytest.approx(4.729468, abs=1e-6)
    assert prop_ph.iso_6946_error_percent == pytest.approx(2.531, abs=1e-3)

    # -- The lower limit is what a plain honeybee series-sum of the layers reports.
    assert prop_ph.r_value_lower_limit == pytest.approx(construction.r_value)
    assert prop_ph.r_value_mean_of_limits > construction.r_value


def test_equivalent_conductivity_reproduces_the_mean_of_limits():
    construction = _framed_wall()
    prop_ph = getattr(construction.properties, "ph")

    equivalent_construction = OpaqueConstruction(
        "equivalent_wall",
        [_material("equivalent", construction.thickness, prop_ph.equivalent_conductivity_mean_of_limits)],
    )

    assert equivalent_construction.u_value == pytest.approx(prop_ph.u_value_mean_of_limits, abs=1e-6)


def test_iso_6946_limits_without_a_host_raise():
    prop_ph = opaque.OpaqueConstructionPhProperties(None)

    for property_name in (
        "r_value_upper_limit",
        "r_value_lower_limit",
        "r_value_mean_of_limits",
        "u_value_mean_of_limits",
        "iso_6946_error_percent",
        "equivalent_conductivity_mean_of_limits",
    ):
        with pytest.raises(opaque.OpaqueConstructionPhProperties_NoHostError):
            getattr(prop_ph, property_name)


def test_limits_survive_an_hbjson_round_trip():
    construction = _framed_wall()
    construction_2 = OpaqueConstruction.from_dict(construction.to_dict())
    prop_ph_1 = getattr(construction.properties, "ph")
    prop_ph_2 = getattr(construction_2.properties, "ph")

    assert prop_ph_2.r_value_upper_limit == pytest.approx(prop_ph_1.r_value_upper_limit)
    assert prop_ph_2.r_value_lower_limit == pytest.approx(prop_ph_1.r_value_lower_limit)
    assert prop_ph_2.u_value_mean_of_limits == pytest.approx(prop_ph_1.u_value_mean_of_limits)
