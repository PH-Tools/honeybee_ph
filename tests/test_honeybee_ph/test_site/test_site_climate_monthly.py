from honeybee_ph import site


def test_basic_climate_monthly_collection():
    monthly_climate_collection = site.Climate_MonthlyValueSet()

    assert 'january' in vars(monthly_climate_collection).keys()
    assert 'july' in vars(monthly_climate_collection).keys()
    assert 'december' in vars(monthly_climate_collection).keys()

    assert monthly_climate_collection


def test_set_climate_monthly_collection_values():
    monthly_climate_collection = site.Climate_MonthlyValueSet()

    monthly_climate_collection.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert monthly_climate_collection.january == 1
    assert monthly_climate_collection.july == 7
    assert monthly_climate_collection.december == 12


def test_climate_monthly_collection_serialization_empty():
    monthly_climate_collection = site.Climate_MonthlyValueSet()
    d = monthly_climate_collection.to_dict()
    new_obj = site.Climate_MonthlyValueSet.from_dict(d)

    assert new_obj.to_dict() == d

def test_climate_monthly_collection_serialization_with_user_data():
    monthly_climate_collection = site.Climate_MonthlyValueSet()
    monthly_climate_collection.user_data["test_key"] = "test_value"
    d = monthly_climate_collection.to_dict()
    new_obj = site.Climate_MonthlyValueSet.from_dict(d)

    assert "test_key" in new_obj.user_data
    assert new_obj.to_dict() == d


def test_climate_monthly_collection_serialization_with_values():
    monthly_climate_collection = site.Climate_MonthlyValueSet()
    monthly_climate_collection.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = site.Climate_MonthlyValueSet.from_dict(d)

    assert new_obj.to_dict() == d
