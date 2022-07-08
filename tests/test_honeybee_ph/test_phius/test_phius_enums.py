import pytest
import honeybee_ph.phius
from honeybee_ph_utils.enumerables import ValueNotAllowedError


def test_building_status_set_by_value():
    status = honeybee_ph.phius.PhiusBuildingStatus('1-IN_PLANNING')
    assert status.value == '1-IN_PLANNING'
    assert status.number == 1

    status.value = '2-UNDER_CONSTRUCTION'
    assert status.value == '2-UNDER_CONSTRUCTION'
    assert status.number == 2

    status.value = '3-COMPLETE'
    assert status.value == '3-COMPLETE'
    assert status.number == 3


def test_building_status_set_by_number():
    status = honeybee_ph.phius.PhiusBuildingStatus('1-IN_PLANNING')
    status.value = 1
    assert status.value == '1-IN_PLANNING'
    assert status.number == 1

    status.value = 2
    assert status.value == '2-UNDER_CONSTRUCTION'
    assert status.number == 2

    status.value = 3
    assert status.value == '3-COMPLETE'
    assert status.number == 3


def test_building_status_not_allowed():
    status = honeybee_ph.phius.PhiusBuildingStatus('1-IN_PLANNING')
    assert status.value == '1-IN_PLANNING'
    assert status.number == 1

    with pytest.raises(ValueNotAllowedError):
        status.value = 'NOT_ALLOWED'
    with pytest.raises(ValueNotAllowedError):
        status.value = len(status.allowed) + 1

    assert status.value == '1-IN_PLANNING'
    assert status.number == 1


def test_building_status_serialization():
    status = honeybee_ph.phius.PhiusBuildingStatus()
    d = status.to_dict()
    new_obj = honeybee_ph.phius.PhiusBuildingStatus.from_dict(d)

    assert new_obj.to_dict() == d


def test_building_bldg_type_set_by_value():
    bldg_type = honeybee_ph.phius.PhiusBuildingType('1-NEW_CONSTRUCTION')
    assert bldg_type.value == '1-NEW_CONSTRUCTION'
    assert bldg_type.number == 1

    bldg_type.value = '2-RETROFIT'
    assert bldg_type.value == '2-RETROFIT'
    assert bldg_type.number == 2

    bldg_type.value = '3-MIXED'
    assert bldg_type.value == '3-MIXED'
    assert bldg_type.number == 3


def test_building_bldg_type_set_by_number():
    bldg_type = honeybee_ph.phius.PhiusBuildingType('1-NEW_CONSTRUCTION')
    bldg_type.value = 1
    assert bldg_type.value == '1-NEW_CONSTRUCTION'
    assert bldg_type.number == 1

    bldg_type.value = 2
    assert bldg_type.value == '2-RETROFIT'
    assert bldg_type.number == 2

    bldg_type.value = 3
    assert bldg_type.value == '3-MIXED'
    assert bldg_type.number == 3


def test_building_bldg_type_not_allowed():
    bldg_type = honeybee_ph.phius.PhiusBuildingType('1-NEW_CONSTRUCTION')
    assert bldg_type.value == '1-NEW_CONSTRUCTION'
    assert bldg_type.number == 1

    with pytest.raises(ValueNotAllowedError):
        bldg_type.value = 'NOT_ALLOWED'
    with pytest.raises(ValueNotAllowedError):
        bldg_type.value = len(bldg_type.allowed) + 1

    assert bldg_type.value == '1-NEW_CONSTRUCTION'
    assert bldg_type.number == 1


def test_bldg_type_serialization():
    status = honeybee_ph.phius.PhiusBuildingType()
    d = status.to_dict()
    new_obj = honeybee_ph.phius.PhiusBuildingType.from_dict(d)

    assert new_obj.to_dict() == d
