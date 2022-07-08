# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Face Passive House (PH) Properties."""
try:
    from typing import Any, Dict
except ImportError:
    pass  # Python 2.7


class FacePhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> FacePhProperties
        _host = new_host or self._host
        new_properties_obj = FacePhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "Face Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        t = 'FacePhProperties' if not \
            abridged else 'FacePhPropertiesAbridged'
        d.update({'type': t})
        d.update({'id_num': self.id_num})

        return {'ph': d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Any) -> FacePhProperties
        assert data['type'] == 'FacePhProperties', \
            'Expected FacePhProperties. Got {}.'.format(data['type'])

        new_prop = cls(host)
        new_prop.id_num = data.get('id_num', 0)

        return new_prop

    def apply_properties_from_dict(self, _face_prop_dict):
        # type: (Dict[str, Any]) -> None
        """Apply properties from an FacePhPropertiesAbridged dictionary.

        Arguments:
        ----------
            * _face_prop_dict (dict): A FacePhPropertiesAbridged dictionary loaded from 
                the Face object itself. Unabridged.

        Returns:
        --------
            * None
        """
        return None
