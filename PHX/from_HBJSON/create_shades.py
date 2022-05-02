# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create new PHX-Shades from HB-Model Orphaned-Shade Objects."""

from honeybee import model, shade
from PHX.model import project
from PHX.model import building
from PHX.from_HBJSON import create_geometry


def _add_shade_geometry_from_model(_var: project.PhxVariant, _hb_model: model.Model) -> None:
    """Creates new PHX Polygons for the shades and adds them to the PHX-Variant.graphics3D

    Arguments:
    ----------
        * _var (project.Variant): The PHX-Variant to add the Shading Objects to.
        * _hb_model (model.Model): The Honeybee-Model to get the orphaned shades from.

    Returns:
    --------
        * None
    """

    for hb_shade_face in _hb_model.orphaned_shades:
        new_shade = create_geometry.create_PHX_Polygon_from_hb_shade(hb_shade_face)
        _var.graphics3D.add_polygons(new_shade)

    return None


def _create_new_component_from_orphaned_shade(_shade: shade.Shade) -> building.PhxComponent:
    """Returns a new PHX-Component for based on the Honeybee-Shade.

    Arguments:
    ----------
        * _shade (shade.Shade): The Honeybee-Shade to base the new component on.

    Returns:
    --------
        * building.Component: A new PHX-Component for the HB-Shade.
    """

    new_compo = building.PhxComponent()

    new_compo.display_name = _shade.display_name
    new_compo.id_num = building.PhxComponent._count

    new_compo.face_type = 1  # Opaque

    new_compo.exposure_exterior = -1
    new_compo.exposure_interior = -1
    new_compo.color_interior = 1  # Ext wall, inner surface
    new_compo.color_exterior = 1  # Ext wall, inner surface

    new_compo.add_polygon_id(_shade.properties.ph.id_num)

    return new_compo


def _add_shade_compos_from_model(_var: project.PhxVariant, _hb_model: model.Model) -> None:
    """Creates new PHX-Components for the shades and adds them to the PHX-Variant.building.components

    Arguments:
    ----------
        * _var (project.Variant): The PHX-Variant to add the Shading Objects to.
        * _hb_model (model.Model): The Honeybee-Model to get the orphaned shades from.

    Returns:
    --------
        * None
    """

    for shade in _hb_model.orphaned_shades:
        new_shade_compo = _create_new_component_from_orphaned_shade(shade)
        _var.building.add_components(new_shade_compo)

    return None


def add_model_shades_to_variant(_var: project.PhxVariant, _hb_model: model.Model) -> None:
    """"Create shading objects from model orphaned shades and add to the PHX-Variant.

    Arguments:
    ----------
        * _var (project.Variant): The PHX-Variant to add the Shading Objects to.
        * _hb_model (model.Model): The Honeybee-Model to get the orphaned shades from.

    Returns:
    --------
        * None
    """

    # Dev Note: To get the right IDs, have to generate the Polygons first.
    _add_shade_geometry_from_model(_var, _hb_model)
    _add_shade_compos_from_model(_var, _hb_model)

    return None
