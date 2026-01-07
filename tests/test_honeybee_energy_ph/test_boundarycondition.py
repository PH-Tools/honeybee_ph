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
