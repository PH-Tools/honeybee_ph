# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""A simplified custom Enum class since IronPython doesn't have an enum."""

try:
    from typing import Any
except ImportError:
    pass  # IronPython


class ValueNotAllowedError(Exception):
    def __init__(self, _in, _enum):
        self.message = 'Value: {} not allowed for enum {}'.format(
            str(_in), _enum)
        super(ValueNotAllowedError, self).__init__(self.message)


class CustomEnum(object):
    allowed = []

    def __init__(self, _value=''):
        self._value = _value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _in):
        # type: (str | int) -> None
        """Allows the user to set the .value as one of the allowed values. If an 
            integer is passed in, will attempt to find the corresponding value from the 
            allowed-values list (1-based, ie: user-input '1' -> self.allowed.index(0) ).
        """
        if str(_in).upper() in self.allowed:
            self._value = str(_in).upper()
        else:
            try:
                input = int(_in) - 1
                self._value = self.allowed[input]
            except:
                raise ValueNotAllowedError(_in, self)

    @property
    def number(self):
        # type: () -> int
        """Returns the index pos of self.value (1-based)"""
        return self.allowed.index(self._value) + 1

    def __str__(self):
        return "{}(_value={} [number={}])".format(self.__class__.__name__, self.value, self.number)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}
        d['_value'] = self.value
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, Any]) -> CustomEnum
        obj = cls(_dict.get('_value'))
        return obj
