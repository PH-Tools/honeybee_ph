# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Model Passive House (PH) Properties."""


class ModelPHProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        _host = new_host or self._host
        new_properties_obj = ModelPHProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Model Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        d = {}
        t = 'ModelPHProperties' if not \
            abridged else 'ModelPHPropertiesAbridged'
        d.update({'type': t})
        d.update({'id_num': self.id_num})

        return {'PH': d}

    @classmethod
    def from_dict(cls, _dict, host):
        assert _dict['type'] == 'ModelPHProperties', \
            'Expected ModelPHProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)

        return new_prop
