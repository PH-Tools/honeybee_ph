# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Model Passive House (PH) Properties."""
try:
    from typing import Any
except ImportError:
    pass  # Python 2.7


class ModelPhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> ModelPhProperties
        _host = new_host or self._host
        new_properties_obj = ModelPhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def __str__(self):
        return "Model Passive House Properties: [host: {}]".format(self.host.display_name)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        t = 'ModelPHProperties' if not \
            abridged else 'ModelPhPropertiesAbridged'
        d.update({'type': t})
        d.update({'id_num': self.id_num})

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> ModelPhProperties
        assert _dict['type'] == 'ModelPhProperties', \
            'Expected ModelPhProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)

        return new_prop
