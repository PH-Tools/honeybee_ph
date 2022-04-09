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
from honeybee_ph import bldg_segment


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
        # type: () -> list[dict[str, Any]]
        """Return a list of all the bldg_segments found on the model's rooms as dicts. 
            This is used when writing an 'Abridged' HBJSON file.

        Arguments:
        ----------
            * None

        Returns:
        --------
            * list[dict[str, Any]]: A list of all the bldg_segments found on the model's 
                rooms as dicts.
        """
        segments = {rm.properties.ph.ph_bldg_segment for rm in self.host.rooms}
        return [seg.to_dict() for seg in segments]

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]

        d = {}
        if abridged == False:
            d['type'] = 'ModelPhPropertiesAbridged'
            d['id_num'] = self.id_num
            d['bldg_segments'] = self._get_bldg_segment_dicts()
        else:
            d['type'] = 'ModelPHProperties'
            d['id_num'] = self.id_num
            d['bldg_segments'] = []

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
        # type: (dict[str, dict]) -> dict
        """Load the HB-Model .ph properties from an HB-Model dictionary as Python objects.

        Loaded objects include: BldgSegment.......

        The function is called when re-serializing an HB-Model object from a 
        dictionary. It will load honeybee_ph entities as Python objects and returns
        a tuple of dictionaries with all the de-serialized Honeybee-PH objects.

        Arguments:
        ----------
            data: A dictionary representation of an entire honeybee-core Model.
                 Note that this dictionary must have ModelPhProperties 
                in order for this method to successfully apply the .ph properties.

                Note: data is an HB-Model dict and .keys() will include: 
                [
                    'display_name', 'identifier', 'tolerance', 
                    'angle_tolerance', 'rooms', 'type', 'version', 
                    'units', 'orphaned_shades', 'properties'
                ]

        Returns:
        --------
            * tuple[dict, dict]: A tuple of dictionaries with all the Honeybee-PH objects.
        """
        assert 'ph' in data['properties'], \
            'HB-Model Dictionary possesses no ModelPhProperties?'

        bldg_segments = {}
        for seg in data['properties']['ph']['bldg_segments']:
            bldg_segments[seg['identifier']] = bldg_segment.BldgSegment.from_dict(seg)

        return bldg_segments

    def apply_properties_from_dict(self, data):
        # type: (dict[str, Any]) -> None
        """Apply the .ph properties of a dictionary to the host Model of this object.

        This method is called when the HB-Model is de-serialized from a dict back into 
        a Python object. In an 'Abridged' HBJSON file, all the property information 
        is stored at the model level, not at the sub-model object level. In that case, 
        this method is used to apply the right property data back onto all the sub-model  
        objects (faces, rooms, apertures, etc).

        Arguments:
        ----------
            * data (dict[str, Any]): A dictionary representation of an entire honeybee-core
                Model. Note that this dictionary must have ModelPhProperties 
                in order for this method to successfully apply the .ph properties.

                Note: data is an HB-Model dict and .keys() will include: 
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
            'Dictionary possesses no ModelPhProperties?'

        # re-build all of the .ph property objects from the HB-Model dict as python objects
        bldg_segments = self.load_properties_from_dict(data)

        # collect lists of .ph property dictionaries at the sub-model level (room, face, etc)
        room_ph_dicts, face_ph_dicts, shd_ph_dicts, ap_ph_dicts, dr_ph_dicts = \
            extensionutil.model_extension_dicts(data, 'ph', [], [], [], [], [])

        # apply the .ph properties to all the sub-model objects in the HB-Model
        for room, room_dict in zip(self.host.rooms, room_ph_dicts):
            if not room_dict:
                continue
            room.properties.ph.apply_properties_from_dict(room_dict, bldg_segments)

        # TODO: all the rest (apertures, faces, etc...)
