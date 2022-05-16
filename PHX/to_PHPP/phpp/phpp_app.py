# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller for managing the PHPP Connection."""

from typing import List

from PHX.model import project

from PHX.to_PHPP.phpp import xl_app, io
from PHX.to_PHPP.phpp.model.locations.shape_model import PhppShape
from PHX.to_PHPP.phpp.model import (areas_surface, climate_entry, uvalues_constructor, component_glazing,
                                    component_frame, windows_rows)


class PHPPConnection:
    def __init__(self, _worksheet_shapes: PhppShape):
        # -- Get the localized (units, language) PHPP Shape with worksheet names and column locations
        self.worksheet_shape = _worksheet_shapes

        # -- Setup the Excel connection and facade object.
        self.xl: xl_app.XLConnection = xl_app.XLConnection()

        # -- Setup all the individual worksheet Classes.
        self.climate = io.Climate(self.xl, self.worksheet_shape.CLIMATE.name)
        self.u_values = io.UValues(self.xl, self.worksheet_shape.UVALUES.name)
        self.components = io.Components(self.xl, self.worksheet_shape.COMPONENTS.name)
        self.areas = io.Areas(self.xl, self.worksheet_shape.AREAS.name)
        self.windows = io.Windows(self.xl, self.worksheet_shape.WINDOWS.name)

    def write_climate_data(self, phx_project: project.PhxProject) -> None:
        """Write the varaint's weather-station data to the PHPP 'Climate' worksheet."""
        columns = self.worksheet_shape.CLIMATE.columns.dict()
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
        columns = self.worksheet_shape.UVALUES.columns.dict()

        construction_blocks: List[uvalues_constructor.ConstructorBlock] = []
        for phx_construction in phx_project.assembly_types.values():
            construction_blocks.append(
                uvalues_constructor.ConstructorBlock(columns, phx_construction)
            )
        self.u_values.write_construction_blocks(construction_blocks)

    def write_project_window_components(self, phx_project: project.PhxProject) -> None:
        """Write all of the frame and glass constructions from a PhxProject to the PHPP 'Components' worksheet."""
        columns_glazings = self.worksheet_shape.COMPONENTS.columns.glazings.dict()
        columns_frames = self.worksheet_shape.COMPONENTS.columns.frames.dict()

        glazing_component_rows: List[component_glazing.GlazingRow] = []
        frame_component_rows: List[component_frame.FrameRow] = []
        for phx_construction in phx_project.window_types.values():
            glazing_component_rows.append(
                component_glazing.GlazingRow(columns_glazings, phx_construction)
            )
            frame_component_rows.append(
                component_frame.FrameRow(columns_frames, phx_construction)
            )
        self.components.write_glazings(glazing_component_rows)
        self.components.write_frames(frame_component_rows)

    def write_project_opaque_surfaces(self, phx_project: project.PhxProject) -> None:
        """Write all of the opaque surfaces from a PhxProject to the PHPP 'Areas' worksheet."""
        columns = self.worksheet_shape.AREAS.columns.dict()

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
        columns = self.worksheet_shape.WINDOWS.columns.dict()

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
                                columns=columns,
                                phx_polygon=ap_polygon,
                                phx_construction=phx_aperture.window_type,
                                phpp_host_surface_id_name=phpp_host_surface_id_name,
                                phpp_id_frame=phpp_id_frame,
                                phpp_id_glazing=phpp_id_glazing
                            )
                        )
        self.windows.write_windows(phpp_windows)
