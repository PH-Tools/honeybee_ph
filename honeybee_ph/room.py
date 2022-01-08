# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive House (PH) Properties."""

try:
    from typing import Any
except ImportError:
    pass  # Python2.7

from honeybee_ph.bldg_segment import BldgSegment


class RoomPhProperties(object):

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self._spaces = []
        self.ph_bldg_segment = BldgSegment()

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
        new_properties_obj._spaces = self._spaces
        new_properties_obj.ph_bldg_segment = self.ph_bldg_segment

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "Room Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}

        if abridged == False:
            d['type'] = 'RoomPhProperties'
            d['id_num'] = self.id_num
            d['ph_bldg_segment'] = self.ph_bldg_segment.to_dict()
        else:
            d['type'] = 'RoomPhPropertiesAbridged'
            d['ph_bldg_segment_id'] = self.ph_bldg_segment.identifier

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> RoomPhProperties
        assert _dict['type'] == 'RoomPhProperties', \
            'Expected RoomPhProperties. Got {}.'.format(_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict.get('id_num', 0)
        new_prop.ph_bldg_segment = BldgSegment.from_dict(
            _dict.get('ph_bldg_segment', {}))

        return new_prop

    def apply_properties_from_dict(self, room_prop_dict, bldg_segments):
        # type: (dict[str, Any], dict[str, BldgSegment]) -> None
        """Apply properties from a RoomPhPropertiesAbridged dictionary.

        Arguments:
        ----------
            * room_prop_dict (dict): A RoomPhPropertiesAbridged dictionary loaded from 
                the room object itself. Unabridged. In Abridged form, this 
                dict will just include the 'ph_bldg_segment_id' reference instead of the
                the entire properties data dict.
            * bldg_segments (dict[str: BldgSegment]): A dict of the BldgSegment 
                objects found at the Model level. Segment-id is used as the key.

        Returns:
        --------
            * None
        """

        room_ph_bldg_segment_id = room_prop_dict.get('ph_bldg_segment_id', None)
        if room_ph_bldg_segment_id:
            self.ph_bldg_segment = bldg_segments[room_ph_bldg_segment_id]
