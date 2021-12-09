# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Model Passive House (PH) Properties."""


class ModelPhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (ModelPhProperties, Any) -> ModelPhProperties
        _host = new_host or self._host
        new_properties_obj = ModelPhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "HB-Model Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (ModelPhProperties, bool) -> dict[str, dict]
        d = {}
        t = 'ModelPHProperties' if not \
            abridged else 'ModelPhPropertiesAbridged'
        d.update({'type': t})
        d.update({'id_num': self.id_num})

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (ModelPhProperties, dict, Any) -> ModelPhProperties
        assert _dict['type'] == 'ModelPhProperties', \
            'Expected ModelPhProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)

        return new_prop
