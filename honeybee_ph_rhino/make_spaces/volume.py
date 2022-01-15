# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create SpaceVolume objects from Rhino/Grasshopper inputs."""

from honeybee_ph import space
from honeybee_ph_rhino import gh_io
from ladybug_geometry.geometry3d.face import Face3D


def create_volume_geometry(IGH, _volume):
    # type: (gh_io.IGH, space.SpaceVolume) -> list[Face3D]
    volume_geometry = IGH.extrude_Face3D_WorldZ(
        _volume.floor.geometry, _volume.avg_ceiling_height)

    return volume_geometry


def volumes_from_floors(IGH, _floors, _heights):
    # type: (gh_io.IGH, list[space.SpaceFloor], list[float]) -> list[space.SpaceVolume]
    """

    Arguments:
    ----------
        * IGH (gh_io.IGH): Honeybee-PH Grasshopper Interface Object.
        * _floors ([list[space.SpaceFloor]):
        * _heights ():

    Returns:
    --------
        * list[space.SpaceVolumes]
    """

    volumes = []
    for i, flr in enumerate(_floors):
        new_volume = space.SpaceVolume()
        new_volume.floor = flr
        new_volume.avg_ceiling_height = gh_io.clean_get(_heights, i, 2.5)
        new_volume.geometry = create_volume_geometry(IGH, new_volume)
        volumes.append(new_volume)

    return volumes
