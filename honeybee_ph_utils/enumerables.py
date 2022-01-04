# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""A simplified custom Enum class since IronPython sucks so bad and doesn't have 
an enum module for some inexplicable reason. God I can't wait for PY3....
"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython


class ValueNotAllowedError(Exception):
    def __init__(self, _in, _enum):
        self.message = 'Value: {} not allowed for enum {}'.format(str(_in), _enum)
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
        # type: (Any) -> None
        if str(_in).upper() in self.allowed:
            self._value = str(_in).upper()
        else:
            try:
                self._value = self.allowed[int(_in) - 1]
            except:
                raise ValueNotAllowedError(_in, self)

    @property
    def number(self):
        return self.allowed.index(self._value) + 1

    def __str__(self):
        return "{}(_value={} [number={}])".format(self.__class__.__name__, self.value, self.number)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d['_value'] = self.value
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> CustomEnum
        obj = cls(_dict.get('_value'))
        return obj
