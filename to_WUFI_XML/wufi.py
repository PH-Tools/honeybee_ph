# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""WUFI XML classes"""

from __future__ import annotations
from typing import Any, ClassVar
from dataclasses import dataclass, field

from honeybee.model import Model as HB_Model
from honeybee.room import Room as HB_Room
from honeybee.face import Face as HB_Face
from honeybee.aperture import Aperture as HB_Aperture
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass

from ladybug_geometry_ph.geometry3d_ph.pointvector import PHX_Vertix

# -- Constructions, Assemblies, Materials


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
    material: Material = Material()

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
            obj.material.conductivity = Layer._conductivity_from_r_value(_hb_material.r_value, obj.thickness)
            obj.material.density = _hb_material.mass_area_density
            obj.material.heat_capacity = _hb_material.area_heat_capacity

            # -- Defaults
            obj.material.water_vapor_resistance = 1.0
            obj.material.porosity = 0.95
            obj.material.reference_water = 0.0

        else:
            raise TypeError(f"Unrecognized Material type: {type(_hb_material)}.")

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
        obj.layers = [Layer.from_hb_material(layer) for layer in _hb_const.materials]

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


# -- Geometry
@dataclass
class Vertix:
    _count: ClassVar[int] = 0
    id_num: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_LBT_P3D(cls, _lbt_Point3D: PHX_Vertix):
        obj = cls()

        obj.id_num = cls._count
        _lbt_Point3D.properties._PH.id_num = obj.id_num

        obj.x = _lbt_Point3D.x
        obj.y = _lbt_Point3D.y
        obj.z = _lbt_Point3D.z

        return obj

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Vertix, cls).__new__(cls, *args, **kwargs)


@dataclass
class Polygon:
    _count: ClassVar[int] = 0
    id_num: int = 0
    normal_vector: Any = None
    vertices: list[Vertix] = field(default_factory=list)
    child_polygon_ids: list[int] = field(default_factory=list)

    @property
    def vertices_id_numbers(self) -> list[int]:
        return [v.id_num for v in self.vertices]

    @classmethod
    def from_HB_Face(cls, _hb_face: HB_Face):
        obj = cls()

        obj.id_num = cls._count
        _hb_face.properties._PH.id_num = obj.id_num
        obj.normal_vector = _hb_face.normal
        obj.vertices = [Vertix.from_LBT_P3D(v) for v in _hb_face.vertices]
        obj.child_polygon_ids = [aperture.properties._PH.id_num for aperture in _hb_face.apertures]

        return obj

    @classmethod
    def from_HB_Aperture(cls, _hb_aperture: HB_Aperture):
        obj = cls()

        obj.id_num = cls._count
        _hb_aperture.properties._PH.id_num = obj.id_num
        obj.normal_vector = _hb_aperture.normal
        obj.vertices = [Vertix.from_LBT_P3D(v) for v in _hb_aperture.vertices]

        return obj

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Polygon, cls).__new__(cls, *args, **kwargs)


@dataclass
class Graphics3D:
    polygons: list[Polygon] = field(default_factory=list)

    @property
    def vertices(self):
        return [vertix for polygon in self.polygons for vertix in polygon.vertices]


# -- Building
@dataclass
class Zone:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> Zone:
        obj = cls()

        obj.id_num = cls._count
        obj.name = _hb_room.display_name

        return obj


@dataclass
class Component:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    type: int = 1
    color_interior: int = 1
    color_exterior: int = 1
    exposure_exterior: int = -1
    exposure_interior: int = 1
    interior_attachment_id: int = -1
    assembly_type_id_num: int = -1
    window_type_id_num: int = -1
    polygon_ids: list[int] = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Component, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_opaque_face(cls, _hb_face: HB_Face, _hb_room: HB_Room) -> Component:
        """Returns a new Component based on a Honeybee Face"""
        obj = cls()

        obj.name = _hb_face.display_name
        obj.id_num = cls._count

        obj.type = obj.hb_face_type_to_WUFI(_hb_face)
        obj.exposure_exterior = obj.hb_face_exposure_ext_to_WUFI(_hb_face)
        obj.exposure_interior = obj.hb_face_exposure_int_to_WUFI(_hb_room)
        obj.color_interior = obj.int_color_by_hb_face(_hb_face)
        obj.color_exterior = obj.ext_color_by_hb_face(_hb_face)
        obj.assembly_type_id_num = _hb_face.properties.energy.construction.properties._PH.id_num

        obj.polygon_ids = [_hb_face.properties._PH.id_num]

        return obj

    @classmethod
    def from_aperture(cls, _aperture: HB_Aperture, _hb_room: HB_Room) -> Component:
        """Create a new Component based on a Honeybee Aperture."""
        obj = cls()

        obj.name = _aperture.display_name
        obj.id_num = cls._count

        obj.type = 2  # Transparent
        obj.exposure_exterior = obj.hb_face_exposure_ext_to_WUFI(_aperture)
        obj.exposure_interior = obj.hb_face_exposure_int_to_WUFI(_hb_room)
        obj.color_interior = 4  # Window
        obj.color_exterior = 4  # Window
        obj.window_type_id_num = _aperture.properties.energy.construction.properties._PH.id_num

        obj.polygon_ids = [_aperture.properties._PH.id_num]

        return obj

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> list[Component]:
        """Returns a list of new Components based on the Room's Opaque Faces and Apertures."""

        compos = []
        for hb_face in _hb_room:
            for aperture in hb_face.apertures:
                compos.append(cls.from_aperture(aperture, _hb_room))

            compos.append(cls.from_opaque_face(hb_face, _hb_room))

        return compos

    def hb_face_type_to_WUFI(self, _hb_face: HB_Face) -> int:
        """Return a WUFI-Type ID for the Component."""

        schema = {
            "Wall": 1,
            "RoofCeiling": 1,
            "Floor": 1,
            "AirBoundary": 3,
        }

        return schema.get(str(_hb_face.type), 1)

    def hb_face_exposure_ext_to_WUFI(self, _hb_face: HB_Face) -> int:
        """Return the ID number of the Exterior-Expsoure Zone for the Component."""
        schema = {
            "Outdoors": -1,
            "Ground": -2,
            "Surface": -3,
        }
        return schema.get(str(_hb_face.boundary_condition), -1)

    def hb_face_exposure_int_to_WUFI(self, _hb_room: HB_Room) -> int:
        """Return the ID number of the Interior-Exposure Zone for the Component."""
        return _hb_room.properties._PH.id_num

    def int_color_by_hb_face(self, _hb_face: HB_Face) -> int:
        """Return the ID number of the WUFI Standard color to use for the Compo."""

        schema = {
            "Wall": {
                "Outdoors": 1,
                "Surface": 3,
                "Ground": 1,
            },
            "RoofCeiling": {
                "Outdoors": 8,
                "Surface": 6,
                "Ground": 12,
            },
            "Floor": {
                "Outdoors": 5,
                "Surface": 5,
                "Ground": 12,
            },
        }

        t = str(_hb_face.type)
        bc = str(_hb_face.boundary_condition)

        return schema.get(t, {}).get(bc, 1)

    def ext_color_by_hb_face(self, _hb_face: HB_Face) -> int:
        """Return the ID number of the WUFI Standard color to use for the Compo."""

        schema = {
            "Wall": {
                "Outdoors": 2,
                "Surface": 3,
                "Ground": 12,
            },
            "RoofCeiling": {
                "Outdoors": 7,
                "Surface": 6,
                "Ground": 12,
            },
            "Floor": {
                "Outdoors": 5,
                "Surface": 5,
                "Ground": 12,
            },
        }

        t = str(_hb_face.type)
        bc = str(_hb_face.boundary_condition)

        return schema.get(t, {}).get(bc, 1)


@dataclass
class Building:
    components: list[Component] = field(default_factory=list)
    zones: list[Zone] = field(default_factory=list)

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> Building:
        obj = cls()
        obj.create_components_from_hb_room(_hb_room)
        obj.create_zones_from_hb_room(_hb_room)

        return obj

    def create_components_from_hb_room(self, _hb_room: HB_Room) -> None:
        self.components = Component.from_hb_room(_hb_room)

    def create_zones_from_hb_room(self, _hb_room: HB_Room) -> None:
        self.zones.append(Zone.from_hb_room(_hb_room))


# --- Variants, Project
@dataclass
class Variant:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = "unnamed_variant"
    remarks: str = ""
    plugin: str = ""
    graphics3D: Graphics3D = field(default_factory=Graphics3D)
    building: Building = field(default_factory=Building)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Variant, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_room(cls, _hb_room: HB_Room) -> Variant:
        """Create a new Variant based on a single PHX/Honeybee Room.

        Arguments:
        ----------
            * _hb_room (honeybee.room.Room): The honeybee room to base the Variant on.

        Returns:
        --------
            * A new Variant object.
        """

        obj = cls()

        obj.id_num = cls._count
        _hb_room.properties._PH.id_num = obj.id_num

        obj.name = _hb_room.display_name

        # -- Build the Variant Elements
        obj.create_geometry_from_hb_room(_hb_room)
        obj.create_building_from_hb_room(_hb_room)

        return obj

    def create_geometry_from_hb_room(self, _hb_room: HB_Room) -> None:
        """Gets all the geometry from an HB Room, adds it to self.graphics3D"""
        for hb_face in _hb_room.faces:
            # Dev Note: To get the right IDs, have to generate the Children Polys first.
            for aperture in hb_face.apertures:
                self.graphics3D.polygons.append(Polygon.from_HB_Aperture(aperture))

            self.graphics3D.polygons.append(Polygon.from_HB_Face(hb_face))

    def create_building_from_hb_room(self, _hb_room: HB_Room) -> None:
        """Create the 'Building' with all Components and Zones."""
        self.building = Building.from_hb_room(_hb_room)


@dataclass
class ProjectData_Agent:
    name: str = ""
    street: str = ""
    city: str = ""
    post_code: str = ""
    telephone: str = ""
    email: str = ""
    license_number = ""


@dataclass
class ProjectData:
    customer: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    building: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    owner: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    responsible: ProjectData_Agent = field(default_factory=ProjectData_Agent)

    project_date: str = ""
    owner_is_client: bool = False
    year_constructed: int = 0
    image: None = None


@dataclass
class Project:
    name: str = "unnamed_project"

    _assembly_types: dict[str, Assembly] = field(default_factory=dict)
    _window_types: dict[str, Any] = field(default_factory=dict)
    utilisation_patterns_ventilation: list = field(default_factory=list)
    utilisation_patterns_ph: list = field(default_factory=list)
    variants: list = field(default_factory=list)

    project_data: ProjectData = field(default_factory=ProjectData)

    data_version: int = 48
    unit_system: int = 1
    program_version: str = "3.2.0.1"
    scope: int = 3
    visualized_geometry: int = 2

    def add_opaque_assemblies_from_HB_model(self, _hb_model: HB_Model) -> None:
        """Adds all of an HB Model's Opaque Constructions to the Project's _assembly_types dict

        Will also align the id_nums of the face's Construction with the Assembly in the Project dict.

        Arguments:
        ----------
            * _hb_model (HB_Model): The Honeybee Model to use as the source.

        Returns:
        --------
            * None
        """

        for room in _hb_model.rooms:
            for face in room.faces:
                hb_const = face.properties.energy.construction

                if hb_const.identifier not in self._assembly_types.keys():
                    self._assembly_types[hb_const.identifier] = Assembly.from_HB_OpaqueConstruction(hb_const)

                hb_const.properties._PH.id_num = self._assembly_types[hb_const.identifier].id_num

        return None

    def add_transparent_assemblies_from_HB_Model(self, _hb_model: HB_Model) -> None:
        """Adds all of the Transparent (window) Constructions from a HB Model the Project's _window_types dict

        Will also align the id_nums of the Aperture Construction's with the WindowType in the Project dict.

        Arguments:
        ----------
            * _hb_model (HB_Model): The Honeybee Model to use as the source.

        Returns:
        --------
            * None
        """

        for room in _hb_model.rooms:
            for face in room.faces:
                for aperture in face._apertures:
                    aperture_const = aperture.properties.energy.construction

                    if aperture_const.identifier not in self._window_types.keys():
                        self._window_types[aperture_const.identifier] = WindowType.from_HB_WindowConstruction(
                            aperture_const
                        )

                    aperture_const.properties._PH.id_num = self._window_types[aperture_const.identifier].id_num

        return

    @property
    def assembly_types(self):
        return self._assembly_types.values()

    @property
    def window_types(self):
        return self._window_types.values()
