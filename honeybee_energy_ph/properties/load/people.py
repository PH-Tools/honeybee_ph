# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties for Honeybee-Energy-PH | Load | People"""

try:
    from typing import Any, Optional
except ImportError:
    # Python 2.7
    pass


class PeoplePhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(PeoplePhProperties_FromDictError, self).__init__(self.msg)


class PeoplePhProperties(object):
    """Ph Properties Object for Honeybee-Energy People"""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.number_bedrooms = 0
        self.number_people = 0.0
        self._is_dwelling_unit = None  # type: Optional[bool]
        self.number_dwelling_units = 0

    @property
    def is_dwelling_unit(self):
        # type: () -> bool
        if self._is_dwelling_unit is not None:
            return self._is_dwelling_unit
        else:
            if self.number_dwelling_units > 0:
                return True
            else:
                return False

    @is_dwelling_unit.setter
    def is_dwelling_unit(self, _input):
        # type: (bool) -> None
        if _input is not None:
            self._is_dwelling_unit = _input

    def duplicate(self, new_host=None):
        # type: (Any) -> PeoplePhProperties
        _host = new_host or self._host
        new_properties_obj = self.__class__(_host)
        new_properties_obj.id_num = self.id_num
        new_properties_obj.number_bedrooms = self.number_bedrooms
        new_properties_obj.number_people = self.number_people
        new_properties_obj._is_dwelling_unit = self._is_dwelling_unit
        new_properties_obj.number_dwelling_units = self.number_dwelling_units

        return new_properties_obj

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}

        if abridged:
            d["type"] = "PeoplePhPropertiesAbridged"
        else:
            d["type"] = "PeoplePhProperties"

        d["id_num"] = self.id_num
        d["number_bedrooms"] = self.number_bedrooms
        d["number_people"] = self.number_people
        d["_is_dwelling_unit"] = self._is_dwelling_unit
        d["number_dwelling_units"] = self.number_dwelling_units

        return {"ph": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> PeoplePhProperties
        valid_types = ("PeoplePhProperties", "PeoplePhPropertiesAbridged")
        if data["type"] not in valid_types:
            raise PeoplePhProperties_FromDictError(valid_types, data["type"])

        new_prop = cls(host)
        new_prop.id_num = data["id_num"]
        new_prop.number_bedrooms = data["number_bedrooms"]
        new_prop.number_people = data["number_people"]
        new_prop._is_dwelling_unit = data["_is_dwelling_unit"]
        new_prop.number_dwelling_units = data["number_dwelling_units"]

        return new_prop

    def __str__(self):
        return "{}: id={}".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return (
            "{!r}(id_num={!r}, number_bedrooms={!r}"
            " number_people={!r}, is_dwelling_unit={!r}, number_dwelling_units={!r})".format(
                self.__class__.__name__,
                self.id_num,
                self.number_bedrooms,
                self.number_people,
                self.number_dwelling_units,
            )
        )

    def ToString(self):
        return self.__repr__()
