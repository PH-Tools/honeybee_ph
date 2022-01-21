# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to create Project elements from the Honeybee-Model"""

from honeybee import model
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from PHX import constructions


def _conductivity_from_r_value(_r_value: float, _thickness: float) -> float:
    """Returns a conductivity value, given a known r-value and thickness

    Arguments:
    ----------
        * _r_value (float): The total R-Value of the layer.
        * _thickness (float): The total thickness of the layer.

    Returns:
    --------
        * float: The Conductivity value of the layer.
    """
    conductivity = _thickness / _r_value
    return conductivity


def build_layer_from_hb_material(_hb_material: (EnergyMaterial | EnergyMaterialNoMass)) -> constructions.Layer:
    """Returns a new PHX-Layer with attributes based on a Honeybee-Material.

    Arguments:
    ----------
        *_hb_material (EnergyMaterial | EnergyMaterialNoMass): The Honeybee Material.

    Returns:
    --------
        * constructions.Layer: The new PHX-Layer object.
    """
    new_layer = constructions.Layer()

    if isinstance(_hb_material, EnergyMaterial):
        new_layer.thickness = _hb_material.thickness
        new_layer.material.conductivity = _hb_material.conductivity
        new_layer.material.density = _hb_material.density
        new_layer.material.heat_capacity = _hb_material.specific_heat

        # -- Defaults
        new_layer.material.porosity = 0.95
        new_layer.material.water_vapor_resistance = 1.0
        new_layer.material.reference_water = 0.0

    elif isinstance(_hb_material, EnergyMaterialNoMass):
        new_layer.thickness = 0.1  # m = 4". Use as default since No-Mass has no thickness
        new_layer.material.conductivity = _conductivity_from_r_value(
            _hb_material.r_value, new_layer.thickness)
        new_layer.material.density = _hb_material.mass_area_density
        new_layer.material.heat_capacity = _hb_material.area_heat_capacity

        # -- Defaults
        new_layer.material.water_vapor_resistance = 1.0
        new_layer.material.porosity = 0.95
        new_layer.material.reference_water = 0.0

    else:
        raise TypeError(
            f"Unrecognized Material type: {type(_hb_material)}.")

    return new_layer


def build_opaque_assemblies_from_HB_model(_project, _hb_model: model.Model) -> None:
    """Build Opaque Constructions from Honeybee Faces and add to the PHX-Project.

    Will also align the id_nums of the face's Construction with the Assembly in the Project dict.

    Arguments:
    ----------
        * _hb_model (model.Model): The Honeybee Model to use as the source.

    Returns:
    --------
        * None
    """

    for room in _hb_model.rooms:
        for face in room.faces:
            hb_const = face.properties.energy.construction

            if not _project.assembly_in_project(hb_const.identifier):
                # -- Create a new Assembly with Layers from the Honeybee-Construction
                new_assembly = constructions.Assembly()
                new_assembly.id_num = constructions.Assembly._count
                new_assembly.name = hb_const.display_name
                new_assembly.layers = [build_layer_from_hb_material(layer)
                                       for layer in hb_const.materials]

                # -- Add the assembly to the Project
                _project.add_new_assembly(hb_const.identifier, new_assembly)

            hb_const.properties._ph.id_num = _project._assembly_types[hb_const.identifier].id_num

    return None


def build_transparent_assemblies_from_HB_Model(_project, _hb_model: model.Model) -> None:
    """Create Transparent Constructions from an HB Model and add to the PHX-Project

    Will also align the id_nums of the Aperture Construction's with the WindowType in the Project dict.

    Arguments:
    ----------
        * _hb_model (model.Model): The Honeybee Model to use as the source.

    Returns:
    --------
        * None
    """

    for room in _hb_model.rooms:
        for face in room.faces:
            for aperture in face._apertures:
                aperture_const = aperture.properties.energy.construction

                if aperture_const.identifier not in _project._window_types.keys():
                    new_aperture_constr = constructions.WindowType()
                    new_aperture_constr.id_num = constructions.WindowType._count
                    new_aperture_constr.name = aperture_const.display_name

                    # TODO: Convert the other HB Values into WUFI-speak

                    _project._window_types[aperture_const.identifier] = new_aperture_constr

                aperture_const.properties._ph.id_num = _project._window_types[
                    aperture_const.identifier].id_num

    return None
