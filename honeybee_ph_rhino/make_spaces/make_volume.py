# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create SpaceVolume objects from Rhino/Grasshopper inputs."""

from honeybee_ph import space
from honeybee_ph_rhino import gh_io


def volumes_from_floors(IGH, _floors, _heights):
    # type: (gh_io.IGH, list[space.SpaceFloor], list[float]) -> list[space.SpaceVolume]
    """Create new SpaceVolume objects based on a list of input SpaceFloors.

    Arguments:
    ----------
        * IGH (gh_io.IGH): Honeybee-PH Grasshopper Interface Object.
        * _floors ([list[space.SpaceFloor]): A list of SpaceFloor objects to 
            build the volumes from.
        * _heights (list[float]): A list of heights to extrude the Volume to.

    Returns:
    --------
        * list[space.SpaceVolumes]: A list of new SpaceVolume objects.
    """

    volumes = []
    for i, flr in enumerate(_floors):
        # -- Set up some of the variables
        height = gh_io.clean_get(_heights, i, 2.5)
        geom = IGH.extrude_Face3D_WorldZ(flr.geometry, height)

        # -- Build the new SpaceVolume
        new_volume = space.SpaceVolume()
        new_volume.floor = flr
        new_volume.avg_ceiling_height = height
        new_volume.geometry = geom

        volumes.append(new_volume)

    return volumes
