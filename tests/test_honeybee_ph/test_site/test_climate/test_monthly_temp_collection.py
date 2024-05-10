import honeybee_ph.site


def test_default_Climate_MonthlyTempCollection():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    assert "january" in vars(monthly_climate_collection.air_temps).keys()
    assert "july" in vars(monthly_climate_collection.dewpoints).keys()
    assert "october" in vars(monthly_climate_collection.ground_temps).keys()
    assert "december" in vars(monthly_climate_collection.sky_temps).keys()

    assert monthly_climate_collection


def test_Climate_MonthlyTempCollection_with_custom_air_temps_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.air_temps.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_MonthlyTempCollection_with_custom_air_temps_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.air_temps.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.air_temps.values == monthly_climate_collection.air_temps.values


def test_Climate_MonthlyTempCollection_with_custom_dewpoints_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.dewpoints.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_MonthlyTempCollection_with_custom_dewpoints_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.dewpoints.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.dewpoints.values == monthly_climate_collection.dewpoints.values


def test_Climate_MonthlyTempCollection_with_custom_ground_temps_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.ground_temps.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_MonthlyTempCollection_with_custom_ground_temps_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.ground_temps.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.ground_temps.values == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def test_Climate_MonthlyTempCollection_with_custom_sky_temps_to_from_dict_roundtrip():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.sky_temps.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = monthly_climate_collection.to_dict()
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_MonthlyTempCollection_with_custom_sky_temps_duplicate():
    monthly_climate_collection = honeybee_ph.site.Climate_MonthlyTempCollection()

    monthly_climate_collection.sky_temps.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_obj = honeybee_ph.site.Climate_MonthlyTempCollection.from_dict(monthly_climate_collection.to_dict())
    assert new_obj.sky_temps.values == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
