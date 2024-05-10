import honeybee_ph.site


def test_default_Climate_MonthlyRadiationCollection():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    assert "january" in vars(monthly_climate_collection.north).keys()
    assert "july" in vars(monthly_climate_collection.south).keys()
    assert "october" in vars(monthly_climate_collection.east).keys()
    assert "december" in vars(monthly_climate_collection.west).keys()
    assert monthly_climate_collection


def test_Climate_MonthlyRadiationCollection_with_custom_north_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.north.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(d)
    assert new_obj.to_dict() == d


def test_Climate_MonthlyRadiationCollection_with_custom_north_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.north.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.north.values == monthly_climate_collection.north.values


def test_Climate_MonthlyRadiationCollection_with_custom_south_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.south.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(d)
    assert new_obj.to_dict() == d


def test_Climate_MonthlyRadiationCollection_with_custom_south_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.south.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.south.values == monthly_climate_collection.south.values


def test_Climate_MonthlyRadiationCollection_with_custom_east_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.east.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(d)
    assert new_obj.to_dict() == d


def test_Climate_MonthlyRadiationCollection_with_custom_east_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.east.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.east.values == monthly_climate_collection.east.values


def test_Climate_MonthlyRadiationCollection_with_custom_west_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.west.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(d)
    assert new_obj.to_dict() == d


def test_Climate_MonthlyRadiationCollection_with_custom_west_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyRadiationCollection()
    monthly_climate_collection.west.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyRadiationCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.west.values == monthly_climate_collection.west.values
