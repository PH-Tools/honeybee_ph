# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Helper/Temp Classes for calculating Phius Multifamily Elec. Energy"""

try:
    from typing import ValuesView
except ImportError:
    pass  # IronPython 2.7

from honeybee import room
from honeybee_ph import space


class PhiusResidentialStory(object):
    """Represents one Residential Story of the Phius Multifamily Calculator."""

    def __init__(self, hb_room_list):
        self.lighting_int_HE_frac = 1.0
        self.lighting_ext_HE_frac = 1.0
        self.lighting_garage_HE_frac = 1.0

        self.total_floor_area_m2 = self.calc_story_floor_area(hb_room_list)
        self.total_number_dwellings = len(hb_room_list)
        self.total_number_bedrooms = self.calc_story_bedrooms(hb_room_list)

        self.design_occupancy = self.calc_design_occupancy()
        self.mel = self.calc_mel()
        self.lighting_int = self.calc_lighting_int()
        self.lighting_ext = self.calc_lighting_ext()
        self.lighting_garage = self.calc_lighting_garage()

    @property
    def total_floor_area_ft2(self):
        # type () -> float
        return self.total_floor_area_m2 * 10.7639

    def calc_story_floor_area(self, _hb_rooms):
        # type: (list[room.Room]) -> float
        story_floor_area = 0
        for rm in _hb_rooms:
            for space in rm.properties.ph.spaces:
                story_floor_area += space.weighted_floor_area
        return story_floor_area

    def calc_story_bedrooms(self, _hb_rooms):
        # type: (list[room.Room]) -> int
        return sum(rm.properties.energy.people.properties.ph.number_bedrooms for rm in _hb_rooms)

    def calc_design_occupancy(self):
        # type: () -> float
        return ((self.total_number_bedrooms / self.total_number_dwellings) + 1) * self.total_number_dwellings

    def calc_mel(self):
        # type: () -> float
        return (self.total_number_dwellings * 413 + 69 * self.total_number_bedrooms + 0.91 * self.total_floor_area_ft2) * 0.8

    def calc_lighting_int(self):
        # type: () -> float
        return (0.2+0.8*(4-3*self.lighting_int_HE_frac)/3.7)*(self.total_number_dwellings*455+0.8*self.total_floor_area_ft2)*0.8

    def calc_lighting_ext(self):
        # type: () -> float
        return (1-0.75*self.lighting_ext_HE_frac)*(self.total_number_dwellings*100+0.05*self.total_floor_area_ft2)*0.8

    def calc_lighting_garage(self):
        # type: () -> float
        return self.total_number_dwellings*(100*(1-self.lighting_garage_HE_frac)+25*self.lighting_garage_HE_frac)*0.8

    def __str__(self):
        return "{}(total_floor_area_m2={}, total_number_dwellings={}, total_number_bedrooms={})".format(
            self.__class__.__name__, self.total_floor_area_m2, self.total_number_dwellings, self.total_number_bedrooms)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

# -----------------------------------------------------------------------------
# -- Non-Res


class PhiusNonResProgram(object):
    """An individual Phius Non-Res Program Type."""

    def __init__(self):
        self.name = "__unnamed_nonres_program_"
        self.usage_days_yr = 0
        self.operating_hours_day = 0
        self.lighting_W_per_ft2 = 0
        self.mel_kWh_yr = 0

    def to_phius_mf_workbook(self):
        # type: () -> str
        """Returns a text block formated to match the Phius MF Calculator."""
        return ",".join([
            str(self.name),
            str(self.usage_days_yr),
            str(self.operating_hours_day),
            str(self.lighting_W_per_ft2),
            str(self.mel_kWh_yr),
        ])

    @classmethod
    def from_hb_room(cls, _hb_room):
        # type: (room.Room) -> PhiusNonResProgram
        obj = cls()

        obj.name = _hb_room.properties.energy.program_type.display_name

        return obj

    def __str__(self):
        return '{}(name={})'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhiusNonResProgramCollection(object):
    """Collection of Phius Non-Res Program Types."""

    def __init__(self):
        self._collection = {}

    def add_program(self, _program, _key=None):
        # type: (PhiusNonResProgram, str | None) -> None
        if not _key:
            _key = _program.name
        self._collection[_key] = _program

    @property
    def programs(self):
        # type: () -> ValuesView[PhiusNonResProgram]
        return self._collection.values()

    def __getitem__(self, key):
        # type: (str) -> PhiusNonResProgram
        return self._collection[key]

    def to_phius_mf_workbook(self):
        # type: () -> str
        """Returns a text block formated to match the Phius MF Calculator."""
        return "\n".join([prog.to_phius_mf_workbook() for prog in self.programs])


class PhiusNonResRoom(object):
    """A single Phius Non-Res Space."""

    def __init__(self):
        self.multipler = 1
        self.occupancy_sensor = "-"
        self.name = "_unnamed_phius_nonres_room"
        self.icfa = 0.0
        self.misc_mel = ""
        self.program_type = PhiusNonResProgram()

    def to_phius_mf_workbook(self):
        # type: () -> str
        return ",".join([
            str(self.multipler),
            str(self.occupancy_sensor),
            str(self.name),
            str(self.program_type.name),
            str(self.misc_mel),
            str(self.icfa),
        ])

    @classmethod
    def from_ph_space(cls, _ph_space):
        # type: (space.Space) -> PhiusNonResRoom
        """Returns a new PhiusNonResSpace with properties based on a PH-Space."""
        obj = cls()

        obj.name = _ph_space.full_name
        obj.icfa = _ph_space.weighted_floor_area
        obj.program_type = PhiusNonResProgram.from_hb_room(_ph_space.host)

        return obj

    def __str__(self):
        return '{}(name={}, program_type={},'\
            'misc_mel={}, icfa={})'.format(
                self.__class__.__name__, self.name, self.program_type, self.misc_mel, self.icfa)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
