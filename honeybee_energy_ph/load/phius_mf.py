# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Helper/Temp Classes for calculating Phius Multifamily Elec. Energy"""

try:
    from typing import ValuesView, List
except ImportError:
    pass  # IronPython 2.7

from honeybee import room
from honeybee_energy.schedule import ruleset
from honeybee_energy.load import equipment
from honeybee_ph import space


class PhiusResidentialStory(object):
    """Represents one Residential Story of the Phius Multifamily Calculator."""

    def __init__(self, hb_room_list):
        self.lighting_int_HE_frac = 1.0
        self.lighting_ext_HE_frac = 1.0
        self.lighting_garage_HE_frac = 1.0

        self.story_number = hb_room_list[0].story
        self.total_floor_area_m2 = self.calc_story_floor_area(hb_room_list)
        self.total_number_dwellings = len(hb_room_list)
        self.total_number_bedrooms = self.calc_story_bedrooms(hb_room_list)

        self.design_occupancy = self.calc_design_occupancy(hb_room_list)
        self.mel = self.calc_mel()
        self.lighting_int = self.calc_lighting_int()
        self.lighting_ext = self.calc_lighting_ext()
        self.lighting_garage = self.calc_lighting_garage()

    @property
    def total_floor_area_ft2(self):
        # type () -> float
        return self.total_floor_area_m2 * 10.7639

    def calc_story_floor_area(self, _hb_rooms):
        # type: (List[room.Room]) -> float
        return sum(
            space.weighted_floor_area
            for rm in _hb_rooms
            for space in rm.properties.ph.spaces
        )

    def calc_story_bedrooms(self, _hb_rooms):
        # type: (List[room.Room]) -> int
        return sum(rm.properties.energy.people.properties.ph.number_bedrooms for rm in _hb_rooms)

    def calc_design_occupancy(self, _hb_rooms):
        # type: (List[room.Room]) -> float
        return sum(rm.properties.energy.people.properties.ph.number_people for rm in _hb_rooms)

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
        self.usage_days_yr = 365
        self.operating_hours_day = 0.0
        self.lighting_W_per_m2 = 0.0
        self.mel_kWh_m2_yr = 0.0
        self.mel_w_m2 = 0.0

    @property
    def lighting_W_per_ft2(self):
        # type: () -> float
        return self.lighting_W_per_m2 * 0.09290304

    @property
    def mel_kWh_ft2_yr(self):
        return self.mel_kWh_m2_yr * 0.09290304

    def to_phius_mf_workbook(self):
        # type: () -> str
        """Returns a text block formatted to match the Phius MF Calculator."""
        return ",".join([
            str(self.name),
            str(self.usage_days_yr),
            str(self.operating_hours_day),
            str(self.lighting_W_per_ft2),
            str(self.mel_kWh_ft2_yr),
        ])

    @classmethod
    def from_hb_room(cls, _hb_room):
        # type: (room.Room) -> PhiusNonResProgram
        """Returns a new PhiusNonResProgram object with attributes based on an HBE-Room."""
        obj = cls()

        obj.name = _hb_room.properties.energy.program_type.display_name
        obj.operating_hours_day = obj._operating_hours_day_from_hb_schedule(
            _hb_room.properties.energy.lighting.schedule)
        obj.lighting_W_per_m2 = _hb_room.properties.energy.lighting.watts_per_area
        obj.mel_kWh_m2_yr = obj._calc_mel_kWh_per_m2_from_hb_elec(
            _hb_room.properties.energy.electric_equipment
        )
        obj.mel_w_m2 = _hb_room.properties.energy.electric_equipment.watts_per_area

        return obj

    def _calc_mel_kWh_per_m2_from_hb_elec(self, _hb_elec_equip):
        # type: (equipment.ElectricEquipment) -> float
        """Returns the total Elec. Equip kWh for the HBE-Electric-Equipment."""

        # -- Calc annual full-load hours
        annual_full_load_hours = sum(_hb_elec_equip.schedule.values())

        # -- Calc total usage in kWh
        return (_hb_elec_equip.watts_per_area * annual_full_load_hours) / 1000

    def _operating_hours_day_from_hb_schedule(self, _hb_lght_sched):
        # type: (ruleset.ScheduleRuleset) -> float
        """Return a daily operating period (num. hours) from an HB-Lighting-Schedule"""
        operating_frac = sum(_hb_lght_sched.values()) / len(_hb_lght_sched.values())
        return operating_frac * 24

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
        """Adds a new PhiusNonResProgram to the collection."""
        if not _key:
            _key = _program.name
        self._collection[_key] = _program

    @property
    def programs(self):
        # type: () -> ValuesView[PhiusNonResProgram]
        """Returns a ValuesView of the PhiusNonResPrograms in the collection dict."""
        return self._collection.values()

    def __getitem__(self, key):
        # type: (str) -> PhiusNonResProgram
        return self._collection[key]

    def to_phius_mf_workbook(self):
        # type: () -> List[str]
        """Returns a text block formatted to match the Phius MF Calculator."""
        return [prog.to_phius_mf_workbook() for prog in self.programs]


class PhiusNonResRoom(object):
    """A single Phius Non-Res Space."""

    def __init__(self):
        self.multiplier = 1
        self.occupancy_sensor = "N"
        self.name = "_unnamed_phius_nonres_room"
        self.icfa_m2 = 0.0
        self.misc_mel = 0.0 # kWh/yr
        self.program_type = PhiusNonResProgram()

    @property
    def icfa_ft2(self):
        # type: () -> float
        return self.icfa_m2 * 10.7639

    @property
    def mel_kWh_yr(self):
        # type: () -> float
        """Total yearly MEL kWh EXCLUDING the Misc MEL"""
        return (self.icfa_m2 * self.program_type.mel_kWh_m2_yr)

    @property
    def mel_w_m2(self):
        # type: () -> float
        return self.program_type.mel_w_m2

    @property
    def total_mel_kWh(self):
        """Total yearly MEL kWh INCLUDING the Misc MEL"""
        # type: () -> float
        return self.mel_kWh_yr + self.misc_mel

    @property
    def total_lighting_kWh(self):
        # type: () -> float
        return (self.program_type.usage_days_yr * self.program_type.operating_hours_day *
                self.program_type.lighting_W_per_m2 * self.icfa_m2) / 1000

    def to_phius_mf_workbook(self):
        # type: () -> str
        """Returns a string representation that matches the Phius MF Calculator."""
        return ",".join([
            str(self.program_type.name),
            "", # Blank
            "", # Number
            str(self.name),
            str(self.occupancy_sensor),
            str(self.multiplier),
            str(self.icfa_ft2),
            str(self.mel_w_m2),
        ])

    def to_phius_mf_workbook_results(self):
        return ",".join([
            str(self.program_type.lighting_W_per_ft2),
            str(self.program_type.usage_days_yr),
            str(self.program_type.operating_hours_day),
            str(self.program_type.mel_kWh_ft2_yr),
            str(self.total_lighting_kWh),
            str(self.mel_kWh_yr),
        ])

    @classmethod
    def from_ph_space(cls, _ph_space):
        # type: (space.Space) -> PhiusNonResRoom
        """Returns a new PhiusNonResSpace with properties based on a PH-Space."""
        obj = cls()

        obj.name = _ph_space.full_name
        obj.icfa_m2 = _ph_space.weighted_floor_area
        obj.program_type = PhiusNonResProgram.from_hb_room(_ph_space.host)

        return obj

    def __str__(self):
        return '{}(name={}, program_type={},'\
            'misc_mel={}, icfa={})'.format(
                self.__class__.__name__, self.name, self.program_type, self.misc_mel, self.icfa_m2)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
