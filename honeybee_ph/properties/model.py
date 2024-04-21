# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-PH Model Properties."""

try:
    from typing import Any, Dict, Tuple
except ImportError:
    pass  # Python 2.7

try:
    from itertools import izip as zip  # type: ignore
except ImportError:
    pass  # Python3

try:
    from honeybee import extensionutil
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee import extensionutil
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_ph.bldg_segment import BldgSegment
    from honeybee_ph.team import ProjectTeam
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


class ModelPhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.team = ProjectTeam()

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> ModelPhProperties
        _host = new_host or self._host
        new_properties_obj = ModelPhProperties(_host)
        new_properties_obj.id_num = self.id_num
        new_properties_obj.team = self.team.duplicate()

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
        # -- Collect all the unique BldgSegments in the Model's Rooms
        ph_bldg_segments = {
            rm.properties.ph.ph_bldg_segment.identifier: rm.properties.ph.ph_bldg_segment for rm in self.host.rooms
        }
        return [seg.to_dict() for seg in ph_bldg_segments.values()]

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]

        d = {}
        if abridged == False:
            d["type"] = "ModelPhPropertiesAbridged"
            d["id_num"] = self.id_num
            d["bldg_segments"] = self._get_bldg_segment_dicts()
            d["team"] = self.team.to_dict()
        else:
            d["type"] = "ModelPhProperties"
            d["id_num"] = self.id_num
            d["bldg_segments"] = []
            d["team"] = self.team.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict[str, Any], Any) -> ModelPhProperties
        assert _dict["type"] == "ModelPhProperties", "Expected ModelPhProperties. Got {}.".format(_dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _dict.get("id_num", 0)
        new_prop.team = ProjectTeam.from_dict(_dict.get("team", {}))

        return new_prop

    @staticmethod
    def load_properties_from_dict(data):
        # type: (Dict[str, Dict]) -> Tuple[Dict[str, BldgSegment], ProjectTeam]
        """Load the HB-Model .ph properties from an HB-Model dictionary as Python objects.

        Loaded objects include: BldgSegment, Team, ...

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
            * tuple[dict[str, BldgSegment], ProjectTeam]: ModelPhProperties Objects
        """
        assert "ph" in data["properties"], "HB-Model Dictionary possesses no ModelPhProperties?"

        bldg_segments_ = {}
        for seg in data["properties"]["ph"]["bldg_segments"]:
            bldg_segments_[seg["identifier"]] = BldgSegment.from_dict(seg)

        team = ProjectTeam.from_dict(data["properties"]["ph"]["team"])

        return bldg_segments_, team

    def apply_properties_from_dict(self, data):
        # type: (Dict[str, Any]) -> None
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
        assert "ph" in data["properties"], "Dictionary possesses no ModelPhProperties?"

        # collect lists of .ph property dictionaries at the sub-model level (room, face, etc)
        (
            room_ph_dicts,
            face_ph_dicts,
            shd_ph_dicts,
            ap_ph_dicts,
            dr_ph_dicts,
        ) = extensionutil.model_extension_dicts(data, "ph", [], [], [], [], [])

        # re-build all of the .ph property objects from the HB-Model dict as python objects
        bldg_segments, self.team = self.load_properties_from_dict(data)

        # apply the .ph properties to all the sub-model objects in the HB-Model
        for room, room_dict in zip(self.host.rooms, room_ph_dicts):
            if not room_dict:
                continue
            room.properties.ph.apply_properties_from_dict(room_dict, bldg_segments)

        apertures = []
        faces = []
        for hb_room in self.host.rooms:
            for face in hb_room.faces:
                faces.append(face)
                for aperture in face.apertures:
                    apertures.append(aperture)

        for face, face_dict in zip(faces, face_ph_dicts):
            face.properties.ph.apply_properties_from_dict(face_dict)

        for aperture, ap_dict in zip(apertures, ap_ph_dicts):
            aperture.properties.ph.apply_properties_from_dict(ap_dict)
