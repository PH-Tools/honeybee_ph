from honeybee_ph._base import _Base


def test_identifier_unique():
    o1 = _Base()
    o2 = _Base()

    assert o1.identifier != o2.identifier
    assert o1.identifier_short != o2.identifier_short

    assert o1.identifier_short in str(o1)
    assert o1.identifier_short in o1.ToString()
    assert o1.identifier_short in repr(o1)


def test_no_name_is_identifier():
    o1 = _Base()

    assert o1.identifier == o1.display_name


def test_display_name():
    o1 = _Base()

    assert o1.identifier == o1.display_name

    o1.display_name = "a test name"

    assert o1.identifier != o1.display_name


def test_set_attrs_from_source():
    o1 = _Base()
    o1.display_name = "A Test"
    o1.user_data["test_key"] = "test_vale"

    o2 = _Base()
    o2.set_base_attrs_from_source(o1)

    assert o1.identifier == o2.identifier
    assert o1.identifier_short == o2.identifier_short
    assert o1.display_name == o2.display_name
    assert o1.user_data == o2.user_data
