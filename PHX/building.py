# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Building Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field

from honeybee.room import Room as HB_Room
from honeybee.face import Face as HB_Face
from honeybee.aperture import Aperture as HB_Aperture

from PHX import ventilation


@dataclass
class Zone:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    volume_gross: float = 0.0
    volume_net: float = 0.0
    weighted_net_floor_area: float = 0.0
    clearance_height: float = 2.5
    specific_heat_capacity: float = 132
    wufi_rooms: list[ventilation.RoomVentilation] = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> Zone:
        obj = cls()

        obj.id_num = cls._count
        obj.name = _hb_room.display_name

        # -- Sort the room order by full_name
        sorted_spaces = sorted(_hb_room.properties.ph.spaces, key=lambda x: x.full_name)

        # -- Create a new WUFI-RoomVentilation for each space
        obj.wufi_rooms = [ventilation.RoomVentilation.from_space(
            sp) for sp in sorted_spaces]

        obj.volume_gross = _hb_room.volume
        obj.weighted_net_floor_area = sum(
            (rm.weighted_floor_area for rm in obj.wufi_rooms))
        obj.volume_net = sum((rm.net_volume for rm in obj.wufi_rooms))

        return obj


@dataclass
class Component:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    type: int = 1
    color_interior: int = 1
    color_exterior: int = 1
    exposure_exterior: int = -1
    exposure_interior: int = 1
    interior_attachment_id: int = -1
    assembly_type_id_num: int = -1
    window_type_id_num: int = -1
    polygon_ids: list[int] = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Component, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_opaque_face(cls, _hb_face: HB_Face, _hb_room: HB_Room) -> Component:
        """Returns a new Component based on a Honeybee Face"""
        obj = cls()

        obj.name = _hb_face.display_name
        obj.id_num = cls._count

        obj.type = obj.hb_face_type_to_WUFI(_hb_face)
        obj.exposure_exterior = obj.hb_face_exposure_ext_to_WUFI(_hb_face)
        obj.exposure_interior = obj.hb_face_exposure_int_to_WUFI(_hb_room)
        obj.color_interior = obj.int_color_by_hb_face(_hb_face)
        obj.color_exterior = obj.ext_color_by_hb_face(_hb_face)
        obj.assembly_type_id_num = _hb_face.properties.energy.construction.properties._ph.id_num

        obj.polygon_ids = [_hb_face.properties._ph.id_num]

        return obj

    @classmethod
    def from_aperture(cls, _aperture: HB_Aperture, _hb_room: HB_Room) -> Component:
        """Create a new Component based on a Honeybee Aperture."""
        obj = cls()

        obj.name = _aperture.display_name
        obj.id_num = cls._count

        obj.type = 2  # Transparent
        obj.exposure_exterior = obj.hb_face_exposure_ext_to_WUFI(_aperture)
        obj.exposure_interior = obj.hb_face_exposure_int_to_WUFI(_hb_room)
        obj.color_interior = 4  # Window
        obj.color_exterior = 4  # Window
        obj.window_type_id_num = _aperture.properties.energy.construction.properties._ph.id_num

        obj.polygon_ids = [_aperture.properties._ph.id_num]

        return obj

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> list[Component]:
        """Returns a list of new Components based on the Room's Opaque Faces and Apertures."""

        compos = []
        for hb_face in _hb_room:
            for aperture in hb_face.apertures:
                compos.append(cls.from_aperture(aperture, _hb_room))

            compos.append(cls.from_opaque_face(hb_face, _hb_room))

        return compos

    def hb_face_type_to_WUFI(self, _hb_face: HB_Face) -> int:
        """Return a WUFI-Type ID for the Component."""

        schema = {
            "Wall": 1,
            "RoofCeiling": 1,
            "Floor": 1,
            "AirBoundary": 3,
        }

        return schema.get(str(_hb_face.type), 1)

    def hb_face_exposure_ext_to_WUFI(self, _hb_face: HB_Face) -> int:
        """Return the ID number of the Exterior-Expsoure Zone for the Component."""
        schema = {
            "Outdoors": -1,
            "Ground": -2,
            "Surface": -3,
        }
        return schema.get(str(_hb_face.boundary_condition), -1)

    def hb_face_exposure_int_to_WUFI(self, _hb_room: HB_Room) -> int:
        """Return the ID number of the Interior-Exposure Zone for the Component."""
        return _hb_room.properties._ph.id_num

    def int_color_by_hb_face(self, _hb_face: HB_Face) -> int:
        """Return the ID number of the WUFI Standard color to use for the Compo."""

        schema = {
            "Wall": {
                "Outdoors": 1,
                "Surface": 3,
                "Ground": 1,
            },
            "RoofCeiling": {
                "Outdoors": 8,
                "Surface": 6,
                "Ground": 12,
            },
            "Floor": {
                "Outdoors": 5,
                "Surface": 5,
                "Ground": 12,
            },
        }

        t = str(_hb_face.type)
        bc = str(_hb_face.boundary_condition)

        return schema.get(t, {}).get(bc, 1)

    def ext_color_by_hb_face(self, _hb_face: HB_Face) -> int:
        """Return the ID number of the WUFI Standard color to use for the Compo."""

        schema = {
            "Wall": {
                "Outdoors": 2,
                "Surface": 3,
                "Ground": 12,
            },
            "RoofCeiling": {
                "Outdoors": 7,
                "Surface": 6,
                "Ground": 12,
            },
            "Floor": {
                "Outdoors": 5,
                "Surface": 5,
                "Ground": 12,
            },
        }

        t = str(_hb_face.type)
        bc = str(_hb_face.boundary_condition)

        return schema.get(t, {}).get(bc, 1)


@dataclass
class Building:
    components: list[Component] = field(default_factory=list)
    zones: list[Zone] = field(default_factory=list)

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> Building:
        obj = cls()
        obj.create_components_from_hb_room(_hb_room)
        obj.create_zones_from_hb_room(_hb_room)

        return obj

    def create_components_from_hb_room(self, _hb_room: HB_Room) -> None:
        self.components = Component.from_hb_room(_hb_room)

    def create_zones_from_hb_room(self, _hb_room: HB_Room) -> None:
        self.zones.append(Zone.from_hb_room(_hb_room))
