# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for Automating some common Sky Matrix operations."""

import os
import subprocess
import math

try:
    from typing import Any, Tuple
except ImportError:
    pass  # IronPython

try:
    import ladybug.epw as epw
    import ladybug.analysisperiod as ap
    from ladybug.wea import Wea
    from ladybug.viewsphere import view_sphere
    from ladybug.dt import DateTime
    from ladybug.config import folders as lb_folders
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:
    from ladybug_geometry.geometry2d.pointvector import Vector2D
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_geometry:\n\t{}'.format(e))

try:
    from ladybug_rhino.togeometry import to_vector2d
    from ladybug_rhino.grasshopper import objectify_output
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

try:
    from honeybee_radiance.config import folders as hb_folders
    from lbt_recipes.version import check_radiance_date
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_radiance:\n\t{}'.format(e))


from honeybee_ph_utils.input_tools import memoize

# -----------------------------------------------------------------------------
# constants for converting RGB values output by gendaymtx to broadband radiation
PATCHES_PER_ROW = {
    1: view_sphere.TREGENZA_PATCHES_PER_ROW + (1,),
    2: view_sphere.REINHART_PATCHES_PER_ROW + (1,)
}
PATCH_ROW_COEFF = {
    1: view_sphere.TREGENZA_COEFFICIENTS,
    2: view_sphere.REINHART_COEFFICIENTS
}


@memoize
def create_analysis_period_hoys(_period):
    # type: (Tuple[int, int]) -> Tuple
    """Return a new Ladybug Analysis Period HOYS."""

    anp = ap.AnalysisPeriod(
        st_month=_period[0],
        st_day=1,
        st_hour=0,
        end_month=_period[1],
        end_day=31,
        end_hour=23,
        timestep=1,
        is_leap_year=False
    )
    return anp.hoys


def broadband_radiation(patch_row_str, row_number, wea_duration, sky_density=1):
    """Parse a row of gendaymtx RGB patch data in W/sr/m2 to radiation in kWh/m2.

    This includes aplying broadband weighting to the RGB bands, multiplication
    by the steradians of each patch, and multiplying by the duration of time that
    they sky matrix represents in hours.

    Args:
        patch_row_str: Text string for a single row of RGB patch data.
        row_number: Interger for the row number that the patch corresponds to.
        sky_density: Integer (either 1 or 2) for the density.
        wea_duration: Number for the duration of the Wea in hours. This is used
            to convert between the average value output by the command and the
            cumulative value that is needed for all ladybug analyses.
    """
    R, G, B = patch_row_str.split(' ')
    weight_val = 0.265074126 * float(R) + 0.670114631 * float(G) + 0.064811243 * float(B)
    return weight_val * PATCH_ROW_COEFF[sky_density][row_number] * wea_duration / 1000


def parse_mtx_data(data_str, wea_duration, sky_density=1):
    """Parse a string of Radiance gendaymtx data to a list of radiation-per-patch.

    This function handles the removing of the header and the conversion of the
    RGB irradianc-=per-steraidian values to broadband radiation. It also removes
    the first patch, which is the ground and is not used by Ladybug.

    Args:
        data_str: The string that has been output by gendaymtx to stdout.
        wea_duration: Number for the duration of the Wea in hours. This is used
            to convert between the average value output by the command and the
            cumulative value that is needed for all ladybug analyses.
        sky_density: Integer (either 1 or 2) for the density.
    """
    # split lines and remove the header, ground patch and last line break
    data_lines = data_str.split('\n')
    patch_lines = data_lines[9:-1]

    # loop through the rows and convert the radiation RGB values
    broadband_irr = []
    patch_counter = 0
    for i, row_patch_count in enumerate(PATCHES_PER_ROW[sky_density]):
        row_slice = patch_lines[patch_counter:patch_counter + row_patch_count]
        irr_vals = (broadband_radiation(row, i, wea_duration, sky_density)
                    for row in row_slice)
        broadband_irr.extend(irr_vals)
        patch_counter += row_patch_count
    return broadband_irr


@memoize
def gen_matrix(_epw_file, _period, _north):
    # type: (epw.EPW, Tuple[int, int], Any) -> Any

    epw_data = epw.EPW(_epw_file)
    _location = epw_data.location
    high_density_ = None
    _ground_ref_ = None
    _hoys_ = create_analysis_period_hoys(_period)
    _direct_rad = epw_data.direct_normal_radiation
    _diffuse_rad = epw_data.diffuse_horizontal_radiation
    _folder_ = None

    # -------------------------------------------------------------------------
    # check the istalled Radiance date and get the path to the gemdaymtx executable
    check_radiance_date()
    gendaymtx_exe = os.path.join(hb_folders.radbin_path, 'gendaymtx.exe') if \
        os.name == 'nt' else os.path.join(hb_folders.radbin_path, 'gendaymtx')

    # -------------------------------------------------------------------------
    # process and set defaults for all of the global inputs
    if _north is not None:  # process the north_
        try:
            north_ = math.degrees(
                to_vector2d(_north).angle_clockwise(Vector2D(0, 1)))
        except AttributeError:  # north angle instead of vector
            north_ = float(_north)
    else:
        north_ = 0
    density = 2 if high_density_ else 1
    ground_r = 0.2 if _ground_ref_ is None else _ground_ref_

    # -------------------------------------------------------------------------
    # filter the radiation by _hoys if they are input
    if len(_hoys_) != 0:
        _direct_rad = _direct_rad.filter_by_hoys(_hoys_)
        _diffuse_rad = _diffuse_rad.filter_by_hoys(_hoys_)

    # -------------------------------------------------------------------------
    # create the wea and write it to the default_epw_folder
    wea = Wea(_location, _direct_rad, _diffuse_rad)
    wea_duration = len(wea) / wea.timestep
    wea_folder = _folder_ if _folder_ is not None else \
        os.path.join(lb_folders.default_epw_folder, 'sky_matrices')
    metd = _direct_rad.header.metadata
    wea_basename = metd['city'].replace(' ', '_') if 'city' in metd else 'unnamed'
    wea_path = os.path.join(wea_folder, wea_basename)
    wea_file = wea.write(wea_path)

    # -------------------------------------------------------------------------
    # execute the Radiance gendaymtx command
    use_shell = True if os.name == 'nt' else False

    # -------------------------------------------------------------------------
    # command for direct patches
    cmds = [gendaymtx_exe, '-m', str(density), '-d', '-O1', '-A', wea_file]
    process = subprocess.Popen(cmds, stdout=subprocess.PIPE, shell=use_shell)
    stdout = process.communicate()
    dir_data_str = stdout[0]

    # -------------------------------------------------------------------------
    # command for diffuse patches
    cmds = [gendaymtx_exe, '-m', str(density), '-s', '-O1', '-A', wea_file]
    process = subprocess.Popen(cmds, stdout=subprocess.PIPE, shell=use_shell)
    stdout = process.communicate()
    diff_data_str = stdout[0]

    # parse the data into a single matrix
    dir_vals = parse_mtx_data(dir_data_str, wea_duration, density)
    diff_vals = parse_mtx_data(diff_data_str, wea_duration, density)

    # -------------------------------------------------------------------------
    # collect sky metadata like the north, which will be used by other components
    metadata = [north_, ground_r]
    if _hoys_:
        metadata.extend([DateTime.from_hoy(h) for h in (_hoys_[0], _hoys_[-1])])
    else:
        metadata.extend([wea.analysis_period.st_time, wea.analysis_period.end_time])
    for key, val in _direct_rad.header.metadata.items():
        metadata.append('{} : {}'.format(key, val))

    # -------------------------------------------------------------------------
    # wrap everything together into an object to output from the component
    mtx_data = (metadata, dir_vals, diff_vals)
    sky_mtx = objectify_output('Cumulative Sky Matrix', mtx_data)

    return sky_mtx
