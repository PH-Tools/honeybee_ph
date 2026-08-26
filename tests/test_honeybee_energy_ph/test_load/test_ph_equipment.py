from honeybee_energy.lib.schedules import schedule_by_identifier
from pytest import approx

from honeybee_energy_ph.load import ph_equipment
from honeybee_ph_standards.programtypes.default_elec_equip import ph_default_equip

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


# -- IHG Utilization Factor defaults


def test_ihg_utilization_factor_defaults():
    """Each appliance type should have the correct PHPP availability factor."""
    assert ph_equipment.PhDishwasher().ihg_utilization_factor == 0.30
    assert ph_equipment.PhClothesWasher().ihg_utilization_factor == 0.30
    assert ph_equipment.PhClothesDryer().ihg_utilization_factor == 0.70
    assert ph_equipment.PhCooktop().ihg_utilization_factor == 0.50
    assert ph_equipment.PhRefrigerator().ihg_utilization_factor == 1.0
    assert ph_equipment.PhFreezer().ihg_utilization_factor == 1.0
    assert ph_equipment.PhFridgeFreezer().ihg_utilization_factor == 1.0
    assert ph_equipment.PhPhiusMEL().ihg_utilization_factor == 1.0
    assert ph_equipment.PhPhiusLightingInterior().ihg_utilization_factor == 1.0
    assert ph_equipment.PhPhiusLightingExterior().ihg_utilization_factor == 1.0
    assert ph_equipment.PhPhiusLightingGarage().ihg_utilization_factor == 1.0
    assert ph_equipment.PhCustomAnnualElectric().ihg_utilization_factor == 1.0
    assert ph_equipment.PhCustomAnnualLighting().ihg_utilization_factor == 1.0
    assert ph_equipment.PhCustomAnnualMEL().ihg_utilization_factor == 1.0
    assert ph_equipment.PhElevatorHydraulic().ihg_utilization_factor == 1.0
    assert ph_equipment.PhElevatorGearedTraction().ihg_utilization_factor == 1.0
    assert ph_equipment.PhElevatorGearlessTraction().ihg_utilization_factor == 1.0


def test_ihg_utilization_factor_in_to_dict():
    """The ihg_utilization_factor should appear in serialized output."""
    e = ph_equipment.PhCooktop()
    d = e.to_dict()
    assert d["ihg_utilization_factor"] == 0.50


def test_ihg_utilization_factor_round_trip():
    """The ihg_utilization_factor should survive a to_dict/from_dict cycle."""
    e1 = ph_equipment.PhDishwasher()
    e1.ihg_utilization_factor = 0.45
    d = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d)
    assert e2.ihg_utilization_factor == 0.45


def test_ihg_utilization_factor_backwards_compat():
    """Old serialized data without ihg_utilization_factor should default to 1.0."""
    e = ph_equipment.PhCustomAnnualElectric()
    d = e.to_dict()
    del d["ihg_utilization_factor"]
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d)
    assert e2.ihg_utilization_factor == 1.0


# -- Reference Quantity defaults


def _all_equipment_subclasses():
    """Every concrete PhEquipment subclass defined in the ph_equipment module."""
    return [
        obj
        for obj in vars(ph_equipment).values()
        if isinstance(obj, type)
        and issubclass(obj, ph_equipment.PhEquipment)
        and obj is not ph_equipment.PhEquipment
        and obj.__module__ == ph_equipment.__name__
    ]


def test_reference_quantity_defaults():
    """Each equipment type should carry the correct WUFI 'Reference Quantity' selector.

    A bare constructor must produce the same value as one built from the standards
    dict -- the six Phius-MF builders once relied on the base-class value and silently
    exported 2 ("Zone occupants") on every custom MEL and lighting device.
    """
    assert ph_equipment.PhDishwasher().reference_quantity == 1
    assert ph_equipment.PhClothesWasher().reference_quantity == 1
    assert ph_equipment.PhClothesDryer().reference_quantity == 1
    assert ph_equipment.PhCooktop().reference_quantity == 1
    assert ph_equipment.PhRefrigerator().reference_quantity == 4
    assert ph_equipment.PhFreezer().reference_quantity == 4
    assert ph_equipment.PhFridgeFreezer().reference_quantity == 4
    assert ph_equipment.PhPhiusMEL().reference_quantity == 3
    assert ph_equipment.PhPhiusLightingInterior().reference_quantity == 6
    assert ph_equipment.PhPhiusLightingExterior().reference_quantity == 6
    assert ph_equipment.PhPhiusLightingGarage().reference_quantity == 2
    assert ph_equipment.PhCustomAnnualElectric().reference_quantity == 5
    assert ph_equipment.PhCustomAnnualLighting().reference_quantity == 5
    assert ph_equipment.PhCustomAnnualMEL().reference_quantity == 5
    assert ph_equipment.PhElevatorHydraulic().reference_quantity == 5
    assert ph_equipment.PhElevatorGearedTraction().reference_quantity == 5
    assert ph_equipment.PhElevatorGearlessTraction().reference_quantity == 5


def test_every_equipment_subclass_declares_its_own_reference_quantity():
    """No subclass may inherit DEFAULT_REFERENCE_QUANTITY from PhEquipment.

    Inheriting it is always a mistake: the base value is a placeholder, not a sensible
    fallback. This guard is what stops the defect coming back when a new equipment
    class is added.
    """
    missing = [cls.__name__ for cls in _all_equipment_subclasses() if "DEFAULT_REFERENCE_QUANTITY" not in vars(cls)]
    assert missing == [], "PhEquipment subclasses missing DEFAULT_REFERENCE_QUANTITY: {}".format(missing)


def test_reference_quantity_matches_the_standards_data():
    """The class defaults and 'ph_default_equip' must not drift apart.

    PHI and PHIUS agree on reference_quantity for every entry, which is why the value
    belongs to the class. Both representations are public, so both have to stay true.
    """
    for cls in _all_equipment_subclasses():
        defaults = ph_default_equip.get(cls.__name__)
        if defaults is None:
            continue  # -- the elevators have no standards entry
        for standard in ("PHI", "PHIUS"):
            assert (
                defaults[standard]["reference_quantity"] == cls.DEFAULT_REFERENCE_QUANTITY
            ), "{}: ph_default_equip['{}'] says {} but the class says {}".format(
                cls.__name__,
                standard,
                defaults[standard]["reference_quantity"],
                cls.DEFAULT_REFERENCE_QUANTITY,
            )


def test_reference_quantity_survives_a_round_trip():
    """An explicitly-set reference_quantity must not be reset by from_dict."""
    e1 = ph_equipment.PhCustomAnnualMEL()
    e1.reference_quantity = 1
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(e1.to_dict())
    assert e2.reference_quantity == 1


# -- Default factories hand out independent objects


def test_default_factories_return_independent_objects():
    """Two calls must not return the same object.

    They used to: the factories cached one instance per class and handed that same
    object to every caller for the life of the process, so anything one caller wrote
    to a default was visible to every later caller -- across Grasshopper solutions and
    across .3dm files opened in one Rhino session.
    """
    for cls in _all_equipment_subclasses():
        if cls.__name__ not in ph_default_equip:
            continue  # -- the elevators have no standards entry
        for factory_name in ("phi_default", "phius_default"):
            a = getattr(cls, factory_name)()
            b = getattr(cls, factory_name)()
            assert a is not b, "{}.{}() handed out the same object twice".format(cls.__name__, factory_name)


def test_mutating_a_default_does_not_affect_the_next_one():
    """A caller writing to a default must not corrupt it for the next caller."""
    a = ph_equipment.PhCooktop.phius_default()
    original_demand = a.energy_demand
    a.energy_demand = 999.0
    a.display_name = "MUTATED BY CALLER A"
    a.comment = "MUTATED BY CALLER A"

    b = ph_equipment.PhCooktop.phius_default()
    assert b.energy_demand == original_demand
    assert b.display_name != "MUTATED BY CALLER A"
    assert b.comment == "default"


def test_default_factories_keep_a_stable_identifier():
    """The identifier must stay the same across calls -- this is load-bearing.

    PHX keys each PhxZone's device collection by the device identifier and upserts, so
    the N per-room devices the Phius MF builders create collapse to one device per zone
    and the N zones sum back to the building total. Handing every room a distinct
    identifier would multiply the exported energy by the room count.
    """
    for cls in _all_equipment_subclasses():
        if cls.__name__ not in ph_default_equip:
            continue  # -- the elevators have no standards entry
        for factory_name in ("phi_default", "phius_default"):
            a = getattr(cls, factory_name)()
            b = getattr(cls, factory_name)()
            assert a.identifier == b.identifier, "{}.{}() re-keyed the default".format(cls.__name__, factory_name)


def test_phi_and_phius_defaults_are_distinct():
    """The two standards must not collapse onto one cached object or one identifier."""
    phi = ph_equipment.PhDishwasher.phi_default()
    phius = ph_equipment.PhDishwasher.phius_default()
    assert phi.identifier != phius.identifier


# -- PhEquipment.duplicate()


def test_duplicate_returns_an_independent_object():
    e1 = ph_equipment.PhDishwasher()
    e1.energy_demand = 123.4
    e2 = e1.duplicate()

    assert e1 is not e2
    e2.energy_demand = 0.0
    assert e1.energy_demand == 123.4


def test_duplicate_preserves_the_identifier():
    """duplicate() deliberately does NOT re-key. See decision 0008."""
    e1 = ph_equipment.PhCustomAnnualMEL()
    assert e1.duplicate().identifier == e1.identifier


def test_duplicate_preserves_every_serialized_attribute():
    """A duplicate must be indistinguishable from its original once serialized."""
    for cls in _all_equipment_subclasses():
        e1 = cls()
        assert e1.duplicate().to_dict() == e1.to_dict(), "{}.duplicate() lost an attribute".format(cls.__name__)


def test_duplicate_does_not_share_nested_type_objects():
    """The enum-style sub-objects must be copies too, not shared references."""
    e1 = ph_equipment.PhCooktop()
    e2 = e1.duplicate()
    assert e1.cooktop_type is not e2.cooktop_type
    assert e1.cooktop_type.value == e2.cooktop_type.value


def test_duplicate_takes_a_new_host():
    e1 = ph_equipment.PhDishwasher()
    new_host = object()
    assert e1.duplicate(new_host=new_host).host is new_host


def test_duplicating_a_collection_copies_the_equipment():
    """Duplicating a Room's equipment collection must not share the equipment objects."""
    collection = ph_equipment.PhEquipmentCollection()
    equip = ph_equipment.PhDishwasher.phius_default()
    collection.add_equipment(equip)

    duplicated = collection.duplicate()

    assert list(duplicated.keys()) == list(collection.keys())
    assert duplicated[equip.identifier] is not collection[equip.identifier]
    assert duplicated[equip.identifier].to_dict() == collection[equip.identifier].to_dict()
