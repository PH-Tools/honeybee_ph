# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Classes for calculating Phius Multifamily Elec. Energy as per Phius Multifamily Calculator (v4.2)"""


try:
    from typing import Any, ValuesView
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee.room import Room
except ImportError as e:
    raise ImportError("Failed to import honeybee: {}".format(e))

try:
    from honeybee_energy.load import equipment
    from honeybee_energy.properties.room import RoomEnergyProperties
    from honeybee_energy.schedule import ruleset
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy: {}".format(e))

try:
    from honeybee_energy_ph.load import phius_residential
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy_ph: {}".format(e))

try:
    from honeybee_ph import space
except ImportError as e:
    raise ImportError("Failed to import honeybee_ph: {}".format(e))

try:
    from ph_units.converter import convert
except ImportError as e:
    raise ImportError("Failed to import ph_units: {}".format(e))


class PhiusResidentialStory(object):
    """Represents one Residential Story of the Phius Multifamily Calculator (v4.2)"""

    LIGHTING_INT_HE_FRAC = 1.0
    LIGHTING_EXT_HE_FRAC = 1.0
    LIGHTING_GARAGE_HE_FRAC = 1.0

    def __init__(self, _hb_rooms, _area_unit):
        # type: (list[Room], str) -> None

        try:
            self.story_number = _hb_rooms[0].story
        except:
            self.story_number = 1

        self.total_floor_area_ft2 = self.calc_story_floor_area_ft2(_hb_rooms, _area_unit)
        self.total_number_dwellings = self.calc_num_dwellings(_hb_rooms)
        self.total_number_bedrooms = self.calc_story_bedrooms(_hb_rooms)

        self.design_occupancy = self.calc_passive_house_occupancy(_hb_rooms)
        self.mel = phius_residential.misc_electrical(
            self.total_number_bedrooms, self.total_floor_area_ft2, self.total_number_dwellings
        )
        self.lighting_int = phius_residential.lighting_interior(
            self.total_floor_area_ft2, self.LIGHTING_INT_HE_FRAC, self.total_number_dwellings
        )
        self.lighting_ext = phius_residential.lighting_exterior(
            self.total_floor_area_ft2, self.LIGHTING_EXT_HE_FRAC, self.total_number_dwellings
        )
        self.lighting_garage = phius_residential.lighting_garage(
            self.LIGHTING_GARAGE_HE_FRAC, self.total_number_dwellings
        )

    @property
    def story_number(self):
        # type: () -> str
        """Return the story number."""
        return str(self._story_number)

    @story_number.setter
    def story_number(self, value):
        # type: (Any) -> None
        """Set the story number."""
        # -- If the input is a single integer value, enforce padding
        try:
            self._story_number = "{:03d}".format(int(value))
        except ValueError:
            self._story_number = str(value)

    def calc_story_floor_area_ft2(self, _hb_rooms, _area_unit):
        # type: (list[Room], str) -> float
        area = sum(space.weighted_floor_area for rm in _hb_rooms for space in getattr(rm.properties, "ph").spaces)
        area_ft2 = convert(area, _area_unit, "FT2")
        if area_ft2 is None:
            raise ValueError("Error: Failed to convert '{}' floor area from {} to FT2".format(area, _area_unit))
        return area_ft2

    def calc_story_bedrooms(self, _hb_rooms):
        # type: (list[Room]) -> int
        return sum(getattr(rm.properties, "energy").people.properties.ph.number_bedrooms for rm in _hb_rooms)

    def calc_passive_house_occupancy(self, _hb_rooms):
        # type: (list[Room]) -> float
        return sum(getattr(rm.properties, "energy").people.properties.ph.number_people for rm in _hb_rooms)

    def calc_num_dwellings(self, _hb_rooms):
        # type: (list[Room]) -> int
        ph_dwelling_objs = {r.properties.energy.people.properties.ph.dwellings for r in _hb_rooms}  # type: ignore
        return sum(d.num_dwellings for d in ph_dwelling_objs)

    def __lt__(self, other):
        # type: (PhiusResidentialStory) -> bool
        return self.story_number < other.story_number

    def __eq__(self, other):
        # type: (PhiusResidentialStory) -> bool
        return self.story_number == other.story_number

    def __str__(self):
        return "{}(total_floor_area_ft2={}, total_number_dwellings={}, total_number_bedrooms={})".format(
            self.__class__.__name__,
            self.total_floor_area_ft2,
            self.total_number_dwellings,
            self.total_number_bedrooms,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


# -----------------------------------------------------------------------------
# -- Non-Res


class PhiusNonResProgram(object):
    """An individual Phius Non-Res Program Type."""

    def __init__(self):
        self.name = "__unnamed_nonres_program__"
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
        # type: () -> float
        return self.mel_kWh_m2_yr * 0.09290304

    def to_phius_mf_workbook(self):
        # type: () -> str
        """Returns a text block formatted to match the Phius MF Calculator."""
        return ",".join(
            [
                str(self.name),
                str(self.usage_days_yr),
                str(self.operating_hours_day),
                str(self.lighting_W_per_ft2),
                str(self.mel_kWh_ft2_yr),
            ]
        )

    @classmethod
    def from_hb_room(cls, _hb_room):
        # type: (Room) -> PhiusNonResProgram
        """Returns a new PhiusNonResProgram object with attributes based on an HBE-Room."""
        obj = cls()

        # -- type Alias
        rm_prop_energy = getattr(_hb_room.properties, "energy")  # type: RoomEnergyProperties

        obj.name = rm_prop_energy.program_type.display_name
        if not isinstance(rm_prop_energy.lighting.schedule, ruleset.ScheduleRuleset):
            raise ValueError(
                "Error: Room Lighting Schedule must be a ScheduleRuleset object."
                "The Lighting Schedule {} from room {} is of type {} which is not compatible wth Honeybee-PH".format(
                    rm_prop_energy.lighting.schedule.display_name,
                    _hb_room.display_name,
                    type(rm_prop_energy.lighting.schedule),
                )
            )
        obj.operating_hours_day = obj._operating_hours_day_from_hb_schedule(rm_prop_energy.lighting.schedule)
        obj.lighting_W_per_m2 = rm_prop_energy.lighting.watts_per_area
        obj.mel_kWh_m2_yr = obj._calc_mel_kWh_per_m2_from_hb_elec(rm_prop_energy.electric_equipment)
        obj.mel_w_m2 = rm_prop_energy.electric_equipment.watts_per_area

        return obj

    def _calc_mel_kWh_per_m2_from_hb_elec(self, _hb_elec_equip):
        # type: (equipment.ElectricEquipment) -> float
        """Returns the total Elec. Equip kWh for an HBE-Electric-Equipment object."""

        # -- Calc annual full-load hours
        if not isinstance(_hb_elec_equip.schedule, ruleset.ScheduleRuleset):
            raise ValueError(
                "Error: Electric Equipment Schedule must be a ScheduleRuleset object."
                "The Electric Equipment Schedule {} is of type {} which is not compatible wth Honeybee-PH".format(
                    _hb_elec_equip.schedule.display_name, type(_hb_elec_equip.schedule)
                )
            )
        annual_full_load_hours = sum(_hb_elec_equip.schedule.values())

        # -- Calc total usage in kWh
        return (_hb_elec_equip.watts_per_area * annual_full_load_hours) / 1000

    def _operating_hours_day_from_hb_schedule(self, _hb_lght_sched):
        # type: (ruleset.ScheduleRuleset) -> float
        """Return a daily operating period (num. hours) from an HB-Lighting-Schedule"""
        operating_frac = sum(_hb_lght_sched.values()) / len(_hb_lght_sched.values())
        return operating_frac * 24

    def __str__(self):
        return "{}(name={})".format(self.__class__.__name__, self.name)

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
        # type: () -> list[str]
        """Returns a text block formatted to match the Phius MF Calculator."""
        return [prog.to_phius_mf_workbook() for prog in self.programs]


class PhiusNonResRoom(object):
    """A single Phius Non-Res Space."""

    def __init__(self):
        self.multiplier = 1
        self.occupancy_sensor = "N"
        self.name = "_unnamed_phius_nonres_room"
        self.reference_floor_area_m2 = 0.0
        self.misc_mel = 0.0  # kWh/yr
        self.program_type = PhiusNonResProgram()

    @property
    def reference_floor_area_ft2(self):
        # type: () -> float
        return self.reference_floor_area_m2 * 10.7639

    @property
    def mel_kWh_yr(self):
        # type: () -> float
        """Total yearly MEL kWh EXCLUDING the Misc MEL"""
        return self.reference_floor_area_m2 * self.program_type.mel_kWh_m2_yr

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
        return (
            self.program_type.usage_days_yr
            * self.program_type.operating_hours_day
            * self.program_type.lighting_W_per_m2
            * self.reference_floor_area_m2
        ) / 1000

    def to_phius_mf_workbook(self):
        # type: () -> str
        """Returns a string representation that matches the Phius MF Calculator."""
        return ",".join(
            [
                str(self.program_type.name),
                "",  # Blank
                "",  # Number
                str(self.name),
                str(self.occupancy_sensor),
                str(self.multiplier),
                str(self.reference_floor_area_ft2),
                str(self.mel_w_m2),
            ]
        )

    def to_phius_mf_workbook_results(self):
        return ",".join(
            [
                str(self.program_type.lighting_W_per_ft2),
                str(self.program_type.usage_days_yr),
                str(self.program_type.operating_hours_day),
                str(self.program_type.mel_kWh_ft2_yr),
                str(self.total_lighting_kWh),
                str(self.mel_kWh_yr),
            ]
        )

    @classmethod
    def from_ph_space(cls, _ph_space):
        # type: (space.Space) -> PhiusNonResRoom
        """Returns a new PhiusNonResSpace with properties based on a PH-Space."""
        obj = cls()

        obj.name = _ph_space.full_name
        obj.reference_floor_area_m2 = _ph_space.weighted_net_floor_area
        if _ph_space.host is not None:
            obj.program_type = PhiusNonResProgram.from_hb_room(_ph_space.host)

        return obj

    def __str__(self):
        return "{}(name={}, program_type={}," "misc_mel={}, ref_floor_area={}m2)".format(
            self.__class__.__name__,
            self.name,
            self.program_type,
            self.misc_mel,
            self.reference_floor_area_m2,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
