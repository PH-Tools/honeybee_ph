from honeybee_phhvac._base import _PhHVACBase


def test_base_default():
    new_obj = _PhHVACBase()

    assert new_obj


def test_base_equal():
    new_obj1 = _PhHVACBase()
    new_obj = new_obj1.duplicate()

    assert new_obj1 == new_obj


def test_base_not_equal():
    new_obj1 = _PhHVACBase()
    new_obj2 = _PhHVACBase()

    assert new_obj1 != new_obj2


def test_base_not_equal_different_types():
    new_obj1 = _PhHVACBase()
    new_obj2 = None

    assert new_obj1 != new_obj2
