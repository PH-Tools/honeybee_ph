# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Conversion Schemas for how to write PH/HB objects to WUFI XML"""

from to_WUFI_XML.wufi import (
    Layer,
    Material,
    Assembly,
    Component,
    Polygon,
    Vertix,
    Graphics3D,
    Project,
    ProjectData,
    Variant,
    WindowType,
    Zone,
)
from to_WUFI_XML.xml_writables import XML_Node, XML_List, XML_Object, xml_writable


def _Project(_wufi_project: Project) -> list[xml_writable]:
    return [
        XML_Node("DataVersion", _wufi_project.data_version),
        XML_Node("UnitSystem", _wufi_project.data_version),
        XML_Node("ProgramVersion", _wufi_project.program_version),
        XML_Node("Scope", _wufi_project.scope),
        XML_Node("DimensionsVisualizedGeometry",
                 _wufi_project.visualized_geometry),
        XML_Object("ProjectData", _wufi_project.project_data),
        XML_List("UtilisationPatternsVentilation",
                 _wufi_project.utilisation_patterns_ventilation),
        XML_List("UtilizationPatternsPH",
                 _wufi_project.utilisation_patterns_ph),
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


def _ProjectData(_project_data: ProjectData) -> list[xml_writable]:
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


def _Variant(_variant: Variant) -> list[xml_writable]:

    return [
        XML_Node("IdentNr", _variant.id_num),
        XML_Node("Name", _variant.name),
        XML_Node("Remarks", _variant.remarks),
        XML_Node("PlugIn", _variant.plugin),
        XML_Object("Graphics_3D", _variant.graphics3D),
        XML_Object("Building", _variant.building),
        # XML_Object("ClimateLocation", _variant.climate),
        # XML_Object("PassivehouseData", temp_PHData),
        # XML_Object("HVAC", _variant.mechanicals, _schema_name="_Mechanicals"),
    ]


def _Graphics3D(_graphics3D: Graphics3D) -> list[xml_writable]:
    return [
        XML_List("Vertices", [XML_Object("Vertix", var, "index", i)
                 for i, var in enumerate(_graphics3D.vertices)]),
        XML_List("Polygons", [XML_Object("Polygon", var, "index", i)
                 for i, var in enumerate(_graphics3D.polygons)]),
    ]


def _Polygon(_p: Polygon) -> list[xml_writable]:
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


def _Vertix(_v: Vertix) -> list[xml_writable]:
    return [
        XML_Node("IdentNr", _v.id_num),
        XML_Node("X", _v.x),
        XML_Node("Y", _v.y),
        XML_Node("Z", _v.z),
    ]


def _Building(_b: Component) -> list[xml_writable]:
    return [
        XML_List("Components", [XML_Object("Component", c, "index", i)
                 for i, c in enumerate(_b.components)]),
        XML_List("Zones", [XML_Object("Zone", z, "index", i)
                 for i, z in enumerate(_b.zones)]),
    ]


def _Component(_c: Component) -> list[xml_writable]:
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


def _Zone(_z: Zone) -> list[xml_writable]:
    return [
        XML_Node("Name", _z.name),
        XML_Node("IdentNr", _z.id_num),
        # XML_Node("GrossVolume_Selection", ),
        # XML_Node("GrossVolume", ),
        # XML_Node("NetVolume_Selection", ),
        # XML_Node("NetVolume", ),
        # XML_Node("FloorArea_Selection", ),
        # XML_Node("FloorArea", ),
        # XML_Node("ClearanceHeight_Selection", ),
        # XML_Node("ClearanceHeight", ),
        # XML_Node("SpecificHeatCapacity_Selection", ),
        # XML_Node("SpecificHeatCapacity", ),
    ]


def _Assembly(_a: Assembly) -> list[xml_writable]:
    return [
        XML_Node("IdentNr", _a.id_num),
        XML_Node("Name", _a.name),
        XML_Node("Order_Layers", _a.layer_order),
        XML_Node("Grid_Kind", _a.grid_kind),
        XML_List("Layers", [XML_Object("Layer", n, "index", i)
                 for i, n in enumerate(_a.layers)]),
    ]


def _Layer(_l: Layer) -> list[xml_writable]:
    return [
        XML_Node("Thickness", _l.thickness),
        XML_Object("Material", _l.material),
    ]


def _Material(_m: Material) -> list[xml_writable]:
    return [
        XML_Node("Mass", _m.name),
        XML_Node("ThermalConductivity", _m.conductivity),
        XML_Node("BulkDensity", _m.density),
        XML_Node("Porosity", _m.porosity),
        XML_Node("HeatCapacity", _m.heat_capacity),
        XML_Node("WaterVaporResistance", _m.water_vapor_resistance),
        XML_Node("ReferenceW", _m.reference_water),
    ]


def _WindowType(_wt: WindowType) -> list[xml_writable]:
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
