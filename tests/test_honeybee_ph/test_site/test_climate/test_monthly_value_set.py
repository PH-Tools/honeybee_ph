from honeybee_ph import site


def test_basic_Climate_MonthlyValueSet():
    monthly_climate_collection = site.Climate_MonthlyValueSet()

    assert "january" in vars(monthly_climate_collection).keys()
    assert "july" in vars(monthly_climate_collection).keys()
    assert "december" in vars(monthly_climate_collection).keys()

    assert monthly_climate_collection


def test_set_Climate_MonthlyValueSet_values():
    monthly_climate_collection = site.Climate_MonthlyValueSet()

    monthly_climate_collection.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert getattr(monthly_climate_collection, "january") == 1
    assert getattr(monthly_climate_collection, "july") == 7
    assert getattr(monthly_climate_collection, "december") == 12


def test_Climate_MonthlyValueSet_serialization_empty():
    monthly_climate_collection = site.Climate_MonthlyValueSet()
    d = monthly_climate_collection.to_dict()
    new_obj = site.Climate_MonthlyValueSet.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_MonthlyValueSet_serialization_with_user_data():
    monthly_climate_collection = site.Climate_MonthlyValueSet()
    monthly_climate_collection.user_data["test_key"] = "test_value"
    d = monthly_climate_collection.to_dict()
    new_obj = site.Climate_MonthlyValueSet.from_dict(d)

    assert "test_key" in new_obj.user_data
    assert new_obj.to_dict() == d


def test_Climate_MonthlyValueSet_serialization_with_values():
    monthly_climate_collection = site.Climate_MonthlyValueSet()
    monthly_climate_collection.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = site.Climate_MonthlyValueSet.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_MonthlyValueSet_deserialization_when_identifier_is_missing():
    """when deserializing from dict, if identifier is missing, (old hbjson files))"""
    obj_1 = site.Climate_MonthlyValueSet()
    d1 = obj_1.to_dict()
    d1.pop("identifier", None)
    obj_2 = site.Climate_MonthlyValueSet.from_dict(d1)

    assert obj_2.identifier != obj_1.identifier
    assert isinstance(obj_2, site.Climate_MonthlyValueSet)
    assert obj_1.to_dict() != obj_2.to_dict()


def test_Climate_MonthlyValueSet_duplicate():
    monthly_climate_value_set = site.Climate_MonthlyValueSet()
    monthly_climate_value_set.user_data["test_key"] = "test_value"
    monthly_climate_value_set.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = monthly_climate_value_set.duplicate()

    assert new_obj.user_data == monthly_climate_value_set.user_data
    assert new_obj.to_dict() == monthly_climate_value_set.to_dict()
    assert new_obj.identifier == monthly_climate_value_set.identifier
    assert isinstance(new_obj, site.Climate_MonthlyValueSet)
    assert isinstance(new_obj, site._base._Base)
    assert "test_key" in new_obj.user_data

    assert new_obj.values == monthly_climate_value_set.values
    assert new_obj.january == monthly_climate_value_set.january
    assert new_obj.july == monthly_climate_value_set.july
    assert new_obj.december == monthly_climate_value_set.december
