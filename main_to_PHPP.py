# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""DEV SANDBOX: export an HBJSON file to a PHPP XL file."""

from rich import print
import pathlib
from typing import List

from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_PHPP.phpp import phpp_app
from PHX.to_PHPP.phpp.model import areas_surface, uvalues_constructor, component_glazing, component_frame, windows_rows

if __name__ == '__main__':
    # --- Input file Path
    # -------------------------------------------------------------------------
    SOURCE_FILE = pathlib.Path("tests", "_source_hbjson",
                               "Default_Room_Single_Zone_with_Apertures.hbjson")

    # --- Read in an existing HB_JSON and re-build the HB Objects
    # -------------------------------------------------------------------------
    print("[bold green]- [/bold green]" * 50)
    print(
        f"[bold green]> Reading in the HBJSON file: ./{SOURCE_FILE}[/bold green]")
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(SOURCE_FILE)
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

    # --- Generate the PhxProject file.
    # -------------------------------------------------------------------------
    phx_project = create_project.convert_hb_model_to_PhxProject(
        hb_model, group_components=True)

    # --- Connect to open instance of XL
    # -------------------------------------------------------------------------
    phpp_conn = phpp_app.PHPPConnection()
    if phpp_conn.xl.connection_is_open():
        file = phpp_conn.xl.wb.name
        print(f'[bold green]> connected to excel doc: {file}[/bold green]')

    with phpp_conn.xl.in_silent_mode():

        # -- Constructions / U-Values
        construction_blocks = []
        for phx_construction in phx_project.assembly_types.values():
            construction_blocks.append(
                uvalues_constructor.ConstructorBlock(phx_construction)
            )
        phpp_conn.u_values.write_construction_blocks(construction_blocks)

        # -- Frame and Glazing Components
        glazing_component_rows = []
        frame_component_rows = []
        for phx_construction in phx_project.window_types.values():
            glazing_component_rows.append(
                component_glazing.GlazingRow(phx_construction)
            )
            frame_component_rows.append(
                component_frame.FrameRow(phx_construction)
            )
        phpp_conn.components.write_glazings(glazing_component_rows)
        phpp_conn.components.write_frames(frame_component_rows)

        # -- Surfaces
        surfaces: List[areas_surface.SurfaceRow] = []
        for phx_variant in phx_project.variants:
            for opaque_component in phx_variant.building.opaque_components:
                for phx_polygon in opaque_component.polygons:
                    surfaces.append(
                        areas_surface.SurfaceRow(
                            phx_polygon,
                            opaque_component,
                            phpp_conn.u_values.get_constructor_phpp_id_by_name(
                                opaque_component.assembly.display_name)
                        )
                    )
        phpp_conn.areas.write_surfaces(surfaces)

        # -- Windows
        phpp_windows: List[windows_rows.WindowRow] = []
        for phx_variant in phx_project.variants:
            for window_component in phx_variant.building.transparent_components:
                for phx_polygon in window_component.polygons:

                    host_polygon = phx_variant.building.get_host_polygon_by_child_id_num(
                        phx_polygon.id_num)
                    phpp_host_surface_id_name = phpp_conn.areas.surfaces.get_surface_phpp_id_by_name(
                        host_polygon.display_name)
                    phpp_id_frame = phpp_conn.components.frames.get_frame_phpp_id_by_name(
                        window_component.window_type.display_name)
                    phpp_id_glazing = phpp_conn.components.frames.get_frame_phpp_id_by_name(
                        window_component.window_type.display_name)

                    phpp_windows.append(
                        windows_rows.WindowRow(
                            phx_polygon=phx_polygon,
                            phpp_host_surface_id_name=phpp_host_surface_id_name,
                            phpp_id_frame=phpp_id_frame,
                            phpp_id_glazing=phpp_id_glazing
                        )
                    )
        phpp_conn.windows.write_windows(phpp_windows)
