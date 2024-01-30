import pytest

from honeybee_energy_ph.properties.load import people


def test_ph_dwellings_set_num():
    obj1 = people.PhDwellings()
    assert obj1.num_dwellings == 0

    obj2 = people.PhDwellings(12)
    assert obj2.num_dwellings == 12


def test_ph_dwellings_round_trip():
    obj1 = people.PhDwellings()
    d1 = obj1.to_dict()
    obj2 = people.PhDwellings.from_dict(d1)

    assert obj2.to_dict() == d1


def test_ph_dwellings_duplicate():
    obj1 = people.PhDwellings()
    obj2 = obj1.duplicate()

    assert obj1 == obj2


def test_can_not_set_num_dwellings():
    obj1 = people.PhDwellings()
    with pytest.raises(Exception):
        obj1.num_dwellings = 12


# -------------------------------------------------------


def test_people_round_trip():
    fake_host = 1
    obj = people.PeoplePhProperties(_host=fake_host)
    d1 = obj.to_dict()
    obj2 = people.PeoplePhProperties.from_dict(d1["ph"], fake_host)

    assert obj2.to_dict() == d1


def test_people_duplicate():
    fake_host = 1
    obj1 = people.PeoplePhProperties(_host=fake_host)
    obj2 = obj1.duplicate()

    assert obj1 == obj2


# -------------------------------------------------------
# Backwards compatibility?


def test_with_old_version_attributes():
    fake_host = 1
    obj = people.PeoplePhProperties(_host=fake_host)
    d1 = obj.to_dict()

    # remove the 'dwellings' from the dict
    # in older versions this attribute was not there
    # so make sure that dicts without it can still be
    # de-serialized and just use a default value
    obj_dict = d1["ph"]
    del obj_dict["dwellings"]

    # Even if that key doesn't exist, it should still de-serialize
    # and just set the dwellings to 0
    obj2 = people.PeoplePhProperties.from_dict(d1["ph"], fake_host)
    assert hasattr(obj2, "dwellings")
    assert obj2.dwellings.num_dwellings == 0
