# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Construction, Materials Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field

from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass


@dataclass
class Material:
    name: str = ""
    conductivity: float = 0.0
    density: float = 0.0
    porosity: float = 0.0
    heat_capacity: float = 0.0
    water_vapor_resistance: float = 0.0
    reference_water: float = 0.0


@dataclass
class Layer:
    thickness: float = 0.0
    material: Material = field(default_factory=Material)

    @classmethod
    def from_hb_material(cls, _hb_material: (EnergyMaterial | EnergyMaterialNoMass)) -> Layer:
        obj = cls()

        if isinstance(_hb_material, EnergyMaterial):
            obj.thickness = _hb_material.thickness
            obj.material.conductivity = _hb_material.conductivity
            obj.material.density = _hb_material.density
            obj.material.heat_capacity = _hb_material.specific_heat

            # -- Defaults
            obj.material.porosity = 0.95
            obj.material.water_vapor_resistance = 1.0
            obj.material.reference_water = 0.0

        elif isinstance(_hb_material, EnergyMaterialNoMass):
            obj.thickness = 0.1  # m = 4". Use as default since No-Mass has no thickness
            obj.material.conductivity = Layer._conductivity_from_r_value(
                _hb_material.r_value, obj.thickness)
            obj.material.density = _hb_material.mass_area_density
            obj.material.heat_capacity = _hb_material.area_heat_capacity

            # -- Defaults
            obj.material.water_vapor_resistance = 1.0
            obj.material.porosity = 0.95
            obj.material.reference_water = 0.0

        else:
            raise TypeError(
                f"Unrecognized Material type: {type(_hb_material)}.")

        return obj

    @staticmethod
    def _conductivity_from_r_value(_r_value: float, _thickness: float) -> float:
        """Returns a conductivity value, given a known r-value and thickness"""
        conductance = 1 / _r_value
        conductivity = conductance / _thickness
        return conductivity


@dataclass
class Assembly:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    layer_order: int = 2  # Outside to Inside
    grid_kind: int = 2  # Medium
    layers: list[Layer] = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Assembly, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_HB_OpaqueConstruction(cls, _hb_const: OpaqueConstruction) -> Assembly:
        obj = cls()
        obj.id_num = cls._count
        obj.name = _hb_const.display_name
        obj.layers = [Layer.from_hb_material(
            layer) for layer in _hb_const.materials]

        return obj


@dataclass
class WindowType:
    _count = 0
    id_num: int = 0
    name: str = ""

    use_detailed_uw: bool = True
    use_detailed_frame: bool = False

    u_value_window: float = 1.0
    u_value_glass: float = 1.0
    u_value_frame: float = 1.0

    frame_width_left: float = 0.1
    frame_psi_g_left: float = 0.1
    frame_psi_inst_left: float = 0.1
    frame_u_value_left: float = 1.0
    frame_factor: float = 0.75

    glass_mean_emissivity: float = 0.1
    glass_g_value: float = 0.4

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(WindowType, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_HB_WindowConstruction(cls, _hb_aperture_const) -> WindowType:
        obj = cls()
        obj.id_num = cls._count
        obj.name = _hb_aperture_const.display_name

        # TODO: Convert HB Values into WUFI-speak

        return obj
