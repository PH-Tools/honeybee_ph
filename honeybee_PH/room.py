# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive House (PH) Properties."""


class RoomPhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (RoomPhProperties, Any) -> RoomPhProperties
        _host = new_host or self._host
        new_properties_obj = RoomPhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Room Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (RoomPhProperties, bool) -> dict[str, dict]
        d = {}
        t = 'RoomPhProperties' if not \
            abridged else 'RoomPhPropertiesAbridged'
        d.update({'type': t})
        d.update({'id_num': self.id_num})

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (RoomPhProperties, dict, Any) -> RoomPhProperties
        assert _dict['type'] == 'RoomPhProperties', \
            'Expected RoomPhProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)

        return new_prop
