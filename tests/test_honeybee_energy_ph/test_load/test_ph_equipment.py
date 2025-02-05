from honeybee_energy.lib.schedules import schedule_by_identifier
from pytest import approx

from honeybee_energy_ph.load import ph_equipment

# -- Basics


def test_PhDishwasher_round_trip():
    e1 = ph_equipment.PhDishwasher()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhClothesWasher_round_trip():
    e1 = ph_equipment.PhClothesWasher()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhClothesDryer_round_trip():
    e1 = ph_equipment.PhClothesDryer()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhRefrigerator_round_trip():
    e1 = ph_equipment.PhRefrigerator()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhFreezer_round_trip():
    e1 = ph_equipment.PhFreezer()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhFridgeFreezer_round_trip():
    e1 = ph_equipment.PhFridgeFreezer()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhCooktop_round_trip():
    e1 = ph_equipment.PhCooktop()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


# -- Phius, MEL


def test_PhPhiusMEL_round_trip():
    e1 = ph_equipment.PhPhiusMEL()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhPhiusLightingInterior_round_trip():
    e1 = ph_equipment.PhPhiusLightingInterior()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhPhiusLightingExterior_round_trip():
    e1 = ph_equipment.PhPhiusLightingExterior()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1
    assert e2.in_conditioned_space == False


def test_PhPhiusLightingGarage_round_trip():
    e1 = ph_equipment.PhPhiusLightingGarage()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1
    assert e2.in_conditioned_space == False


def test_PhCustomAnnualElectric_round_trip():
    e1 = ph_equipment.PhCustomAnnualElectric()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhCustomAnnualLighting_round_trip():
    e1 = ph_equipment.PhCustomAnnualLighting()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhCustomAnnualMEL_round_trip():
    e1 = ph_equipment.PhCustomAnnualMEL()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


# --- Elevators


def test_PhElevatorHydraulic_round_trip():
    e1 = ph_equipment.PhElevatorHydraulic()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhElevatorGearedTraction_round_trip():
    e1 = ph_equipment.PhElevatorGearedTraction()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


def test_PhElevatorGearlessTraction_round_trip():
    e1 = ph_equipment.PhElevatorGearlessTraction()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


# -- Defaults


def _test_defaults(_type):
    phi_equip = _type.phi_default()
    assert phi_equip.comment == "default"

    d = phi_equip.to_dict()
    e = ph_equipment.PhEquipmentBuilder.from_dict(d)
    assert e.to_dict() == d

    phius_equip = _type.phius_default()
    assert phius_equip.comment == "default"

    d = phius_equip.to_dict()
    e = ph_equipment.PhEquipmentBuilder.from_dict(d)
    assert e.to_dict() == d


def test_dishwasher_default():
    _test_defaults(ph_equipment.PhDishwasher)


def test_clothes_washer_default():
    _test_defaults(ph_equipment.PhClothesWasher)


def test_clothes_dryer_default():
    _test_defaults(ph_equipment.PhClothesDryer)


def test_refrigerator_default():
    _test_defaults(ph_equipment.PhRefrigerator)


def test_freezer_default():
    _test_defaults(ph_equipment.PhFreezer)


def test_fridge_freezer_default():
    _test_defaults(ph_equipment.PhFridgeFreezer)


def test_cooktop_default():
    _test_defaults(ph_equipment.PhCooktop)


def test_phius_mel_default():
    _test_defaults(ph_equipment.PhPhiusMEL)


def test_phius_lighting_interior_default():
    _test_defaults(ph_equipment.PhPhiusLightingInterior)


def test_phius_lighting_exterior_default():
    _test_defaults(ph_equipment.PhPhiusLightingExterior)


def test_phius_lighting_garage_default():
    _test_defaults(ph_equipment.PhPhiusLightingGarage)


def test_custom_annual_electric_default():
    _test_defaults(ph_equipment.PhCustomAnnualElectric)


def test_custom_annual_lighting_default():
    _test_defaults(ph_equipment.PhCustomAnnualLighting)


def test_custom_annual_mel_default():
    _test_defaults(ph_equipment.PhCustomAnnualMEL)


# -- Annual Energy kWH


def test_dishwasher_annual_kWh():
    e = ph_equipment.PhDishwasher.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(269)


def test_clothes_washer_annual_kWh():
    e = ph_equipment.PhClothesWasher.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(120)


def test_clothes_dryer_annual_kWh():
    e = ph_equipment.PhClothesDryer.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(405.657336726039)


def test_refrigerator_annual_kWh():
    e = ph_equipment.PhRefrigerator.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(365.0)


def test_freezer_annual_kWh():
    e = ph_equipment.PhFreezer.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(394.0175)


def test_fridge_freezer_annual_kWh():
    e = ph_equipment.PhFridgeFreezer.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(445.3)


def test_cooktop_annual_kWh():
    e = ph_equipment.PhCooktop.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(300.0)


def test_phius_mel_annual_kWh():
    e = ph_equipment.PhPhiusMEL.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(1168.8)


def test_phius_lighting_interior_annual_kWh():
    e = ph_equipment.PhPhiusLightingInterior.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(417.881081081081)


def test_phius_lighting_exterior_annual_kWh():
    e = ph_equipment.PhPhiusLightingExterior.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(30.0)


def test_phius_lighting_garage_annual_kWh():
    e = ph_equipment.PhPhiusLightingGarage.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(20.0)


def test_custom_annual_electric_annual_kWh():
    e = ph_equipment.PhCustomAnnualElectric.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(0)


def test_custom_annual_lighting_annual_kWh():
    e = ph_equipment.PhCustomAnnualLighting.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(0)


def test_custom_annual_mel_annual_kWh():
    e = ph_equipment.PhCustomAnnualMEL.phius_default()
    annual_kwh = e.annual_energy_kWh(
        **{
            "_num_occupants": 3,
            "_num_bedrooms": 2,
            "_floor_area_ft2": 1_000,
        }
    )
    assert annual_kwh == approx(0)


# -- Annual Average Wattage


def test_average_wattage():
    d = {
        "_num_occupants": 3,
        "_num_bedrooms": 2,
        "_floor_area_ft2": 1_000,
        "_schedule": schedule_by_identifier("Always On"),
    }
    e = ph_equipment.PhDishwasher.phius_default()
    assert e.annual_avg_wattage(**d) == approx(30.707762557077626)

    e = ph_equipment.PhClothesWasher.phius_default()
    assert e.annual_avg_wattage(**d) == approx(13.698630136986301)

    e = ph_equipment.PhClothesDryer.phius_default()
    assert e.annual_avg_wattage(**d) == approx(46.30791515137431)

    e = ph_equipment.PhRefrigerator.phius_default()
    assert e.annual_avg_wattage(**d) == approx(41.666666666666664)

    e = ph_equipment.PhFreezer.phius_default()
    assert e.annual_avg_wattage(**d) == approx(44.979166666666664)

    e = ph_equipment.PhFridgeFreezer.phius_default()
    assert e.annual_avg_wattage(**d) == approx(50.833333333333336)

    e = ph_equipment.PhCooktop.phius_default()
    assert e.annual_avg_wattage(**d) == approx(34.24657534246575)

    e = ph_equipment.PhPhiusMEL.phius_default()
    assert e.annual_avg_wattage(**d) == approx(133.42465753424656)

    e = ph_equipment.PhPhiusLightingInterior.phius_default()
    assert e.annual_avg_wattage(**d) == approx(47.70331975811428)

    e = ph_equipment.PhPhiusLightingExterior.phius_default()
    assert e.annual_avg_wattage(**d) == approx(3.4246575342465753)

    e = ph_equipment.PhPhiusLightingGarage.phius_default()
    assert e.annual_avg_wattage(**d) == approx(2.28310502283105)

    e = ph_equipment.PhCustomAnnualElectric.phius_default()
    assert e.annual_avg_wattage(**d) == approx(0)

    e = ph_equipment.PhCustomAnnualLighting.phius_default()
    assert e.annual_avg_wattage(**d) == approx(0)

    e = ph_equipment.PhCustomAnnualMEL.phius_default()
    assert e.annual_avg_wattage(**d) == approx(0)
