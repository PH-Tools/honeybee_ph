# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties for Honeybee-Energy-PH | Load | People"""

from uuid import uuid4

try:
    from typing import Any, Optional, Dict
except ImportError:
    pass  # Python 2.7


class PeoplePhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(PeoplePhProperties_FromDictError, self).__init__(self.msg)


class PhDwellings(object):
    """A Dwelling Object to store information on the number of dwelling units."""

    _default = None # type: Optional[PhDwellings]

    def __init__(self, _num_dwellings=0):
        # type: (int) -> None
        self.identifier = uuid4()
        self._num_dwellings = _num_dwellings

    @property
    def num_dwellings(self):
        # type: () -> int
        return self._num_dwellings

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Any]
        d = {}
        d["identifier"] = str(self.identifier)
        d["num_dwellings"] = self.num_dwellings
        return d
    
    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhDwellings
        obj = cls(_input_dict["num_dwellings"])
        obj.identifier = _input_dict["identifier"]
        return obj

    @classmethod
    def default(cls):
        # type: () -> PhDwellings
        if cls._default is None:
            cls._default = cls()
        return cls._default

    def duplicate(self, new_host=None):
        # type: (Any) -> PhDwellings
        obj = self.__class__(self.num_dwellings)
        obj.identifier = self.identifier
        return obj

    def __hash__(self):
        return hash(self.identifier)
    
    def __eq__(self, other):
        # type: (PhDwellings) -> bool
        return self.identifier == other.identifier

    def __str__(self):
        return '{}(num_dwellings={})'.format(self.__class__.__name__, self.num_dwellings)
    
    def __repr__(self):
        return str(self)
    
    def ToString(self):
        return str(self)


class PeoplePhProperties(object):
    """Ph Properties Object for Honeybee-Energy People"""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.number_bedrooms = 0
        self.number_people = 0.0
        self.dwellings = PhDwellings.default()

    def duplicate(self, new_host=None):
        # type: (Any) -> PeoplePhProperties
        _host = new_host or self._host
        new_properties_obj = self.__class__(_host)
        new_properties_obj.id_num = self.id_num
        new_properties_obj.number_bedrooms = self.number_bedrooms
        new_properties_obj.number_people = self.number_people
        new_properties_obj.dwellings = self.dwellings

        return new_properties_obj

    @property
    def host(self):
        return self._host

    @property
    def is_residential(self):
        # type: () -> bool
        """Return True is this Load is for a 'Residential' zone."""
        return self.dwellings.num_dwellings >= 1

    @property
    def is_dwelling_unit(self):
        print("WARNING: The 'PeoplePhProperties' property 'is_dwelling_unit' is deprecated and should be replace with 'is_residential' from now on.")
        return self.is_residential

    @property
    def number_dwelling_units(self):
        """Return the total number of dwelling units on the Load."""
        # type: () -> int
        return self.dwellings.num_dwellings

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, dict]
        d = {}

        if abridged:
            d["type"] = "PeoplePhPropertiesAbridged"
        else:
            d["type"] = "PeoplePhProperties"

        d["id_num"] = self.id_num
        d["number_bedrooms"] = self.number_bedrooms
        d["number_people"] = self.number_people
        d["dwellings"] = self.dwellings.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (Dict[str, Any], Any) -> PeoplePhProperties
        valid_types = ("PeoplePhProperties", "PeoplePhPropertiesAbridged")
        if data["type"] not in valid_types:
            raise PeoplePhProperties_FromDictError(valid_types, data["type"])

        new_prop = cls(host)
        new_prop.id_num = data["id_num"]
        new_prop.number_bedrooms = data["number_bedrooms"]
        new_prop.number_people = data["number_people"]
        new_prop.dwellings = PhDwellings.from_dict(data["dwellings"])

        return new_prop

    def __eq__(self, other):
        # type: (PeoplePhProperties) -> bool

        if self.host != other.host:
            return False
        if self.id_num != other.id_num:
            return False
        if self.number_bedrooms != other.number_bedrooms:
            return False
        if self.number_people != other.number_people:
            return False
        if self.dwellings != other.dwellings:
            return False
        return True
    
    def __str__(self):
        return "{}: id={}".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return (
            "{!r}(id_num={!r}, number_bedrooms={!r}"
            " number_people={!r}, dwellings={!r})".format(
                self.__class__.__name__,
                self.id_num,
                self.number_bedrooms,
                self.number_people,
                self.dwellings
            )
        )

    def ToString(self):
        return self.__repr__()
