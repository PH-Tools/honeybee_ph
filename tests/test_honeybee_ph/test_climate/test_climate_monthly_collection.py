import honeybee_ph.climate


def test_basic_climate_monthly_collection():
    monthly_climate_collection = honeybee_ph.climate.Climate_MonthlyValueCollection()

    assert len(vars(monthly_climate_collection)) == 12

    for _ in vars(monthly_climate_collection):
        assert getattr(monthly_climate_collection, _) == 0

    assert 'january' in vars(monthly_climate_collection)
    assert 'july' in vars(monthly_climate_collection)
    assert 'december' in vars(monthly_climate_collection)

    assert monthly_climate_collection


def test_set_climate_monthly_collection_values():
    monthly_climate_collection = honeybee_ph.climate.Climate_MonthlyValueCollection()

    monthly_climate_collection.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert monthly_climate_collection.january == 1
    assert monthly_climate_collection.july == 7
    assert monthly_climate_collection.december == 12


def test_climate_monthly_collection_serialization_empty():
    monthly_climate_collection = honeybee_ph.climate.Climate_MonthlyValueCollection()
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.climate.Climate_MonthlyValueCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_climate_monthly_collection_serialization_with_values():
    monthly_climate_collection = honeybee_ph.climate.Climate_MonthlyValueCollection()
    monthly_climate_collection.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.climate.Climate_MonthlyValueCollection.from_dict(d)

    assert new_obj.to_dict() == d
