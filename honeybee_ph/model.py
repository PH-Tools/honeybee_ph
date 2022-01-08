# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Model Passive House (PH) Properties."""
try:
    from typing import Any
except ImportError:
    pass  # Python 2.7

try:
    from itertools import izip as zip
except ImportError:
    pass  # Python3


from honeybee import extensionutil
from honeybee_ph.bldg_segment import BldgSegment


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

    def _get_bldg_segment_dicts(self):
        # type: () -> list[dict]
        """Return a dict of all the bldg_segments found on the model rooms.

        Arguments:
        ----------
            * None

        Returns:
        --------
            * list: A list of all the bldg_segments found on the rooms as dicts.
        """
        return [hb_room.properties.ph.ph_bldg_segment.to_dict() for hb_room in self.host.rooms]

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        t = 'ModelPHProperties' if not \
            abridged else 'ModelPhPropertiesAbridged'
        d['type'] = t
        d['id_num'] = self.id_num

        # -- Add all the bldg_segment objects to the dict
        d['bldg_segments'] = self._get_bldg_segment_dicts()

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict[str, Any], Any) -> ModelPhProperties
        assert _dict['type'] == 'ModelPhProperties', \
            'Expected ModelPhProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)

        return new_prop

    @staticmethod
    def load_properties_from_dict(data):
        # type: (dict) -> tuple
        """Load model .ph properties of a dictionary into Python objects.

        Loaded objects include .......

        The function is called when re-serializing a Model object from a dictionary
        to load honeybee_ph objects into their Python object form before
        applying them to the Model geometry.

        Arguments:
        ----------
            data: A dictionary representation of an entire honeybee-core Model.
                Note that this dictionary must have ModelPhProperties in order
                for this method to successfully load the .ph properties.

                Note: data.keys() will include: 
                [
                    'display_name', 'identifier', 'tolerance', 
                    'angle_tolerance', 'rooms', 'type', 'version', 
                    'units', 'orphaned_shades', 'properties'
                ]

        Returns:
        --------
            * tuple[dict, dict]
        """
        assert 'ph' in data['properties'], \
            'HB-Model Dictionary possesses no ModelPhProperties?'

        bldg_segments = {}
        for seg in data['properties']['ph']['bldg_segments']:
            bldg_segments[seg['identifier']] = BldgSegment.from_dict(seg)

        return {}, bldg_segments

    def apply_properties_from_dict(self, data):
        # type: (dict[str, Any]) -> None
        """Apply the .ph properties of a dictionary to the host Model of this object.

        Arguments:
        ----------
            * data (dict[str, Any]): A dictionary representation of an entire 
                honeybee-core Model. Note that this dictionary must have ModelPhProperties 
                in order for this method to successfully apply the .ph properties.

                Note: data.keys() will include: 
                [
                    'display_name', 'identifier', 'tolerance', 
                    'angle_tolerance', 'rooms', 'type', 'version', 
                    'units', 'orphaned_shades', 'properties'
                ]

        Returns:
        --------
            * None
        """
        assert 'ph' in data['properties'], \
            'Dictionary possesses no ModelPhProperties.'

        # re-build all of the .ph property objects from the HB-Model dict
        spaces, bldg_segments = self.load_properties_from_dict(data)

        # collect lists of .ph property dictionaries at the sub-model level (room, face, etc)
        room_ph_dicts, face_ph_dicts, shd_ph_dicts, ap_ph_dicts, dr_ph_dicts = \
            extensionutil.model_extension_dicts(data, 'ph', [], [], [], [], [])

        # apply the .ph properties to all the objects in the Model
        for room, room_dict in zip(self.host.rooms, room_ph_dicts):
            if not room_dict:
                continue
            room.properties.ph.apply_properties_from_dict(room_dict, bldg_segments)
