from functools import partial
from collections import defaultdict
from functools import reduce
from honeybee_ph_rhino.gh_io import clean_get, IGH
import honeybee_ph.space


def create_volumes(_floor_segments, _heights):
    # type (list, list) -> list[honeybee_ph.space.SpaceVolume]
    volumes = []
    for i, flr_seg in enumerate(_floor_segments):
        new_volume = honeybee_ph.space.SpaceVolume()

        new_volume.floor.floor_segments.append(flr_seg)
        new_volume.avg_ceiling_height = clean_get(_heights, i, 2.5)

        volumes.append(new_volume)
    return volumes


def create_spaces(_volumes, _space_names, _space_numbers):
    # type: (list, list, list) -> list
    spaces = []
    for i, volume in enumerate(_volumes):
        space = honeybee_ph.space.Space()

        space.volumes.append(volume)
        space.name = clean_get(_space_names, i, 'unnamed_room_{}'.format(i))
        space.number = clean_get(_space_numbers, i, '00')

        spaces.append(space)

    return spaces


def merge_spaces(IGH, space_1, space_2):
    # type: (IGH, honeybee_ph.space.Space, honeybee_ph.space.Space) -> honeybee_ph.space.Space
    """Combine two Spaces into a single new space."""

    # TODO: Merge Spaces, join Floor Surfaces, etc...

    return honeybee_ph.space.Space()


def merge_spaces_by_name(IGH, _spaces):
    # type: (IGH, list[honeybee_ph.space.Space]) -> list[honeybee_ph.space.Space]

    # -- Group the spaces by full-name. ie: "101-Kitchen", etc
    space_groups = defaultdict(list)
    for space in _spaces:
        space_groups[space.full_name].append(space)

    # -- Merge the groups of spaces together
    # -- Note: Pass the IGH to merge ahead of time uing partial since
    # -- reduce requires a two-argument function.
    _merge_with_IGH = partial(merge_spaces, IGH)
    spaces_ = []
    for space_group in space_groups.values():
        spaces_.append(reduce(_merge_with_IGH, space_group))

    return spaces_
