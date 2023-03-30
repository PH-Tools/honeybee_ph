# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.construction.window.WindowConstructionShade Objects"""

try:
    from typing import Any, Dict, Collection
except ImportError:
    pass  # Python 2.7


class WindowConstructionShadePhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        #type: (Collection[str], Dict[str, Any]) -> None
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type)
        super(WindowConstructionShadePhProperties_FromDictError, self).__init__(self.msg)


class WindowConstructionShadePhProperties(object):
    def __init__(self, _host):
        # type: (Any) -> None
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> WindowConstructionShadePhProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Any) -> WindowConstructionShadePhProperties
        host = new_host or self.host

        new_obj = self.__class__(host)
        new_obj.id_num = self.id_num

        return new_obj

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Any]
        d = {}

        if abridged:
            d['type'] = 'WindowConstructionShadePhPropertiesAbridged'
        else:
            d['type'] = 'WindowConstructionShadePhProperties'

        d['id_num'] = self.id_num

        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], Any) -> WindowConstructionShadePhProperties
        valid_types = ('WindowConstructionShadePhProperties',
                       'WindowConstructionShadePhPropertiesAbridged')
        if _input_dict['type'] not in valid_types:
            raise WindowConstructionShadePhProperties_FromDictError(
                valid_types, _input_dict['type'])

        new_obj = cls(host)
        new_obj.id_num = _input_dict['id_num']
        return new_obj

    def __str__(self):
        return '{}(id_num={!r})'.format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
