# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Energy conversion factor (CO2, Source) functions"""

try:
    from typing import List, Any, Generator, Optional
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import _base


class FuelNotAllowedError(Exception):
    def __init__(self, _fuel_type_input):
        self.msg = "Error: Fuel type: '{}' not allowed.".format(_fuel_type_input)
        super(FuelNotAllowedError, self).__init__(self.msg)


def clean_input(input):
    # type: (Optional[str]) -> Optional[str]
    """Returns a clean/standardized string with no spaces, all upper-case"""
    if not input:
        return None
    return str(input).lstrip().rstrip().replace(' ', '_').upper()


def build_factors_from_library(_factor_dict):
    # type: (dict[str, dict[str, Any]]) -> List[Factor]
    """Returns a list of factors based on an input data dict. from the library."""

    factor_list = []
    for item, item_dict in _factor_dict.items():
        new_factor = Factor()
        new_factor.fuel_name = clean_input(item)
        new_factor.value = item_dict['value']
        new_factor.unit = item_dict['unit']
        factor_list.append(new_factor)

    return factor_list


class Factor(_base._Base):
    """Dataclass for site->other conversion factor"""

    def __init__(self):
        # type: () -> None
        super(Factor, self).__init__()
        self.fuel_name = ''
        self.value = 0.0
        self.unit = ''

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['fuel_name'] = self.fuel_name
        d['value'] = self.value
        d['units'] = self.unit

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> Factor
        new_obj = cls()

        new_obj.fuel_name = _input_dict['fuel_name']
        new_obj.value = _input_dict['value']
        new_obj.unit = _input_dict['units']

        return new_obj

    def __str__(self):
        return "{}(fuel={}, value={:.02f})".format(
            self.__class__.__name__, self.fuel_name, float(self.value))

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class FactorCollection(_base._Base):
    """Collection of conversion factors."""

    def __init__(self, _name='', _factors=None):
        # type: (str, List[Factor] | None) -> None
        super(FactorCollection, self).__init__()
        self.name = _name
        if _factors:
            self.factors = _factors
        else:
            self.factors = []

    def add_factor(self, _new_factor):
        # type: (Factor) -> None
        """Add a new factor to the collection. If the factor already exists, update it."""

        for i, exg_factor in enumerate(self.factors):
            if exg_factor.fuel_name == _new_factor.fuel_name:
                self.factors[i] = _new_factor
                return None
        self.factors.append(_new_factor)
        return None

    def validate_fuel_types(self, _allowed_fuels):
        for factor in self.factors:
            if factor.fuel_name not in _allowed_fuels:
                raise FuelNotAllowedError(factor.fuel_name)

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['factors'] = []
        for factor in self.factors:
            d['factors'].append(factor.to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> FactorCollection
        new_obj = cls()

        for factor_dict in _input_dict['factors']:
            new_obj.factors.append(Factor.from_dict(factor_dict))

        return new_obj

    def __copy__(self):
        # type: () -> FactorCollection
        obj = FactorCollection()

        obj.set_base_attrs_from_source(self)
        obj.name = self.name
        obj.factors = [f for f in self.factors]

        return obj

    def duplicate(self):
        # type: () -> FactorCollection
        return self.__copy__()

    def __iter__(self):
        # type: () -> Generator[Factor, None, None]
        for factor in self.factors:
            yield factor

    def __str__(self):
        return "{}(name={}, {} fuel factors)".format(
            self.__class__.__name__, self.name, len(self.factors))

    def ToString(self):
        return str(self)
