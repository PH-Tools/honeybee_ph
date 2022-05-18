# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller for managing the PHPP Connection."""

from typing import List

from PHX.model import project, certification

from PHX.to_PHPP import xl_app
from PHX.to_PHPP import sheet_io
from PHX.to_PHPP.phpp_localization import shape_model
from PHX.to_PHPP.phpp_model import (areas_surface, climate_entry, uvalues_constructor,
                                    component_glazing, component_frame, component_vent, ventilation_data,
                                    windows_rows, vent_space, vent_units, vent_ducts)


class PHPPConnection:

    def __init__(self, _phpp_shape: shape_model.PhppShape):
        # -- Get the localized (units, language) PHPP Shape with worksheet names and column locations
        self.shape = _phpp_shape

        # -- Setup the Excel connection and facade object.
        self.xl: xl_app.XLConnection = xl_app.XLConnection()

        # -- Setup all the individual worksheet Classes.
        self.climate = sheet_io.Climate(self.xl, self.shape.CLIMATE.name)
        self.u_values = sheet_io.UValues(self.xl, self.shape.UVALUES.name)
        self.components = sheet_io.Components(self.xl, self.shape.COMPONENTS)
        self.areas = sheet_io.Areas(self.xl, self.shape.AREAS.name)
        self.windows = sheet_io.Windows(self.xl, self.shape.WINDOWS)
        self.addnl_vent = sheet_io.AddnlVent(self.xl, self.shape.ADDNL_VENT)
        self.ventilation = sheet_io.Ventilation(self.xl, self.shape.VENTILATION)

    def write_climate_data(self, phx_project: project.PhxProject) -> None:
        """Write the variant's weather-station data to the PHPP 'Climate' worksheet."""
        columns = self.shape.CLIMATE.columns.dict()
        for phx_variant in phx_project.variants:
            # -- Write the actual weather station data
            weather_station_data = climate_entry.ClimateDataBlock(
                columns,
                phx_variant.location
            )
            self.climate.write_climate_block(weather_station_data)

            # -- Set the active weather station
            active_climate_data = climate_entry.ClimateSettings(
                columns,
                phx_variant.location
            )
            self.climate.write_active_climate(active_climate_data)

    def write_project_constructions(self, phx_project: project.PhxProject) -> None:
        """Write all of the opaque constructions to the PHPP 'U-Values' worksheet."""
        columns = self.shape.UVALUES.columns.dict()

        construction_blocks: List[uvalues_constructor.ConstructorBlock] = []
        for phx_construction in phx_project.assembly_types.values():
            construction_blocks.append(
                uvalues_constructor.ConstructorBlock(
                    columns,
                    phx_construction)
            )
        self.u_values.write_construction_blocks(construction_blocks)

    def write_project_window_components(self, phx_project: project.PhxProject) -> None:
        """Write all of the frame and glass constructions from a PhxProject to the PHPP 'Components' worksheet."""

        glazing_component_rows: List[component_glazing.GlazingRow] = []
        frame_component_rows: List[component_frame.FrameRow] = []
        for phx_construction in phx_project.window_types.values():
            glazing_component_rows.append(
                component_glazing.GlazingRow(
                    shape=self.shape.COMPONENTS,
                    phx_construction=phx_construction)
            )
            frame_component_rows.append(
                component_frame.FrameRow(
                    shape=self.shape.COMPONENTS,
                    phx_construction=phx_construction)
            )
        self.components.write_glazings(glazing_component_rows)
        self.components.write_frames(frame_component_rows)

    def write_project_ventilation_components(self, phx_project: project.PhxProject) -> None:
        """Write all of the ventilators from a PhxProject to the PHPP 'Components' worksheet."""

        phpp_ventilator_rows: List[component_vent.VentilatorRow] = []
        for phx_variant in phx_project.variants:
            for phx_vent_sys in phx_variant.mech_systems.ventilation_subsystems:
                new_vent_row = component_vent.VentilatorRow(
                    shape=self.shape.COMPONENTS,
                    phx_vent_sys=phx_vent_sys.device,
                )
                phpp_ventilator_rows.append(new_vent_row)
        self.components.write_ventilators(phpp_ventilator_rows)

    def write_project_opaque_surfaces(self, phx_project: project.PhxProject) -> None:
        """Write all of the opaque surfaces from a PhxProject to the PHPP 'Areas' worksheet."""
        columns = self.shape.AREAS.columns.dict()

        surfaces: List[areas_surface.SurfaceRow] = []
        for phx_variant in phx_project.variants:
            for opaque_component in phx_variant.building.opaque_components:
                for phx_polygon in opaque_component.polygons:
                    surfaces.append(
                        areas_surface.SurfaceRow(
                            columns,
                            phx_polygon,
                            opaque_component,
                            self.u_values.get_constructor_phpp_id_by_name(
                                opaque_component.assembly.display_name)
                        )
                    )
        self.areas.write_surfaces(surfaces)

    def write_project_window_surfaces(self, phx_project: project.PhxProject) -> None:
        """Write all of the window surfaces from a PhxProject to the PHPP 'Windows' worksheet."""

        phpp_windows: List[windows_rows.WindowRow] = []
        for phx_variant in phx_project.variants:
            for phx_component in phx_variant.building.opaque_components:
                for phx_aperture in phx_component.apertures:
                    for ap_polygon in phx_aperture.polygons:
                        host_polygon = phx_component.get_host_polygon_by_child_id_num(
                            ap_polygon.id_num
                        )
                        phpp_host_surface_id_name = self.areas.surfaces.get_surface_phpp_id_by_name(
                            host_polygon.display_name
                        )
                        phpp_id_frame = self.components.frames.get_frame_phpp_id_by_name(
                            phx_aperture.window_type.display_name
                        )
                        phpp_id_glazing = self.components.frames.get_frame_phpp_id_by_name(
                            phx_aperture.window_type.display_name
                        )

                        phpp_windows.append(
                            windows_rows.WindowRow(
                                shape=self.shape.WINDOWS,
                                phx_polygon=ap_polygon,
                                phx_construction=phx_aperture.window_type,
                                phpp_host_surface_id_name=phpp_host_surface_id_name,
                                phpp_id_frame=phpp_id_frame,
                                phpp_id_glazing=phpp_id_glazing
                            )
                        )
        self.windows.write_windows(phpp_windows)

    def write_project_ventilators(self, phx_project: project.PhxProject) -> None:
        """Write all of the used Ventilator Units from a PhxProject to the PHPP 'Additional Vent' worksheet."""

        phpp_vent_unit_rows: List[vent_units.VentUnitRow] = []
        for phx_variant in phx_project.variants:
            for phx_vent_sys in phx_variant.mech_systems.ventilation_subsystems:
                phpp_id_ventilator = self.components.ventilators.get_ventilator_phpp_id_by_name(
                    phx_vent_sys.device.display_name
                )
                new_vent_row = vent_units.VentUnitRow(
                    shape=self.shape.ADDNL_VENT,
                    phx_vent_sys=phx_vent_sys.device,
                    phpp_id_ventilator=phpp_id_ventilator,
                )
                phpp_vent_unit_rows.append(new_vent_row)

        self.addnl_vent.write_vent_units(phpp_vent_unit_rows)

    def write_project_spaces(self, phx_project: project.PhxProject) -> None:
        """Write all of the PH-Spaces from a PhxProject to the PHPP 'Additional Vent' worksheet."""

        phpp_vent_rooms: List[vent_space.VentSpaceRow] = []
        for phx_variant in phx_project.variants:
            for zone in phx_variant.building.zones:
                for room in zone.wufi_rooms:
                    phx_mech_vent_system = phx_variant.mech_systems.get_mech_subsystem_by_id(
                        room.vent_unit_id_num
                    )
                    phpp_id_ventilator = self.components.ventilators.get_ventilator_phpp_id_by_name(
                        phx_mech_vent_system.device.display_name
                    )
                    phpp_row_ventilator = self.addnl_vent.vent_units.get_vent_unit_num_by_phpp_id(
                        phpp_id_ventilator
                    )
                    phx_vent_pattern = phx_project.utilization_patterns_ventilation.get_pattern_by_id_num(
                        room.vent_pattern_id_num
                    )

                    phpp_rm = vent_space.VentSpaceRow(
                        shape=self.shape.ADDNL_VENT,
                        phx_room_vent=room,
                        phpp_row_ventilator=phpp_row_ventilator,
                        phx_vent_pattern=phx_vent_pattern,
                    )
                    phpp_vent_rooms.append(phpp_rm)

        self.addnl_vent.write_spaces(phpp_vent_rooms)

    def write_project_ventilation_type(self, phx_project: project.PhxProject) -> None:
        """Write the Ventilation-Type to the PHPP 'Ventilation' worksheet."""

        for variant in phx_project.variants:
            self.ventilation.write_ventilation_type(
                # TODO: Get the actual type from the model someplace?
                ventilation_data.VentilationInputItem.vent_type(
                    self.shape.VENTILATION,
                    "1-Balanced PH ventilation with HR"
                )
            )
            self.ventilation.write_multi_vent_worksheet_on(
                ventilation_data.VentilationInputItem.multi_unit_on(
                    self.shape.VENTILATION,
                    "x"
                )
            )

    def write_project_airtightness(self, phx_project: project.PhxProject) -> None:
        """Write the Airtightness data to the PHPP 'Ventilation' worksheet."""

        for variant in phx_project.variants:
            if not variant.ph_certification.ph_building_data:
                continue
            ph_bldg: certification.PhxPhBuildingData = variant.ph_certification.ph_building_data

            self.ventilation.write_wind_coeff_e(
                ventilation_data.VentilationInputItem.wind_coeff_e(
                    self.shape.VENTILATION,
                    ph_bldg.wind_coefficient_e
                )
            )
            self.ventilation.write_wind_coeff_f(
                ventilation_data.VentilationInputItem.wind_coeff_f(
                    self.shape.VENTILATION,
                    ph_bldg.wind_coefficient_f
                )
            )
            self.ventilation.write_airtightness_n50(
                ventilation_data.VentilationInputItem.airtightness_n50(
                    self.shape.VENTILATION,
                    ph_bldg.airtightness_n50
                )
            )
            self.ventilation.write_airtightness_q50(
                ventilation_data.VentilationInputItem.airtightness_q50(
                    self.shape.VENTILATION,
                    ph_bldg.airtightness_q50
                )
            )
