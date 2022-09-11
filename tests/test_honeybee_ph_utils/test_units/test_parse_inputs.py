from honeybee_ph_utils.units import parse_input


def test_parse_string_no_units():
    assert parse_input("4") == ("4", None)
    assert parse_input(4) == ("4", None)
    assert parse_input("-4") == ("-4", None)
    assert parse_input(-4) == ("-4", None)

    assert parse_input("4.0") == ("4.0", None)
    assert parse_input(4.0) == ("4.0", None)
    assert parse_input("-4.0") == ("-4.0", None)
    assert parse_input(-4.0) == ("-4.0", None)


def test_parse_string_with_units():
    assert parse_input("4 BTU/HR-FT-F") == ("4", "BTU/HR-FT-F")
    assert parse_input("4 BTU/HR-FT-F") == ("4", "BTU/HR-FT-F")
    assert parse_input("4BTU/HR-FT-F") == ("4", "BTU/HR-FT-F")
    assert parse_input("-4 BTU/HR-FT-F") == ("-4", "BTU/HR-FT-F")

    assert parse_input("4.0 BTU/HR-FT-F") == ("4.0", "BTU/HR-FT-F")
    assert parse_input("4.0BTU/HR-FT-F") == ("4.0", "BTU/HR-FT-F")
    assert parse_input("-4.0 BTU/HR-FT-F") == ("-4.0", "BTU/HR-FT-F")


def test_parse_string_no_value():
    assert parse_input("Missing Value") == ("", "Missing Value")
