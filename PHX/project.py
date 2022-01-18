# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Project Classes"""

from __future__ import annotations
from typing import Any, ClassVar
from dataclasses import dataclass, field

from honeybee.model import Model as HB_Model
from honeybee.room import Room as HB_Room
from PHX import building, geometry, climate, certification, constructions, schedules


@dataclass
class Variant:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = "unnamed_variant"
    remarks: str = ""
    plugin: str = ""
    graphics3D: geometry.Graphics3D = field(default_factory=geometry.Graphics3D)
    building: building.Building = field(default_factory=building.Building)
    ph_data: certification.PassivehouseData = field(
        default_factory=certification.PassivehouseData)
    climate: climate.ClimateLocation = field(default_factory=climate.ClimateLocation)

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
                    geometry.Polygon.from_HB_Aperture(aperture))

            self.graphics3D.polygons.append(geometry.Polygon.from_HB_Face(hb_face))

    def create_building_from_hb_room(self, _hb_room: HB_Room) -> None:
        """Create the 'Building' with all Components and Zones."""
        self.building = building.Building.from_hb_room(_hb_room)

    def create_phius_certification_from_hb_room(self, _hb_room: HB_Room) -> None:
        self.ph_data.ph_certificate_criteria = _hb_room.properties.ph.ph_bldg_segment.ph_certification.certification_criteria
        self.ph_data.ph_selection_target_data = _hb_room.properties.ph.ph_bldg_segment.ph_certification.localization_selection_type
        self.ph_data.annual_heating_demand = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_heating_demand
        self.ph_data.annual_cooling_demand = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_cooling_demand
        self.ph_data.peak_heating_load = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_heating_load
        self.ph_data.peak_cooling_load = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_cooling_load

    def create_PH_Building_from_hb_room(self, _hb_room: HB_Room) -> None:
        ph_building = certification.PH_Building()

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

    _assembly_types: dict[str, constructions.Assembly] = field(default_factory=dict)
    _window_types: dict[str, Any] = field(default_factory=dict)
    utilisation_patterns_ventilation: schedules.UtilPat_Vent_Collection = field(
        default_factory=schedules.UtilPat_Vent_Collection)
    utilisation_patterns_ph: list = field(default_factory=list)
    variants: list = field(default_factory=list)

    project_data: ProjectData = field(default_factory=ProjectData)

    data_version: int = 48
    unit_system: int = 1
    program_version: str = "3.2.0.1"
    scope: int = 3
    visualized_geometry: int = 2

    def build_opaque_assemblies_from_HB_model(self, _hb_model: HB_Model) -> None:
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
                    self._assembly_types[hb_const.identifier] = constructions.Assembly.from_HB_OpaqueConstruction(
                        hb_const)

                hb_const.properties._ph.id_num = self._assembly_types[hb_const.identifier].id_num

        return None

    def build_transparent_assemblies_from_HB_Model(self, _hb_model: HB_Model) -> None:
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
                        self._window_types[aperture_const.identifier] = constructions.WindowType.from_HB_WindowConstruction(
                            aperture_const
                        )

                    aperture_const.properties._ph.id_num = self._window_types[
                        aperture_const.identifier].id_num

        return

    def build_util_patterns_ventilation_from_HB_Model(self, _hb_model: HB_Model) -> None:
        for hb_room in _hb_model.rooms:
            vent_pattern_id = hb_room.properties.energy.ventilation.identifier
            if self.utilisation_patterns_ventilation.key_is_in_collection(vent_pattern_id):
                # -- This is just to help speed things up.
                # -- Don't re-make the util pattern if it is already in collection.
                continue
            pat = schedules.UtilizationPatternVent.from_hb_room(hb_room)
            self.utilisation_patterns_ventilation.add_new_util_pattern(pat)

    @property
    def assembly_types(self):
        return self._assembly_types.values()

    @property
    def window_types(self):
        return self._window_types.values()
