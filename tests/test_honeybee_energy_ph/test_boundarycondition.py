import pytest
from honeybee.altnumber import autocalculate

from honeybee_energy_ph.boundarycondition import PhAdditionalZone


def test_default_PhAdditionalZone():
    bc = PhAdditionalZone(identifier="test")
    assert bc.identifier == "test"
    assert bc.zone_id_num == 0
    assert bc.zone_name == ""
    assert bc.zone_type == ""
    assert bc.temperature_reduction_factor == 1.0
    assert bc.temperature == autocalculate


def test_PhAdditionalZone_to_from_dict_roundtrip_autocalculate_temperature():
    bc = PhAdditionalZone(
        identifier="bc_1",
        heat_transfer_coefficient=0.42,
        zone_name="Stair",
        zone_type="Ancillary",
        temperature_reduction_factor=0.85,
    )

    d = bc.to_dict()
    assert d["type"] == "PhAdditionalZone"
    assert d["temperature"] == autocalculate.to_dict()
    assert d["heat_transfer_coefficient"] == 0.42
    assert d["zone_name"] == "Stair"
    assert d["zone_type"] == "Ancillary"
    assert d["temperature_reduction_factor"] == 0.85

    bc2 = PhAdditionalZone.from_dict(d)
    assert bc2 is not bc
    assert bc2.to_dict() == d


def test_PhAdditionalZone_to_from_dict_roundtrip_float_temperature():
    bc = PhAdditionalZone(
        identifier="bc_2",
        temperature=22.5,
        heat_transfer_coefficient=0.1,
        zone_name="Garage",
        zone_type="Unconditioned",
        temperature_reduction_factor=0.6,
    )

    d = bc.to_dict()
    assert d["type"] == "PhAdditionalZone"
    assert d["temperature"] == 22.5

    bc2 = PhAdditionalZone.from_dict(d)
    assert bc2.to_dict() == d
    assert bc2.temperature == 22.5


def test_PhAdditionalZone_from_dict_missing_temperature_defaults_to_autocalculate():
    d = PhAdditionalZone(identifier="bc_3").to_dict()
    d.pop("temperature")

    bc2 = PhAdditionalZone.from_dict(d)
    assert bc2.temperature == autocalculate


def test_PhAdditionalZone_from_dict_wrong_type_raises():
    d = PhAdditionalZone(identifier="bc_4").to_dict()
    d["type"] = "NotPhAdditionalZone"
    with pytest.raises(AssertionError):
        PhAdditionalZone.from_dict(d)


def test_PhAdditionalZone_equality_and_hash():
    bc1 = PhAdditionalZone(
        identifier="same",
        temperature=autocalculate,
        heat_transfer_coefficient=0.25,
        zone_name="Zone",
        zone_type="Type",
        temperature_reduction_factor=0.9,
    )
    bc2 = PhAdditionalZone(
        identifier="same",
        temperature=autocalculate,
        heat_transfer_coefficient=0.25,
        zone_name="Zone",
        zone_type="Type",
        temperature_reduction_factor=0.9,
    )

    assert bc1 == bc2
    assert hash(bc1) == hash(bc2)

    bc3 = PhAdditionalZone(identifier="different")
    assert bc1 != bc3


# -----------------------------------------------------------------------------
# -- PHPP v10 custom-exposure factors (Issue #78)


def test_PhAdditionalZone_new_factors_default_to_none():
    bc = PhAdditionalZone(identifier="test")

    assert bc.heating_load_reduction_factor is None
    assert bc.cooling_demand_reduction_factor is None
    assert bc.cooling_load_reduction_factor is None
    assert bc.passive_cooling_reduction_factor is None
    assert bc.adjacent_zone_temperature_c is None


def test_PhAdditionalZone_unset_factors_resolve_to_the_heating_demand_factor():
    bc = PhAdditionalZone(identifier="test", temperature_reduction_factor=0.6)

    assert bc.heating_demand_factor == 0.6
    assert bc.heating_load_factor == 0.6
    assert bc.cooling_demand_factor == 0.6
    assert bc.cooling_load_factor == 0.6
    assert bc.passive_cooling_factor == 0.6


def test_PhAdditionalZone_set_factors_resolve_to_their_own_value():
    bc = PhAdditionalZone(
        identifier="test",
        temperature_reduction_factor=0.6,
        heating_load_reduction_factor=0.5,
        cooling_demand_reduction_factor=0.4,
        cooling_load_reduction_factor=0.3,
        passive_cooling_reduction_factor=0.2,
    )

    assert bc.heating_demand_factor == 0.6
    assert bc.heating_load_factor == 0.5
    assert bc.cooling_demand_factor == 0.4
    assert bc.cooling_load_factor == 0.3
    assert bc.passive_cooling_factor == 0.2


def test_PhAdditionalZone_a_zero_factor_is_kept_not_treated_as_unset():
    """PHI accepts factors below 0, so 0.0 must not collapse to the fallback."""
    bc = PhAdditionalZone(
        identifier="test",
        temperature_reduction_factor=0.6,
        cooling_demand_reduction_factor=0.0,
    )

    assert bc.cooling_demand_factor == 0.0


def test_PhAdditionalZone_round_trip_keeps_every_attribute():
    bc = PhAdditionalZone(
        identifier="bc_all",
        temperature=12.5,
        heat_transfer_coefficient=0.33,
        zone_name="Garage",
        zone_type="Unconditioned",
        temperature_reduction_factor=0.6,
        heating_load_reduction_factor=0.5,
        cooling_demand_reduction_factor=0.4,
        cooling_load_reduction_factor=0.3,
        passive_cooling_reduction_factor=0.2,
        adjacent_zone_temperature_c=8.0,
    )
    bc.zone_id_num = 7

    bc2 = PhAdditionalZone.from_dict(bc.to_dict())

    assert bc2.to_dict() == bc.to_dict()
    assert bc2 == bc
    assert bc2.zone_id_num == 7
    assert bc2.heating_load_reduction_factor == 0.5
    assert bc2.cooling_demand_reduction_factor == 0.4
    assert bc2.cooling_load_reduction_factor == 0.3
    assert bc2.passive_cooling_reduction_factor == 0.2
    assert bc2.adjacent_zone_temperature_c == 8.0


def test_PhAdditionalZone_legacy_dict_without_the_new_keys_still_loads():
    """HBJSON written before Issue #78 carries none of the five new keys."""
    legacy_dict = PhAdditionalZone(identifier="bc_old", temperature_reduction_factor=0.75).to_dict()
    for key in (
        "heating_load_reduction_factor",
        "cooling_demand_reduction_factor",
        "cooling_load_reduction_factor",
        "passive_cooling_reduction_factor",
        "adjacent_zone_temperature_c",
    ):
        legacy_dict.pop(key)

    bc = PhAdditionalZone.from_dict(legacy_dict)

    assert bc.temperature_reduction_factor == 0.75
    assert bc.heating_load_reduction_factor is None
    assert bc.adjacent_zone_temperature_c is None
    # -- An old model keeps behaving as it did: one factor, used everywhere.
    assert bc.cooling_load_factor == 0.75


def test_PhAdditionalZone_equality_distinguishes_the_new_factors():
    kwargs = {"identifier": "same", "temperature_reduction_factor": 0.6}
    bc1 = PhAdditionalZone(**kwargs)
    bc2 = PhAdditionalZone(cooling_demand_reduction_factor=0.4, **kwargs)

    assert bc1 != bc2
    assert hash(bc1) != hash(bc2)


def test_PhAdditionalZone_survives_a_full_hbjson_model_round_trip():
    """The acceptance criterion: the BC reaches a Face, is written into an
    HB-Model dict, and comes back with every attribute intact."""
    from honeybee.model import Model
    from honeybee.room import Room

    import honeybee_energy_ph._extend_honeybee_energy_ph  # noqa: F401  (registers the BC)

    bc = PhAdditionalZone(
        identifier="garage_bc",
        temperature=8.0,
        heat_transfer_coefficient=0.33,
        zone_name="Garage",
        zone_type="Unconditioned",
        temperature_reduction_factor=0.6,
        heating_load_reduction_factor=0.5,
        cooling_demand_reduction_factor=0.4,
        cooling_load_reduction_factor=0.3,
        passive_cooling_reduction_factor=0.2,
        adjacent_zone_temperature_c=8.0,
    )
    bc.zone_id_num = 7

    room = Room.from_box("r1", 5, 5, 3)
    wall = [f for f in room.faces if f.normal.z == 0][0]
    wall.boundary_condition = bc

    model = Model.from_dict(Model("m", rooms=[room]).to_dict())
    reloaded = [f for f in model.rooms[0].faces if f.identifier == wall.identifier][0].boundary_condition

    assert isinstance(reloaded, PhAdditionalZone)
    assert reloaded == bc
    assert reloaded.zone_id_num == 7
    assert reloaded.passive_cooling_factor == 0.2
