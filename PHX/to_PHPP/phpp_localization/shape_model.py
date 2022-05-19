# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Datamodel of the PHPP 'Shape' (worksheet names and input column names)."""

from pydantic import BaseModel


# -----------------------------------------------------------------------------


class VerificationInputItem(BaseModel):
    locator_col: str
    locator_string: str
    input_column: str


class Verification(BaseModel):
    name: str
    cert_type: VerificationInputItem
    cert_class: VerificationInputItem
    pe_type: VerificationInputItem
    enerphit_type: VerificationInputItem
    retrofit_type: VerificationInputItem


# -----------------------------------------------------------------------------


class ClimateActiveDatasetCol(BaseModel):
    country: str
    region: str
    dataset: str
    elevation_override: str


class ClimateActiveDataset(BaseModel):
    locator_col_header: str
    locator_string_header: str
    input_columns: ClimateActiveDatasetCol


class ClimateUDBlockCol(BaseModel):
    jan: str
    feb: str
    mar: str
    apr: str
    may: str
    jun: str
    jul: str
    aug: str
    sep: str
    oct: str
    nov: str
    dec: str
    peak_heating_1: str
    peak_heating_2: str
    peak_cooling_1: str
    peak_cooling_2: str
    PER: str
    latitude: str
    longitude: str
    elevation: str
    display_name: str
    summer_delta_t: str
    source: str


class ClimateUDBlock(BaseModel):
    locator_col_header: str
    locator_string_header: str
    input_columns: ClimateUDBlockCol


class Climate(BaseModel):
    name: str
    active_dataset: ClimateActiveDataset
    ud_block: ClimateUDBlock


# -----------------------------------------------------------------------------


class UValuesConstructorCol(BaseModel):
    display_name: str
    r_si: str
    r_se: str
    interior_insulation: str
    sec_1_description: str
    sec_1_conductivity: str
    sec_2_description: str
    sec_2_conductivity: str
    sec_3_description: str
    sec_3_conductivity: str
    thickness: str
    u_val_supplement: str


class UValuesConstructor(BaseModel):
    locator_col_header: str
    locator_string_header: str
    input_columns: UValuesConstructorCol


class UValues(BaseModel):
    name: str
    constructor: UValuesConstructor


# -----------------------------------------------------------------------------


class AreasSurfaceRowsCol(BaseModel):
    description: str
    group_number: str
    quantity: str
    area: str
    assembly_id: str
    orientation: str
    angle: str
    shading: str
    absorptivity: str
    emissivity: str


class AreasSurfaceRows(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: AreasSurfaceRowsCol


class Areas(BaseModel):
    name: str
    surface_rows: AreasSurfaceRows


# -----------------------------------------------------------------------------


class ColGround(BaseModel):
    ...


class Ground(BaseModel):
    name: str
    columns: ColGround


# -----------------------------------------------------------------------------


class ComponentsGlazingsCol(BaseModel):
    description: str
    g_value: str
    u_value: str


class ComponentsFramesCol(BaseModel):
    description: str
    u_value_left: str
    u_value_right: str
    u_value_bottom: str
    u_value_top: str
    width_left: str
    width_right: str
    width_bottom: str
    width_top: str
    psi_g_left: str
    psi_g_right: str
    psi_g_bottom: str
    psi_g_top: str
    psi_i_left: str
    psi_i_right: str
    psi_i_bottom: str
    psi_i_top: str


class ComponentsVentilatorsCol(BaseModel):
    display_name: str
    sensible_heat_recovery: str
    latent_heat_recovery: str
    electric_efficiency: str
    min_m3h: str
    max_m3h: str
    pa_per_section: str
    pa_per_fittings: str
    frost_protection_reqd: str
    noise_35DBA: str
    noise_supply_air: str
    noise_extract_air: str
    additional_info: str


class ComponentsGlazings(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: ComponentsGlazingsCol


class ComponentsFrames(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: ComponentsFramesCol


class ComponentsVentilators(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: ComponentsVentilatorsCol


class Components(BaseModel):
    name: str
    glazings: ComponentsGlazings
    frames: ComponentsFrames
    ventilators: ComponentsVentilators


# -----------------------------------------------------------------------------


class WindowWindowRowsColumns(BaseModel):
    quantity: str
    description: str
    width: str
    height: str
    host: str
    glazing_id: str
    frame_id: str
    psi_i_left: str
    psi_i_right: str
    psi_i_bottom: str
    psi_i_top: str
    comfort_exempt: str
    comfort_temp: str


class WindowWindowRows(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: WindowWindowRowsColumns


class Windows(BaseModel):
    name: str
    window_rows: WindowWindowRows


# -----------------------------------------------------------------------------


class ColShading(BaseModel):
    ...


class Shading(BaseModel):
    name: str
    columns: ColShading


# -----------------------------------------------------------------------------


class VentilationInputItem(BaseModel):
    locator_col: str
    locator_string: str
    input_column: str


class Ventilation(BaseModel):
    name: str
    vent_type: VentilationInputItem
    wind_coeff_e: VentilationInputItem
    wind_coeff_f: VentilationInputItem
    airtightness_n50: VentilationInputItem
    airtightness_q50: VentilationInputItem
    multi_unit_on: VentilationInputItem


# -----------------------------------------------------------------------------


class AddnlVentColumnsRooms(BaseModel):
    quantity: str
    display_name: str
    vent_unit_assigned: str
    weighted_floor_area: str
    clear_height: str
    V_sup: str
    V_eta: str
    V_trans: str
    operating_days: str
    operating_weeks: str
    holiday_days: str
    period_high_speed: str
    period_high_time: str
    period_standard_speed: str
    period_standard_time: str
    period_minimum_speed: str
    period_minimum_time: str


class AddnlVentColumnsUnits(BaseModel):
    quantity: str
    display_name: str
    unit_selected: str
    oda_sup_pa: str
    eta_eha_pa: str
    addnl_pa: str
    ext_location: str
    subsoil_hr: str
    frost_protection_type: str
    temperature_below_defrost_used: str


class AddnlVentColumnsDucts(BaseModel):
    quantity: str
    diameter: str
    width: str
    height: str
    insul_thickness: str
    insul_conductivity: str
    insul_reflective: str
    sup_air_duct_len: str
    oda_air_duct_len: str
    exh_air_duct_len: str
    duct_assign_1: str
    duct_assign_2: str
    duct_assign_3: str
    duct_assign_4: str
    duct_assign_5: str
    duct_assign_6: str
    duct_assign_7: str
    duct_assign_8: str
    duct_assign_9: str
    duct_assign_10: str


class AddnlVentRoomsInputBlockRooms(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: AddnlVentColumnsRooms


class AddnlVentRoomsInputBlockUnits(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: AddnlVentColumnsUnits


class AddnlVentRoomsInputBlockDucts(BaseModel):
    locator_col_header: str
    locator_string_header: str
    locator_col_entry: str
    locator_string_entry: str
    input_columns: AddnlVentColumnsDucts


class AddnlVent(BaseModel):
    name: str
    rooms: AddnlVentRoomsInputBlockRooms
    units: AddnlVentRoomsInputBlockUnits
    ducts: AddnlVentRoomsInputBlockDucts


# -----------------------------------------------------------------------------


class ColSummVent(BaseModel):
    ...


class SummVent(BaseModel):
    name: str
    columns: ColSummVent


class ColCoolingUnits(BaseModel):
    ...


class CoolingUnits(BaseModel):
    name: str
    columns: ColCoolingUnits


class ColDhw(BaseModel):
    ...


class Dhw(BaseModel):
    name: str
    columns: ColDhw


class ColSolarDhw(BaseModel):
    ...


class SolarDhw(BaseModel):
    name: str
    columns: ColSolarDhw


class ColPv(BaseModel):
    ...


class Pv(BaseModel):
    name: str
    columns: ColPv


class ColElectricity(BaseModel):
    ...


class Electricity(BaseModel):
    name: str
    columns: ColElectricity


class ColUseNonRes(BaseModel):
    ...


class UseNonRes(BaseModel):
    name: str
    columns: ColUseNonRes


class ColElecNonRes(BaseModel):
    ...


class ElecNonRes(BaseModel):
    name: str
    columns: ColElecNonRes


class ColAuxElec(BaseModel):
    ...


class AuxElec(BaseModel):
    name: str
    columns: ColAuxElec


class ColIhgNonRes(BaseModel):
    ...


class IhgNonRes(BaseModel):
    name: str
    columns: ColIhgNonRes


class ColPer(BaseModel):
    ...


class Per(BaseModel):
    name: str
    columns: ColPer


class ColHp(BaseModel):
    ...


class Hp(BaseModel):
    name: str
    columns: ColHp


class ColBoiler(BaseModel):
    ...


class Boiler(BaseModel):
    name: str
    columns: ColBoiler


# -----------------------------------------------------------------------------


class PhppShape(BaseModel):
    VERIFICATION: Verification
    CLIMATE: Climate
    UVALUES: UValues
    AREAS: Areas
    GROUND: Ground
    COMPONENTS: Components
    WINDOWS: Windows
    SHADING: Shading
    VENTILATION: Ventilation
    ADDNL_VENT: AddnlVent
    SUMM_VENT: SummVent
    COOLING_UNITS: CoolingUnits
    DHW: Dhw
    SOLAR_DHW: SolarDhw
    PV: Pv
    ELECTRICITY: Electricity
    USE_NON_RES: UseNonRes
    ELEC_NON_RES: ElecNonRes
    AUX_ELEC: AuxElec
    IHG_NON_RES: IhgNonRes
    PER: Per
    HP: Hp
    BOILER: Boiler
