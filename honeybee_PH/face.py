# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Face Passive House (PH) Properties."""


class FacePHProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        _host = new_host or self._host
        new_properties_obj = FacePHProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Face Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        base = {'_PH': {}}
        base['_PH']['type'] = 'FacePHProperties' if not \
            abridged else 'FacePHPropertiesAbridged'

        return base

    @classmethod
    def from_dict(cls, data, host):
        assert data['type'] == 'FacePHProperties', \
            'Expected FacePHProperties. Got {}.'.format(data['type'])

        new_prop = cls(host)
        new_prop.id_num = data.get('id_num', 0)

        return new_prop
