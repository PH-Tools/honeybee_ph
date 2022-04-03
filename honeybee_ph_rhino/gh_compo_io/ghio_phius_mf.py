# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for organizing inputs to Phius Multifamily Elec. Energy"""

from honeybee import room
from collections import defaultdict

try:
    import Grasshopper.Kernel as ghK
except ImportError:
    pass


def stories_error(_hb_rooms):
    # type (list[room.Room]) -> bool
    """Returns False if HBE-Stories are less than 2."""
    try:
        stories = {rm.story for rm in _hb_rooms}
        if len(stories) < 2:
            return True
        else:
            return False
    except AttributeError as e:
        return True


def spaces_error(_hb_rooms):
    # type: (list[room.Room]) -> room.Room | bool
    """Returns any Honeybee Room which does not have PH-Spaces."""
    for rm in _hb_rooms:
        if len(rm.properties.ph.spaces) == 0:
            return rm
    return False


def people_error(_hb_rooms):
    # type: (list[room.Room]) -> room.Room | bool
    """Returns any room that does not have the 'People' HBE property applied."""
    for rm in _hb_rooms:
        if rm.properties.energy.people is None:
            return rm
    return False


def check_inputs(_hb_rooms, _ghenv):
    # type: (list[room.Room], ghenv) -> None
    """Validate the input Honeybee-Rooms.

    Arguments:
    ----------
        * _hb_rooms (list[room.Room]): A list of the honeybee-rooms to use.
        * _ghenv (ghenv): The Grasshopper Component ghenv for displaying warnings.

    Returns:
    --------
        * None
    """

    # -- Check the HBE-Stories
    if stories_error(_hb_rooms):
        msg = "Warning: It appears that there is only 1 Honeybee-Story assigned to the "\
            "Honeybee-Rooms? If that is true, ignore this warning. Otherwise, check that you "\
            "have used the Honeybee 'Set Story' component to properly assign story ID numbers "\
            "to each of the rooms in the project. This calculator sorts the rooms by story, "\
            "so it is important to set the story attribute before using this component."
        _ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)
        print(msg)

    # -- Check that al the rooms have "PH-Spaces"
    rm_with_error = spaces_error(_hb_rooms)
    if rm_with_error:
        msg = "Error: There are no PH-Spaces assigned to room: '{}'. Please be sure to assign the "\
            "PH-Spaces before using this component. Use the HB-PH 'Create Spaces' and 'Add Spaces' "\
            "components in order to add Spaces to all the Honeybee-Rooms.".format(
                rm_with_error.display_name)
        _ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Error, msg)
        print(msg)

    # -- Check that all the rooms have a "People"
    rm = people_error(_hb_rooms)
    if rm_with_error:
        msg = "Error: There is no 'People' property assigned to room: '{}'. Be sure to use "\
            "the HB-PH 'Set Occupancy' component to assign the number of bedrooms per-HB-Room "\
            "before using this calculator.".format(rm_with_error.display_name)
        _ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Error, msg)
        print(msg)


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
