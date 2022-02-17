# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Conversion Schemas for how to write PH/HB objects to WUFI XML"""

from dataclasses import dataclass
from typing import List

from PHX.model import project
from PHX.model import building, certification, climate, constructions, geometry, ground, mech_equip, schedules, ventilation
from PHX.to_WUFI_XML.xml_writables import XML_Node, XML_List, XML_Object, xml_writable

TOL = 2  # Value tolerance for rounding. ie; 9.84318191919 -> 9.84


# -- PROJECT --


def _Project(_wufi_project: project.Project) -> List[xml_writable]:
    return [
        XML_Node("DataVersion", _wufi_project.data_version),
        XML_Node("UnitSystem", _wufi_project.data_version),
        XML_Node("ProgramVersion", _wufi_project.program_version),
        XML_Node("Scope", _wufi_project.scope),
        XML_Node("DimensionsVisualizedGeometry",
                 _wufi_project.visualized_geometry),
        XML_Object("ProjectData", _wufi_project.project_data),
        XML_List("UtilisationPatternsVentilation",
                 [XML_Object("UtilizationPatternVent", pat, "index", i)
                  for i, pat in enumerate(_wufi_project.utilization_patterns_ventilation)]),
        XML_List("UtilizationPatternVent",
                 _wufi_project.utilization_patterns_ph),
        XML_List("Variants", [XML_Object("Variant", var, "index", i)
                 for i, var in enumerate(_wufi_project.variants)]),
        XML_List(
            "Assemblies",
            [XML_Object("Assembly", at_id, "index", i)
             for i, at_id in enumerate(_wufi_project.assembly_types)],
        ),
        XML_List(
            "WindowTypes",
            [XML_Object("WindowType", wt_id, "index", i)
             for i, wt_id in enumerate(_wufi_project.window_types)],
        ),
    ]


def _Variant(_variant: project.Variant) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _variant.id_num),
        XML_Node("Name", _variant.name),
        XML_Node("Remarks", _variant.remarks),
        XML_Node("PlugIn", _variant.plugin),
        XML_Object("Graphics_3D", _variant.graphics3D),
        XML_Object("Building", _variant.building),
        XML_Object("ClimateLocation", _variant.climate),
        XML_Object("PassivehouseData", _variant.ph_data),
        XML_Object("HVAC", _variant.mech_systems,
                   _schema_name='_HVAC_Collection'),
    ]


def _ProjectData(_project_data: project.ProjectData) -> List[xml_writable]:
    return [
        XML_Node("Year_Construction", _project_data.year_constructed),
        XML_Node("OwnerIsClient", _project_data.owner_is_client),
        XML_Node("Date_Project", _project_data.project_date),
        XML_Node("WhiteBackgroundPictureBuilding", _project_data.image),
        XML_Node("Customer_Name", _project_data.customer.name),
        XML_Node("Customer_Street", _project_data.customer.street),
        XML_Node("Customer_Locality", _project_data.customer.city),
        XML_Node("Customer_PostalCode", _project_data.customer.post_code),
        XML_Node("Customer_Tel", _project_data.customer.telephone),
        XML_Node("Customer_Email", _project_data.customer.email),
        XML_Node("Building_Name", _project_data.building.name),
        XML_Node("Building_Street", _project_data.building.street),
        XML_Node("Building_Locality", _project_data.building.city),
        XML_Node("Building_PostalCode", _project_data.building.post_code),
        XML_Node("Owner_Name", _project_data.owner.name),
        XML_Node("Owner_Street", _project_data.owner.street),
        XML_Node("Owner_Locality", _project_data.owner.city),
        XML_Node("Owner_PostalCode", _project_data.owner.post_code),
        XML_Node("Responsible_Name", _project_data.responsible.name),
        XML_Node("Responsible_Street", _project_data.responsible.street),
        XML_Node("Responsible_Locality", _project_data.responsible.city),
        XML_Node("Responsible_PostalCode",
                 _project_data.responsible.post_code),
        XML_Node("Responsible_Tel", _project_data.responsible.telephone),
        XML_Node("Responsible_LicenseNr",
                 _project_data.responsible.license_number),
        XML_Node("Responsible_Email", _project_data.responsible.email),
    ]


# -- BUILDING --


def _Building(_b: building.Building) -> List[xml_writable]:
    return [
        XML_List("Components", [XML_Object("Component", c, "index", i)
                 for i, c in enumerate(_b.components)]),
        XML_List("Zones", [XML_Object("Zone", z, "index", i)
                 for i, z in enumerate(_b.zones)]),
    ]


def _Zone(_z: building.Zone) -> List[xml_writable]:
    return [
        XML_Node("Name", _z.name),
        XML_Node("IdentNr", _z.id_num),
        XML_List("RoomsVentilation", [XML_Object("Room", rm, "index", i)
                                      for i, rm in enumerate(_z.wufi_rooms)]),
        XML_Node("GrossVolume_Selection", 6),
        XML_Node("GrossVolume", _z.volume_gross),
        XML_Node("NetVolume_Selection", 6),
        XML_Node("NetVolume", _z.volume_net),
        XML_Node("FloorArea_Selection", 6),
        XML_Node("FloorArea", _z.weighted_net_floor_area),
        XML_Node("ClearanceHeight_Selection", 1),
        XML_Node("ClearanceHeight", _z.clearance_height),
        XML_Node("SpecificHeatCapacity_Selection", 2),
        XML_Node("SpecificHeatCapacity", _z.specific_heat_capacity),
        XML_Node("IdentNrPH_Building", 1),
    ]


def _Component(_c: building.Component) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _c.id_num),
        XML_Node("Name", _c.name),
        XML_Node("Visual", True),
        XML_Node("Type", _c.type),
        XML_Node("IdentNrColorI", _c.color_interior),
        XML_Node("IdentNrColorE", _c.color_exterior),
        XML_Node("InnerAttachment", _c.exposure_interior),
        XML_Node("OuterAttachment", _c.exposure_exterior),
        XML_Node("IdentNr_ComponentInnerSurface", _c.interior_attachment_id),
        XML_Node("IdentNrAssembly", _c.assembly_type_id_num),
        XML_Node("IdentNrWindowType", _c.window_type_id_num),
        XML_List("IdentNrPolygons", [XML_Node(
            "IdentNr", n, "index", i) for i, n in enumerate(_c.polygon_ids)]),
    ]


# -- CERTIFICATION --


def _PH_Building(_ph_bldg: certification.PH_Building) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _ph_bldg._count),
        XML_Node("BuildingCategory", _ph_bldg.building_category),
        XML_Node("OccupancyTypeResidential", _ph_bldg.occupancy_type),
        XML_Node("BuildingStatus", _ph_bldg.building_status),
        XML_Node("BuildingType", _ph_bldg.building_type),
        XML_Node("OccupancySettingMethod", _ph_bldg.occupancy_setting_method),
        XML_Node("NumberUnits", _ph_bldg.num_of_units),
        XML_Node("CountStories", _ph_bldg.num_of_floors),
        XML_Node("EnvelopeAirtightnessCoefficient", _ph_bldg.airtightness_q50),
        XML_List('FoundationInterfaces', [XML_Object('FoundationInterface', f, 'index', i, _schema_name='_FoundationInterface')
                                          for i, f in enumerate(_ph_bldg.foundations)]),
    ]


def _PassivehouseData(_ph_data: certification.PassivehouseData) -> List[xml_writable]:
    return [
        XML_Node("PH_CertificateCriteria", _ph_data.ph_certificate_criteria),
        XML_Node("PH_SelectionTargetData", _ph_data.ph_selection_target_data),
        XML_Node("AnnualHeatingDemand", _ph_data.annual_heating_demand),
        XML_Node("AnnualCoolingDemand", _ph_data.annual_cooling_demand),
        XML_Node("PeakHeatingLoad", _ph_data.peak_heating_load),
        XML_Node("PeakCoolingLoad", _ph_data.peak_cooling_load),
        XML_List("PH_Buildings", [XML_Object("PH_Building", obj, "index", i)
                 for i, obj in enumerate(_ph_data.ph_buildings)]),
    ]


# -- FOUNDATIONS --

def _FoundationInterface(_f: ground.Foundation) -> List[xml_writable]:
    return [
        XML_Node("Name", ''),
        XML_Node("SettingFloorSlabType", _f.floor_setting_num,
                 'choice', _f.floor_setting_str),
        XML_Node("FloorSlabType", _f.floor_type_num, 'choice', _f.floor_type_str),

        # XML_Node("PositionPerimeterInsulation", 1),
        # XML_Node("PerimeterInsulationWidthDepth", 1),
        # XML_Node("ThicknessPerimeterInsulation", 1),
        # XML_Node("ConductivityPerimeterInsulation", 1),
        # XML_Node("PhaseShiftMonths", 1),
        # XML_Node("HarmonicFraction", 1),
        # XML_Node("BasementVentilationACH", 1),
        # XML_Node("DepthBasementBelowGroundSurface_Selection", 1),
        # XML_Node("DepthBasementBelowGroundSurface", 1),
        # XML_Node("HeightBasementWallAboveGrade_Selection", 1),
        # XML_Node("HeightBasementWallAboveGrade", 1),
        # XML_Node("CrawlspaceVentOpenings_Selection", 1),
        # XML_Node("CrawlspaceVentOpenings", 1),
        # XML_Node("FloorSlabArea_Selection", 1),
        # XML_Node("FloorSlabArea", 1),
        # XML_Node("U_ValueBasementSlab_Selection", 1),
        # XML_Node("U_ValueBasementSlab", 1),
        # XML_Node("FloorCeilingArea_Selection", 1),
        # XML_Node("FloorCeilingArea", 1),
        # XML_Node("U_ValueCeilingToUnheatedCellar_Selection", 1),
        # XML_Node("U_ValueCeilingToUnheatedCellar", 1),
        # XML_Node("U_ValueBasementWall_Selection", 1),
        # XML_Node("U_ValueBasementWall", 1),
        # XML_Node("U_ValueWallAboveGround_Selection", 1),
        # XML_Node("U_ValueWallAboveGround", 1),
        # XML_Node("FloorSlabPerimeter_Selection", 1),
        # XML_Node("FloorSlabPerimeter", 1),
        # XML_Node("BasementVolume_Selection", 1),
        # XML_Node("BasementVolume", 1),
        # XML_Node("U_ValueCrawlspaceFloor_Selection", 1),
        # XML_Node("U_ValueCrawlspaceFloor", 1),
    ]


# -- CLIMATE --


def _PH_ClimateLocation(_climate: climate.PH_ClimateLocation) -> List[xml_writable]:
    return [
        XML_Node('Selection', _climate.selection),
        XML_Node('SelectionPECO2Factor', _climate.selection_pe_co2_factor),
        XML_Node('DailyTemperatureSwingSummer', _climate.daily_temp_swing),
        XML_Node('AverageWindSpeed', _climate.avg_wind_speed),

        # -- Location
        XML_Node('Latitude', _climate.location.latitude),
        XML_Node('Longitude', _climate.location.longitude),
        XML_Node('HeightNNWeatherStation', _climate.location.weather_station_elevation),
        XML_Node('dUTC', _climate.location.hours_from_UTC),
        XML_Node('ClimateZone', _climate.location.climate_zone),

        # -- Ground
        XML_Node('GroundThermalConductivity',
                 _climate.ground.ground_thermal_conductivity),
        XML_Node('GroundHeatCapacitiy', _climate.ground.ground_heat_capacitiy),
        XML_Node('GroundDensity', _climate.ground.ground_density),
        XML_Node('DepthGroundwater', _climate.ground.depth_groundwater),
        XML_Node('FlowRateGroundwater', _climate.ground.flow_rate_groundwater),

        # -- Monthly
        XML_List('TemperatureMonthly', [XML_Node("Item", val, "index", i)
                                        for i, val in enumerate(_climate.monthly_temperature_air)]),
        XML_List('DewPointTemperatureMonthly', [XML_Node("Item", val, "index", i)
                                                for i, val in enumerate(_climate.monthly_temperature_dewpoint)]),
        XML_List('SkyTemperatureMonthly', [XML_Node("Item", val, "index", i)
                                           for i, val in enumerate(_climate.monthly_temperature_sky)]),
        XML_List('NorthSolarRadiationMonthly', [XML_Node("Item", val, "index", i)
                                                for i, val in enumerate(_climate.monthly_radiation_north)]),
        XML_List('EastSolarRadiationMonthly', [XML_Node("Item", val, "index", i)
                                               for i, val in enumerate(_climate.monthly_radiation_east)]),
        XML_List('SouthSolarRadiationMonthly', [XML_Node("Item", val, "index", i)
                                                for i, val in enumerate(_climate.monthly_radiation_south)]),
        XML_List('WestSolarRadiationMonthly', [XML_Node("Item", val, "index", i)
                                               for i, val in enumerate(_climate.monthly_radiation_west)]),
        XML_List('GlobalSolarRadiationMonthly', [XML_Node("Item", val, "index", i)
                                                 for i, val in enumerate(_climate.monthly_radiation_global)]),

        # -- Peak Load Values
        XML_Node('TemperatureHeating1', _climate.peak_heating_1.temp),
        XML_Node('NorthSolarRadiationHeating1', _climate.peak_heating_1.rad_north),
        XML_Node('EastSolarRadiationHeating1', _climate.peak_heating_1.rad_east),
        XML_Node('SouthSolarRadiationHeating1', _climate.peak_heating_1.rad_south),
        XML_Node('WestSolarRadiationHeating1', _climate.peak_heating_1.rad_west),
        XML_Node('GlobalSolarRadiationHeating1', _climate.peak_heating_1.rad_global),

        XML_Node('TemperatureHeating2', _climate.peak_heating_2.temp),
        XML_Node('NorthSolarRadiationHeating2', _climate.peak_heating_2.rad_north),
        XML_Node('EastSolarRadiationHeating2', _climate.peak_heating_2.rad_east),
        XML_Node('SouthSolarRadiationHeating2', _climate.peak_heating_2.rad_south),
        XML_Node('WestSolarRadiationHeating2', _climate.peak_heating_2.rad_west),
        XML_Node('GlobalSolarRadiationHeating2', _climate.peak_heating_2.rad_global),

        XML_Node('TemperatureCooling', _climate.peak_cooling_1.temp),
        XML_Node('NorthSolarRadiationCooling', _climate.peak_cooling_1.rad_north),
        XML_Node('EastSolarRadiationCooling', _climate.peak_cooling_1.rad_east),
        XML_Node('SouthSolarRadiationCooling', _climate.peak_cooling_1.rad_south),
        XML_Node('WestSolarRadiationCooling', _climate.peak_cooling_1.rad_west),
        XML_Node('GlobalSolarRadiationCooling', _climate.peak_cooling_1.rad_global),

        XML_Node('TemperatureCooling2', _climate.peak_cooling_2.temp),
        XML_Node('NorthSolarRadiationCooling2', _climate.peak_cooling_2.rad_north),
        XML_Node('EastSolarRadiationCooling2', _climate.peak_cooling_2.rad_east),
        XML_Node('SouthSolarRadiationCooling2', _climate.peak_cooling_2.rad_south),
        XML_Node('WestSolarRadiationCooling2', _climate.peak_cooling_2.rad_west),
        XML_Node('GlobalSolarRadiationCooling2', _climate.peak_cooling_2.rad_global),
    ]


def _ClimateLocation(_climate: climate.ClimateLocation) -> List[xml_writable]:
    return [
        XML_Node('Selection', _climate.selection),
        # XML_Node('IDNr_DB', _climate.),
        # XML_Node('Name_DB', _climate.),
        # XML_Node('Comment_DB', _climate.),
        XML_Node('Latitude_DB', _climate.ph_climate_location.location.latitude, 'unit', "°"),
        XML_Node('Longitude_DB', _climate.ph_climate_location.location.longitude,  'unit', "°"),
        XML_Node(
            'HeightNN_DB', _climate.ph_climate_location.location.weather_station_elevation, 'unit', "m"),
        XML_Node('dUTC_DB', _climate.ph_climate_location.location.hours_from_UTC),
        # XML_Node('FileName_DB', _climate.),
        # XML_Node('Type_DB', _climate.),
        # XML_Node('CatalogueNr_DB', _climate.),
        # XML_Node('MapNr_DB', _climate.),
        XML_Node('Albedo', -2, 'choice', "User defined"),
        XML_Node('GroundReflShort', 0.2, 'unit', "-"),
        XML_Node('GroundReflLong', 0.1, 'unit', "-"),
        XML_Node('GroundEmission', 0.9, 'unit', "-"),
        XML_Node('CloudIndex', 0.66, 'unit', "-"),
        XML_Node('CO2concenration', 350, 'unit', "mg/m³"),
        XML_Node('Unit_CO2concentration', 48, 'choice', "ppmv"),
        XML_Object('PH_ClimateLocation', _climate.ph_climate_location),
    ]


# -- GEOMETRY --


def _Graphics3D(_graphics3D: geometry.Graphics3D) -> List[xml_writable]:
    return [
        XML_List("Vertices", [XML_Object("Vertix", var, "index", i)
                 for i, var in enumerate(_graphics3D.vertices)]),
        XML_List("Polygons", [XML_Object("Polygon", var, "index", i)
                 for i, var in enumerate(_graphics3D.polygons)]),
    ]


def _Polygon(_p: geometry.Polygon) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _p.id_num),
        XML_Node("NormalVectorX", _p.normal_vector.x),
        XML_Node("NormalVectorY", _p.normal_vector.y),
        XML_Node("NormalVectorZ", _p.normal_vector.z),
        XML_List(
            "IdentNrPoints", [XML_Node("IdentNr", v_id, "index", i)
                              for i, v_id in enumerate(_p.vertices_id_numbers)]
        ),
        XML_List(
            "IdentNrPolygonsInside",
            [XML_Node("IdentNr", v_id, "index", i)
             for i, v_id in enumerate(_p.child_polygon_ids)],
        ),
    ]


def _Vertix(_v: geometry.Vertix) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _v.id_num),
        XML_Node("X", _v.x),
        XML_Node("Y", _v.y),
        XML_Node("Z", _v.z),
    ]


# -- CONSTRUCTIONS --


def _Assembly(_a: constructions.Assembly) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _a.id_num),
        XML_Node("Name", _a.name),
        XML_Node("Order_Layers", _a.layer_order),
        XML_Node("Grid_Kind", _a.grid_kind),
        XML_List("Layers", [XML_Object("Layer", n, "index", i)
                 for i, n in enumerate(_a.layers)]),
    ]


def _Layer(_l: constructions.Layer) -> List[xml_writable]:
    return [
        XML_Node("Thickness", _l.thickness),
        XML_Object("Material", _l.material),
    ]


def _Material(_m: constructions.Material) -> List[xml_writable]:
    return [
        XML_Node("Mass", _m.name),
        XML_Node("ThermalConductivity", _m.conductivity),
        XML_Node("BulkDensity", _m.density),
        XML_Node("Porosity", _m.porosity),
        XML_Node("HeatCapacity", _m.heat_capacity),
        XML_Node("WaterVaporResistance", _m.water_vapor_resistance),
        XML_Node("ReferenceW", _m.reference_water),
    ]


def _WindowType(_wt: constructions.WindowType) -> List[xml_writable]:
    return [
        XML_Node("IdentNr", _wt.id_num),
        XML_Node("Name", _wt.name),
        XML_Node("Uw_Detailed>", _wt.use_detailed_uw),
        XML_Node("GlazingFrameDetailed", _wt.use_detailed_frame),
        XML_Node("U_Value", _wt.u_value_window),
        XML_Node("U_Value_Glazing", _wt.u_value_glass),
        XML_Node("U_Value_Frame", _wt.u_value_frame),
        XML_Node("Frame_Width_Left", _wt.frame_width_left),
        XML_Node("Frame_Psi_Left", _wt.frame_psi_inst_left),
        XML_Node("Frame_U_Left", _wt.frame_u_value_left),
        XML_Node("FrameFactor", _wt.frame_factor),
        XML_Node("Glazing_Psi_Left", _wt.frame_psi_g_left),
        XML_Node("SHGC_Hemispherical", _wt.glass_g_value),
        XML_Node("MeanEmissivity", _wt.glass_mean_emissivity),
        XML_Node("g_Value", _wt.glass_g_value),
    ]


# -- VENTILATION --


def _RoomVentilation(_r: ventilation.RoomVentilation) -> List[xml_writable]:
    return [
        XML_Node('Name', _r.name),
        XML_Node('Type', _r.wufi_type),
        XML_Node('IdentNrUtilizationPatternVent', _r.vent_pattern_id_num),
        XML_Node('IdentNrVentilationUnit', _r.vent_unit_id_num),
        XML_Node('Quantity', _r.quantity),
        XML_Node('AreaRoom', _r.weighted_floor_area, "unit", "m²"),
        XML_Node('ClearRoomHeight', _r.clear_height, "unit", "m"),
        XML_Node('DesignVolumeFlowRateSupply',
                 round(_r.ventilation_load.flow_supply, TOL), "unit", "m³/h"),
        XML_Node('DesignVolumeFlowRateExhaust',
                 round(_r.ventilation_load.flow_extract, TOL), "unit", "m³/h"),
        # XML_Node('SupplyFlowRateUserDef', 'Test', "unit", "m³/h"),
        # XML_Node('ExhaustFlowRateUserDef', 'Test', "unit", "m³/h"),
        # XML_Node('DesignFlowInterzonalUserDef', 'Test', "unit", "m³/h"),
    ]


def _UtilizationPatternVent(_util_pat: schedules.UtilizationPatternVent) -> List[xml_writable]:
    op_periods = _util_pat.operating_periods
    return [
        XML_Node("Name", _util_pat.name),
        XML_Node("IdentNr", _util_pat.id_num),
        XML_Node("OperatingDays", _util_pat.operating_days),
        XML_Node("OperatingWeeks", _util_pat.operating_weeks),
        XML_Node("Maximum_DOS", round(op_periods.high.period_operating_hours, TOL)),
        XML_Node("Maximum_PDF", round(op_periods.high.period_operation_speed, TOL)),
        XML_Node("Standard_DOS", round(op_periods.standard.period_operating_hours, TOL)),
        XML_Node("Standard_PDF", round(op_periods.standard.period_operation_speed, TOL)),
        XML_Node("Basic_DOS", round(op_periods.basic.period_operating_hours, TOL)),
        XML_Node("Basic_PDF", round(op_periods.basic.period_operation_speed, TOL)),
        XML_Node("Minimum_DOS", round(op_periods.minimum.period_operating_hours, TOL)),
        XML_Node("Minimum_PDF", round(op_periods.minimum.period_operation_speed, TOL)),
    ]


# -- HVAC --


def _PhxZoneCoverage(_zc: mech_equip.PhxZoneCoverage) -> List[xml_writable]:
    return [
        XML_Node("IdentNrZone", _zc.zone_num),
        XML_Node("CoverageHeating", _zc.zone_num),
        XML_Node("CoverageCooling", _zc.zone_num),
        XML_Node("CoverageVentilation", _zc.zone_num),
        XML_Node("CoverageHumidification", _zc.zone_num),
        XML_Node("CoverageDehumidification", _zc.zone_num),
    ]


@dataclass
class Temp_PH_Params:
    quantity: int = 1
    heat_recovery_efficiency: float = 0.0
    moisture_recovery_efficiency: float = 0.0
    fan_power: float = 0.55
    frost_protection_reqd: bool = True
    frost_temp: float = -5.0
    in_conditioned_space: bool = True


def _Device_Ventilator(_d: mech_equip.PhxVentilator) -> List[xml_writable]:
    ph_params = Temp_PH_Params()
    ph_params.quantity = _d.quantity
    ph_params.heat_recovery_efficiency = _d.heat_recovery_efficiency
    ph_params.moisture_recovery_efficiency = _d.moisture_recovery_efficiency
    ph_params.fan_power = _d.fan_power
    ph_params.frost_protection_reqd = _d.frost_protection_reqd
    ph_params.frost_temp = _d.frost_temp
    ph_params.in_conditioned_space = _d.in_conditioned_space

    return [
        XML_Node("Name", _d.name),
        XML_Node("IdentNr", _d.id_num),
        XML_Node("SystemType", _d.system_type_num, 'choice', _d.system_type_str),
        XML_Node("TypeDevice", _d.device_type_num, 'choice', _d.device_type_str),
        XML_Node("UsedFor_Heating", False),
        XML_Node("UsedFor_DHW", False),
        XML_Node("UsedFor_Cooling", False),
        XML_Node("UsedFor_Ventilation", True),
        XML_Node("UsedFor_Humidification", False),
        XML_Node("UsedFor_Dehumidification", False),
        XML_Node("UseOptionalClimate", False),
        XML_Node("IdentNr_OptionalClimate", -1),
        XML_Node("HeatRecovery", _d.heat_recovery_efficiency),
        XML_Node("MoistureRecovery ", _d.moisture_recovery_efficiency),
        XML_Object('PH_Parameters', ph_params,
                   _schema_name='_Device_Ventilator_PH_Params')
    ]


def _Device_Ventilator_PH_Params(_params: Temp_PH_Params) -> List[xml_writable]:
    return [
        XML_Node("Quantity", _params.quantity),
        XML_Node("HumidityRecoveryEfficiency", _params.moisture_recovery_efficiency),
        XML_Node("ElectricEfficiency", _params.fan_power),
        XML_Node("DefrostRequired", _params.frost_protection_reqd),
        XML_Node("FrostProtection", _params.frost_protection_reqd),
        XML_Node("TemperatureBelowDefrostUsed", _params.frost_temp),
        XML_Node("InConditionedSpace", _params.in_conditioned_space),
        # XML_Node("SubsoilHeatExchangeEfficiency", _params.),
        # XML_Node("VolumeFlowRateFrom", "unit","m³/h", _params.),
        # XML_Node("VolumeFlowRateTo", "unit","m³/h", _params.),
        # XML_Node("NoSummerBypass", _params.),
        # XML_Node("Maximum_VOS", _params.),
        # XML_Node("Maximum_PP", _params.),
        # XML_Node("Standard_VOS", _params.),
        # XML_Node("Standard_PP", _params.),
        # XML_Node("Basic_VOS", _params.),
        # XML_Node("Basic_PP", _params.),
        # XML_Node("Minimum_VOS", _params.),
        # XML_Node("Minimum_PP", _params.),
        # XML_Node("AuxiliaryEnergy", _params.),
        # XML_Node("AuxiliaryEnergyDHW", _params.),
    ]


def _Device_ElecResistance(_d: mech_equip.PhxMechanicalEquipment) -> List[xml_writable]:
    return []


def _WUFI_HVAC_SystemGroup(_hvac_system: mech_equip.PhxMechanicalEquipmentCollection) -> List[xml_writable]:
    devices = {
        1: '_Device_Ventilator',
        2: '_Device_ElecResistance',
    }

    return [
        XML_Node("Name", _hvac_system.name),
        XML_Node("Type", _hvac_system.sys_type_num, 'choice', _hvac_system.sys_type_str),
        XML_Node("IdentNr", _hvac_system.id_num),
        XML_List('ZonesCoverage', [XML_Object("ZoneCoverage", n, "index", i)
                 for i, n in enumerate([_hvac_system.zone_coverage])]),
        XML_List('Devices', [XML_Object("Device", d, "index", i, _schema_name=devices[d.device_type_num])
                 for i, d in enumerate(_hvac_system.equipment)]),
    ]


def _HVAC_Collection(_hvac) -> List[xml_writable]:
    return [
        XML_List("Systems", [XML_Object("System", n, "index", i, _schema_name='_WUFI_HVAC_SystemGroup')
                 for i, n in enumerate([_hvac])]),
    ]
