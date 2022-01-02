# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive House (PH) Properties."""
try:
    from typing import Any
except ImportError:
    # IronPython
    pass


class RoomPhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self._spaces = []

    @property
    def spaces(self):
        # type: () -> list
        return self._spaces

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> RoomPhProperties
        _host = new_host or self._host
        new_properties_obj = RoomPhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Room Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        t = 'RoomPhProperties' if not \
            abridged else 'RoomPhPropertiesAbridged'
        d.update({'type': t})
        d.update({'id_num': self.id_num})

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> RoomPhProperties
        assert _dict['type'] == 'RoomPhProperties', \
            'Expected RoomPhProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)

        return new_prop
