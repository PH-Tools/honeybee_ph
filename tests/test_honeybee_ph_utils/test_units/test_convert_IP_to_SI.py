from ast import parse
from honeybee_ph_utils.units import parse_input, convert


def test_positive_inches():
    assert convert(*parse_input("3 IN"), "IN") == 3
    assert convert(*parse_input("3 IN"), "FT") == 0.25
    assert convert(*parse_input("4 IN"), "M") == 0.1016
    assert convert(*parse_input("4 IN"), "CM") == 10.16
    assert convert(*parse_input("4 IN"), "MM") == 101.6


def test_negative_inches():
    assert convert(*parse_input("-3 IN"), "IN") == -3
    assert convert(*parse_input("-3 IN"), "FT") == -0.25
    assert convert(*parse_input("-4 IN"), "M") == -0.1016
    assert convert(*parse_input("-4 IN"), "CM") == -10.16
    assert convert(*parse_input("-4 IN"), "MM") == -101.6


def test_positive_feet():
    assert convert(*parse_input("3 FT"), "FT") == 3
    assert convert(*parse_input("3 FT"), "IN") == 36
    assert convert(*parse_input("4 FT"), "M") == 1.2192
    assert convert(*parse_input("4 FT"), "CM") == 121.92
    assert convert(*parse_input("4 FT"), "MM") == 1219.2


def test_negative_feet():
    assert convert(*parse_input("-3 FT"), "FT") == -3
    assert convert(*parse_input("-3 FT"), "IN") == -36
    assert convert(*parse_input("-4 FT"), "M") == -1.2192
    assert convert(*parse_input("-4 FT"), "CM") == -121.92
    assert convert(*parse_input("-4 FT"), "MM") == -1219.2
