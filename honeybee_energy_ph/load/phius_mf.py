# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Classes and functions for calculating Phius Multifamily Elec. Energy"""

from collections import defaultdict
from honeybee import room


class PhiusResidentialStory(object):
    """Represents one Residential Story of the Phius Multifamily Calculator"""

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


def sort_rooms_by_story(_hb_rooms):
    # type (list[room.Room]) -> list[list[room.Room]]
    """Returns lists of the rooms, organized by their Honeybee 'story'.

    Arguments:
    ----------
        * _hb_rooms (list[room.Room]):

    Returns:
    --------
        * list[list[room.Room]]: 
    """

    d = defaultdict(list)
    for rm in _hb_rooms:
        d[rm.story].append(rm)
    return [d[story_key] for story_key in sorted(d.keys())]


# --- Error Checking


def stories_error(_hb_rooms):
    # type (list[room.Room]) -> bool
    """Check that all the Honeybee-Rooms have a Honeybee-Story attribute."""
    try:
        stories = {rm.story for rm in _hb_rooms}
        if len(stories) < 2:
            return True
        else:
            return False
    except AttributeError as e:
        return True


def spaces_error(_hb_rooms_by_story):
    # type: (list[list[room.Room]]) -> room.Room | None
    """Check if all the Honeybee-Rooms have PH Spaces applied."""
    for story in _hb_rooms_by_story:
        for rm in story:
            if len(rm.properties.ph.spaces) == 0:
                return rm
    return None


def people_error(_hb_rooms_by_story):
    # type: (list[list[room.Room]]) -> room.Room | None
    """Checks that all the HB rooms have a 'People' HBE property applied"""
    for story in _hb_rooms_by_story:
        for rm in story:
            if rm.properties.energy.people is None:
                return rm
    return None
