from honeybee_ph_standards.sourcefactors import factors, phius_CO2_factors


def test_load_phius_2018_library() -> None:
    # -- build the factors from the library
    factor_list = factors.build_factors_from_library(phius_CO2_factors.factors_2018)
    assert len(factor_list) == 16

    # -- Add them to a collection
    new_factor_collection = factors.FactorCollection()
    for factor in factor_list:
        new_factor_collection.add_factor(factor)
    assert len(new_factor_collection.factors) == 16


def test_load_phius_2021_library() -> None:
    # -- build the factors from the library
    factor_list = factors.build_factors_from_library(phius_CO2_factors.factors_2021)
    assert len(factor_list) == 16

    # -- Add them to a collection
    new_factor_collection = factors.FactorCollection()
    for factor in factor_list:
        new_factor_collection.add_factor(factor)
    assert len(new_factor_collection.factors) == 16


def test_load_phius_2024_library() -> None:
    # -- build the factors from the library
    factor_list = factors.build_factors_from_library(phius_CO2_factors.factors_2024)
    assert len(factor_list) == 16

    # -- Add them to a collection
    new_factor_collection = factors.FactorCollection()
    for factor in factor_list:
        new_factor_collection.add_factor(factor)
    assert len(new_factor_collection.factors) == 16
