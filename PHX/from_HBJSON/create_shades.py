# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create new Shade PhxComponents from HB-Model Orphaned-Shade Objects."""

from honeybee import model, shade

from PHX.model import components, project
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceOpacity, ComponentColor
from PHX.from_HBJSON import create_geometry


def create_new_component_from_orphaned_shade(_shade: shade.Shade) -> components.PhxComponentOpaque:
    """Returns a new PHX-Component for based on the Honeybee-Shade.

    Arguments:
    ----------
        * _shade (shade.Shade): The Honeybee-Shade to base the new component on.

    Returns:
    --------
        * (components.PhxComponentOpaque): A new PHX-Component for the HB-Shade.
    """

    new_compo = components.PhxComponentOpaque()

    new_compo.display_name = _shade.display_name
    new_compo.face_opacity = ComponentFaceOpacity.OPAQUE
    new_compo.exposure_exterior = ComponentExposureExterior.EXTERIOR
    new_compo.exposure_interior = -1
    new_compo.color_interior = ComponentColor.EXT_WALL_INNER
    new_compo.color_exterior = ComponentColor.EXT_WALL_INNER

    # -- Polygons
    phx_polygon = create_geometry.create_PhxPolygon_from_hb_shade(_shade)
    new_compo.add_polygons(phx_polygon)

    return new_compo


def add_hb_model_shades_to_variant(_var: project.PhxVariant, _hb_model: model.Model) -> None:
    """"Create shading PhxComponents from an HB-model's orphaned shades and add to the PhxVariant.

    Arguments:
    ----------
        * _var (project.Variant): The PhxVariant to add the Shading Objects to.
        * _hb_model (model.Model): The Honeybee-Model to get the orphaned shades from.

    Returns:
    --------
        * None
    """

    for hb_shade_face in _hb_model.orphaned_shades:
        _var.building.add_components(
            create_new_component_from_orphaned_shade(hb_shade_face)
        )

    return None
