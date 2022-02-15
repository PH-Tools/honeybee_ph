# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to convert a standard HBJSON Model over to WUFI Objects"""

from collections import defaultdict

from honeybee import model
from honeybee import room

from PHX.project import Project
from from_HBJSON import create_assemblies, create_variant, merge
from from_HBJSON import create_schedules


class MissingPropertiesError(Exception):
    def __init__(self, _lbt_obj):
        self.message = (f'Error: LBT Object "{_lbt_obj}" does not have a .properties attribute?\n'
                        'Can not add the .ph to missing .properties attribute.')
        super().__init__(self.message)


def sort_hb_rooms_by_bldg_segment(_hb_rooms: tuple[room.Room]) -> list[list[room.Room]]:
    """Returns Groups of Honeybee-Rooms broken up by properties.ph.ph_bldg_segment.identifier.

    Arguments:
    ----------
        * _hb_rooms (list[room.Room]): The list of Honeybee Rooms to sort into bins.

    Returns:
    --------
        * list[list[room.Room]]: A list of the groups of Honeybee Rooms.
    """

    rooms_by_segment = defaultdict(list)
    for room in _hb_rooms:
        rooms_by_segment[room.properties.ph.ph_bldg_segment.identifier].append(room)

    return list(rooms_by_segment.values())


def convert_HB_model_to_WUFI_Project(_hb_model: model.Model, group_components: bool = False) -> Project:
    """Return a complete WUFI Project object with values based on the HB Model

    Arguments:
    ----------
        * _hb_model (model.Model): The Honeybee Model to base the WUFI Project on
        * group_components (bool): defauly=False. Set to true to have the converter
            group the components by assembly-type.

    Returns:
    --------
        * (Project): The new WUFI Project object. 
    """

    project = Project()
    create_assemblies.build_opaque_assemblies_from_HB_model(project, _hb_model)
    create_assemblies.build_transparent_assemblies_from_HB_Model(project, _hb_model)
    create_schedules.build_util_patterns_ventilation_from_HB_Model(project, _hb_model)

    # -- Merge the rooms together by their Building Segment, Add to the Project
    for room_group in sort_hb_rooms_by_bldg_segment(_hb_model.rooms):
        merged_hb_room = merge.merge_rooms(room_group)
        new_variant = create_variant.from_hb_room(merged_hb_room, group_components)
        project.add_new_variant(new_variant)

    return project
