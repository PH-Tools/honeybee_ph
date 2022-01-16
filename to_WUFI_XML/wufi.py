# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""WUFI XML classes.

The data classes here match the strucure and relationships of the WUFI file and are created at write-time from the 
Honeybee model objects. The WUFI structure differs significantly from the Honeybee Model structure and so many 
translations and conversions need to take place. The objects here are subsequently passed along to the xml_schemas 
for writing to file, and these xml-schemas contain the actual WUFI XML node names and ordering.
"""

from __future__ import annotations
from typing import Any, ClassVar
from dataclasses import dataclass, field

from honeybee.model import Model as HB_Model
from honeybee.room import Room as HB_Room
from honeybee.face import Face as HB_Face
from honeybee.aperture import Aperture as HB_Aperture
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass

from ladybug_geometry_ph.geometry3d_ph.pointvector import PH_Point3D

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# -- Geometry


@dataclass
class Vertix:
    _count: ClassVar[int] = 0
    id_num: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_LBT_P3D(cls, _lbt_Point3D: PH_Point3D):
        obj = cls()

        obj.id_num = cls._count
        _lbt_Point3D.properties._ph.id_num = obj.id_num

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
        _hb_face.properties._ph.id_num = obj.id_num
        obj.normal_vector = _hb_face.normal
        obj.vertices = [Vertix.from_LBT_P3D(v) for v in _hb_face.vertices]
        obj.child_polygon_ids = [
            aperture.properties._ph.id_num for aperture in _hb_face.apertures]

        return obj

    @classmethod
    def from_HB_Aperture(cls, _hb_aperture: HB_Aperture):
        obj = cls()

        obj.id_num = cls._count
        _hb_aperture.properties._ph.id_num = obj.id_num
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

# -----------------------------------------------------------------------------
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
        obj.assembly_type_id_num = _hb_face.properties.energy.construction.properties._ph.id_num

        obj.polygon_ids = [_hb_face.properties._ph.id_num]

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
        obj.window_type_id_num = _aperture.properties.energy.construction.properties._ph.id_num

        obj.polygon_ids = [_aperture.properties._ph.id_num]

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
        return _hb_room.properties._ph.id_num

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

# -----------------------------------------------------------------------------
# --- PH Certification


@dataclass
class PH_Building:
    _count: ClassVar[int] = 0
    building_category: int = 1
    occupancy_type: int = 1
    building_status: int = 1
    building_type: int = 1
    num_of_units: int = 1
    num_of_floors: int = 1
    occupancy_setting_method: int = 2  # Design
    airtightness_q50: float = 0.2  # m3/hr-m2-envelope

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PH_Building, cls).__new__(cls, *args, **kwargs)


@dataclass
class PassivehouseData:
    ph_certificate_criteria: int = 3
    ph_selection_target_data: int = 2
    annual_heating_demand: float = 15.0
    annual_cooling_demand: float = 15.0
    peak_heating_load: float = 10.0
    peak_cooling_load: float = 10.0
    ph_buildings: list[PH_Building] = field(default_factory=list)

# -----------------------------------------------------------------------------
# -- Climate


@dataclass
class Ground:
    ground_thermal_conductivity: float = 2
    ground_heat_capacitiy: float = 1000
    ground_density: float = 2000
    depth_groundwater: float = 3
    flow_rate_groundwater: float = 0.05


@dataclass
class Location:
    latitude: float = 40.6
    longitude: float = -73.8
    weather_station_elevation: float = 3.0
    climate_zone: int = 1
    hours_from_UTC: int = -4


@dataclass
class PeakLoad:
    temp: float = 0
    rad_north: float = 0
    rad_east: float = 0
    rad_south: float = 0
    rad_west: float = 0
    rad_global: float = 0


@dataclass
class PH_ClimateLocation:
    selection: int = 6
    selection_pe_co2_factor: int = 1
    daily_temp_swing: float = 8.0
    avg_wind_speed: float = 4.0
    location: Location = field(default_factory=Location)
    ground: Ground = field(default_factory=Ground)

    monthly_temperature_air: list[float] = field(default_factory=list)
    monthly_temperature_dewpoint: list[float] = field(default_factory=list)
    monthly_temperature_sky: list[float] = field(default_factory=list)

    monthly_radiation_north: list[float] = field(default_factory=list)
    monthly_radiation_east: list[float] = field(default_factory=list)
    monthly_radiation_south: list[float] = field(default_factory=list)
    monthly_radiation_west: list[float] = field(default_factory=list)
    monthly_radiation_global: list[float] = field(default_factory=list)

    peak_heating_1: PeakLoad = field(default_factory=PeakLoad)
    peak_heating_2: PeakLoad = field(default_factory=PeakLoad)
    peak_cooling_1: PeakLoad = field(default_factory=PeakLoad)
    peak_cooling_2: PeakLoad = field(default_factory=PeakLoad)


@dataclass
class ClimateLocation:
    selection: int = 1
    ph_climate_location: PH_ClimateLocation = field(default_factory=PH_ClimateLocation)

# -----------------------------------------------------------------------------
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
    ph_data: PassivehouseData = field(default_factory=PassivehouseData)
    climate: ClimateLocation = field(default_factory=ClimateLocation)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Variant, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_room(cls, _hb_room: HB_Room) -> Variant:
        """Create a new Variant based on a single PH/Honeybee Room.

        Arguments:
        ----------
            * _hb_room (honeybee.room.Room): The honeybee room to base the Variant on.

        Returns:
        --------
            * A new Variant object.
        """

        obj = cls()

        # -- Keep all the ID numbers aligned
        obj.id_num = cls._count
        _hb_room.properties.ph.id_num = obj.id_num
        obj.name = _hb_room.display_name

        # -- Build the Variant Elements
        obj.create_geometry_from_hb_room(_hb_room)
        obj.create_building_from_hb_room(_hb_room)
        obj.create_phius_certification_from_hb_room(_hb_room)
        obj.create_PH_Building_from_hb_room(_hb_room)
        obj.create_climate_from_hb_room(_hb_room)

        return obj

    def create_geometry_from_hb_room(self, _hb_room: HB_Room) -> None:
        """Gets all the geometry from an HB Room, adds it to self.graphics3D"""
        for hb_face in _hb_room.faces:
            # Dev Note: To get the right IDs, have to generate the Children Polys first.
            for aperture in hb_face.apertures:
                self.graphics3D.polygons.append(
                    Polygon.from_HB_Aperture(aperture))

            self.graphics3D.polygons.append(Polygon.from_HB_Face(hb_face))

    def create_building_from_hb_room(self, _hb_room: HB_Room) -> None:
        """Create the 'Building' with all Components and Zones."""
        self.building = Building.from_hb_room(_hb_room)

    def create_phius_certification_from_hb_room(self, _hb_room: HB_Room) -> None:
        self.ph_data.ph_certificate_criteria = _hb_room.properties.ph.ph_bldg_segment.ph_certification.certification_criteria
        self.ph_data.ph_selection_target_data = _hb_room.properties.ph.ph_bldg_segment.ph_certification.localization_selection_type
        self.ph_data.annual_heating_demand = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_heating_demand
        self.ph_data.annual_cooling_demand = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_cooling_demand
        self.ph_data.peak_heating_load = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_heating_load
        self.ph_data.peak_cooling_load = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_cooling_load

    def create_PH_Building_from_hb_room(self, _hb_room: HB_Room) -> None:
        ph_building = PH_Building()

        ph_building.building_category = _hb_room.properties.ph.ph_bldg_segment.usage_type.number
        ph_building.occupancy_type = _hb_room.properties.ph.ph_bldg_segment.occupancy_type.number
        ph_building.building_status = _hb_room.properties.ph.ph_bldg_segment.ph_certification.building_status.number
        ph_building.building_type = _hb_room.properties.ph.ph_bldg_segment.ph_certification.building_type.number
        ph_building.num_of_units = _hb_room.properties.ph.ph_bldg_segment.num_dwelling_units
        ph_building.num_of_floors = _hb_room.properties.ph.ph_bldg_segment.num_floor_levels

        # Not clear why this is a list in the WUFI file? When would there be more than one?
        self.ph_data.ph_buildings.append(ph_building)

    def create_climate_from_hb_room(self, _hb_room: HB_Room) -> None:
        ud_climate = _hb_room.properties.ph.ph_bldg_segment.climate

        # -- Basics
        self.climate.ph_climate_location.daily_temp_swing = ud_climate.summer_daily_temperature_swing
        self.climate.ph_climate_location.avg_wind_speed = ud_climate.average_wind_speed

        # -- Location
        self.climate.ph_climate_location.location.latitude = ud_climate.location.latitude
        self.climate.ph_climate_location.location.longitude = ud_climate.location.longitude
        self.climate.ph_climate_location.location.weather_station_elevation = ud_climate.location.weather_station_elevation
        self.climate.ph_climate_location.location.climate_zone = ud_climate.location.longitude
        self.climate.ph_climate_location.location.hours_from_UTC = ud_climate.location.hours_from_UTC

        # -- Ground
        self.climate.ph_climate_location.ground.ground_thermal_conductivity = ud_climate.ground.ground_thermal_conductivity
        self.climate.ph_climate_location.ground.ground_heat_capacitiy = ud_climate.ground.ground_heat_capacitiy
        self.climate.ph_climate_location.ground.ground_density = ud_climate.ground.ground_density
        self.climate.ph_climate_location.ground.depth_groundwater = ud_climate.ground.depth_groundwater
        self.climate.ph_climate_location.ground.flow_rate_groundwater = ud_climate.ground.flow_rate_groundwater

        # -- Monthly Values
        self.climate.ph_climate_location.monthly_temperature_air = ud_climate.monthly_temperature_air.values
        self.climate.ph_climate_location.monthly_temperature_dewpoint = ud_climate.monthly_temperature_dewpoint.values
        self.climate.ph_climate_location.monthly_temperature_sky = ud_climate.monthly_temperature_sky.values

        self.climate.ph_climate_location.monthly_radiation_north = ud_climate.monthly_radiation_north.values
        self.climate.ph_climate_location.monthly_radiation_east = ud_climate.monthly_radiation_east.values
        self.climate.ph_climate_location.monthly_radiation_south = ud_climate.monthly_radiation_south.values
        self.climate.ph_climate_location.monthly_radiation_west = ud_climate.monthly_radiation_west.values
        self.climate.ph_climate_location.monthly_radiation_global = ud_climate.monthly_radiation_global.values

        # -- Peak Load Values
        self.climate.ph_climate_location.peak_heating_1.temp = ud_climate.peak_heating_1.temp
        self.climate.ph_climate_location.peak_heating_1.rad_north = ud_climate.peak_heating_1.rad_north
        self.climate.ph_climate_location.peak_heating_1.rad_east = ud_climate.peak_heating_1.rad_east
        self.climate.ph_climate_location.peak_heating_1.rad_south = ud_climate.peak_heating_1.rad_south
        self.climate.ph_climate_location.peak_heating_1.rad_west = ud_climate.peak_heating_1.rad_west
        self.climate.ph_climate_location.peak_heating_1.rad_global = ud_climate.peak_heating_1.rad_global

        self.climate.ph_climate_location.peak_heating_2.temp = ud_climate.peak_heating_2.temp
        self.climate.ph_climate_location.peak_heating_2.rad_north = ud_climate.peak_heating_2.rad_north
        self.climate.ph_climate_location.peak_heating_2.rad_east = ud_climate.peak_heating_2.rad_east
        self.climate.ph_climate_location.peak_heating_2.rad_south = ud_climate.peak_heating_2.rad_south
        self.climate.ph_climate_location.peak_heating_2.rad_west = ud_climate.peak_heating_2.rad_west
        self.climate.ph_climate_location.peak_heating_2.rad_global = ud_climate.peak_heating_2.rad_global

        self.climate.ph_climate_location.peak_cooling_1.temp = ud_climate.peak_cooling_1.temp
        self.climate.ph_climate_location.peak_cooling_1.rad_north = ud_climate.peak_cooling_1.rad_north
        self.climate.ph_climate_location.peak_cooling_1.rad_east = ud_climate.peak_cooling_1.rad_east
        self.climate.ph_climate_location.peak_cooling_1.rad_south = ud_climate.peak_cooling_1.rad_south
        self.climate.ph_climate_location.peak_cooling_1.rad_west = ud_climate.peak_cooling_1.rad_west
        self.climate.ph_climate_location.peak_cooling_1.rad_global = ud_climate.peak_cooling_1.rad_global

        self.climate.ph_climate_location.peak_cooling_2.temp = ud_climate.peak_cooling_2.temp
        self.climate.ph_climate_location.peak_cooling_2.rad_north = ud_climate.peak_cooling_2.rad_north
        self.climate.ph_climate_location.peak_cooling_2.rad_east = ud_climate.peak_cooling_2.rad_east
        self.climate.ph_climate_location.peak_cooling_2.rad_south = ud_climate.peak_cooling_2.rad_south
        self.climate.ph_climate_location.peak_cooling_2.rad_west = ud_climate.peak_cooling_2.rad_west
        self.climate.ph_climate_location.peak_cooling_2.rad_global = ud_climate.peak_cooling_2.rad_global


@dataclass
class ProjectData_Agent:
    name: str = ""
    street: str = ""
    city: str = ""
    post_code: str = ""
    telephone: str = ""
    email: str = ""
    license_number: str = ""


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
                    self._assembly_types[hb_const.identifier] = Assembly.from_HB_OpaqueConstruction(
                        hb_const)

                hb_const.properties._ph.id_num = self._assembly_types[hb_const.identifier].id_num

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

                    aperture_const.properties._ph.id_num = self._window_types[
                        aperture_const.identifier].id_num

        return

    @property
    def assembly_types(self):
        return self._assembly_types.values()

    @property
    def window_types(self):
        return self._window_types.values()
