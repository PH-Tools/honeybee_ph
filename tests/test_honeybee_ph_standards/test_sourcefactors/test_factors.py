import pytest

from honeybee_ph_standards.sourcefactors import factors


def test_clean_input() -> None:
    assert factors.clean_input(None) == None
    assert factors.clean_input("") == ""
    assert factors.clean_input("abc") == "ABC"
    assert factors.clean_input("abc ") == "ABC"
    assert factors.clean_input(" abc") == "ABC"
    assert factors.clean_input(" abc ") == "ABC"
    assert factors.clean_input(" abc def ") == "ABC_DEF"


def test_Factor() -> None:
    factor = factors.Factor()
    assert factor.fuel_name == ""
    assert factor.value == 0.0
    assert factor.unit == ""
    d = factor.to_dict()
    assert d == {"fuel_name": "", "value": 0.0, "units": ""}
    assert factors.Factor.from_dict(d).to_dict() == d


def test_FactorCollection() -> None:
    factor_collection = factors.FactorCollection()
    factor_collection.add_factor(factors.Factor("abc", 1.0, "KWH/KWH"))
    assert len(factor_collection.factors) == 1

    d = factor_collection.to_dict()
    assert d == {"factors": [{"fuel_name": "ABC", "value": 1.0, "units": "KWH/KWH"}]}
    assert factors.FactorCollection.from_dict(d).to_dict() == d


def test_FactorCollection_get_nonexisting_factor():
    factor_collection = factors.FactorCollection()

    with pytest.raises(ValueError):
        factor_collection.get_factor("abc")


def test_FactorCollection_get_existing_factor():
    factor_collection = factors.FactorCollection()
    factor_collection.add_factor(factors.Factor("abc", 1.0, "KWH/KWH"))
    factor = factor_collection.get_factor("ABC")
    assert factor.value == 1.0
    assert factor.unit == "KWH/KWH"
