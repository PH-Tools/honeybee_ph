# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
ISO 6946 | "Building components and building elements. Thermal resistance and thermal
transmittance. Calculation methods"

Section 6.7 gives the R-value of a component with thermally inhomogeneous layers as the mean of
two limits:

- the UPPER limit (parallel path): each path is a complete section through the whole component,
  and the paths are combined in parallel by their area fractions.
- the LOWER limit (isothermal planes): each inhomogeneous layer is combined in parallel by area
  first, and the layer resistances are then summed in series.

The two limits differ only across a STACK of layers. For a single layer taken alone they are the
same number, `d / sum(f_j * lambda_j)`, which is what `PhDivisionGrid.get_equivalent_conductivity()`
returns. That is why the mean of limits lives here, over a list of layers, and not on the grid.

Framing in different layers is read as STAGGERED: the upper-limit paths are the cartesian product
of each layer's paths. This matches the PH-Navigator editors and assumes nothing about framing in
one layer lining up with framing in another.

All values are SI. Surface (air film) resistances are optional and default to zero, because a
honeybee `OpaqueConstruction` does not know its own exposure. Where they matter, pass them: ISO 6946
puts Rsi and Rse INSIDE each upper-limit path, so adding them to a film-free upper limit afterwards
is not the same number. On a 2x6 stud wall the two readings are 0.011 m2k/W apart.
"""

try:
    from typing import Any, Iterable, List, Optional, Tuple
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_energy.material import opaque
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy:\n\t{}".format(e))


# -- A pathological model would otherwise expand the cartesian product without bound. Real
# -- assemblies have at most two or three layers with a division grid.
MAX_HEAT_FLOW_PATHS = 10000


class TooManyHeatFlowPathsError(Exception):
    """An error for when the parallel-path expansion would exceed MAX_HEAT_FLOW_PATHS."""

    def __init__(self, _layer_number, _path_count):
        # type: (int, int) -> None
        self.msg = (
            "Error: The ISO 6946 upper-limit calculation would need {} heat-flow paths at layer {}, "
            "which is more than the {} allowed. Simplify the division grids on the "
            "construction's layers.".format(_path_count, _layer_number, MAX_HEAT_FLOW_PATHS)
        )
        super(TooManyHeatFlowPathsError, self).__init__(self.msg)


def _get_division_grid(_hb_material):
    # type: (Any) -> Optional[Any]
    """Return the PhDivisionGrid of a material, or None if it does not have a populated one."""
    material_prop_ph = getattr(_hb_material.properties, "ph", None)
    if material_prop_ph is None:
        return None

    division_grid = getattr(material_prop_ph, "divisions", None)
    if division_grid is None:
        return None

    if division_grid.cell_count == 0:
        return None

    return division_grid


def _get_cell_conductivity(_cell, _hb_material):
    # type: (Any, opaque.EnergyMaterial) -> float
    """Return a grid-cell's conductivity (W/mk), falling back to the host layer's own material.

    honeybee-energy allows a material conductivity of zero, which has no resistance to give.
    """
    if _cell.material.conductivity <= 0:
        return _hb_material.conductivity
    return _cell.material.conductivity


def get_layer_paths(_hb_material):
    # type: (Any) -> List[Tuple[float, float]]
    """Return the parallel heat-flow paths through a single construction layer.

    A layer with no division grid is a single path with the whole area. A layer with a division
    grid has one path per grid-cell: the grid divides the layer 'in-plane' (columns are widths,
    rows are heights), so every cell spans the full thickness of the layer.

    Arguments:
    ----------
        * _hb_material (Any): A honeybee-energy opaque material (EnergyMaterial,
            EnergyMaterialNoMass, or EnergyMaterialVegetation).

    Returns:
    --------
        * list[tuple[float, float]]: The layer's paths as (area-fraction, r-value) pairs. The
            area-fractions sum to 1.0.
    """
    if not hasattr(_hb_material, "conductivity"):
        # -- A no-mass material carries its R-value directly and cannot have a division grid.
        return [(1.0, _hb_material.r_value)]

    division_grid = _get_division_grid(_hb_material)
    if division_grid is None:
        return [(1.0, _hb_material.r_value)]

    cell_areas = []  # type: List[Tuple[Any, float]]
    total_area = 0.0
    for cell in division_grid.cells:
        cell_area = division_grid.get_cell_area(cell.column, cell.row)
        cell_areas.append((cell, cell_area))
        total_area += cell_area

    if total_area <= 0:
        return [(1.0, _hb_material.r_value)]

    paths = []  # type: List[Tuple[float, float]]
    for cell, cell_area in cell_areas:
        cell_conductivity = _get_cell_conductivity(cell, _hb_material)
        paths.append((cell_area / total_area, _hb_material.thickness / cell_conductivity))
    return paths


def _get_paths_by_layer(_hb_materials):
    # type: (Iterable[Any]) -> List[List[Tuple[float, float]]]
    """Return the parallel heat-flow paths for each layer, in layer order."""
    return [get_layer_paths(m) for m in _hb_materials]


def _r_value_lower_limit_from_paths(_paths_by_layer, _r_si, _r_se):
    # type: (List[List[Tuple[float, float]]], float, float) -> float
    """Return the ISO 6946 lower-limit R-value from pre-computed layer paths."""
    total_r_value = _r_si + _r_se
    for layer_paths in _paths_by_layer:
        layer_u_value = 0.0
        for area_fraction, r_value in layer_paths:
            if r_value > 0:
                layer_u_value += area_fraction / r_value
        if layer_u_value > 0:
            total_r_value += 1.0 / layer_u_value
    return total_r_value


def _r_value_upper_limit_from_paths(_paths_by_layer, _r_si, _r_se):
    # type: (List[List[Tuple[float, float]]], float, float) -> float
    """Return the ISO 6946 upper-limit R-value from pre-computed layer paths.

    The surface resistances are carried inside each path, as ISO 6946 6.7.1 requires.
    """
    # -- Each element is one path through the layers built so far: (r-value, area-fraction)
    assembly_paths = [(_r_si + _r_se, 1.0)]  # type: List[Tuple[float, float]]

    for layer_number, layer_paths in enumerate(_paths_by_layer):
        path_count = len(assembly_paths) * len(layer_paths)
        if path_count > MAX_HEAT_FLOW_PATHS:
            raise TooManyHeatFlowPathsError(layer_number, path_count)

        new_assembly_paths = []  # type: List[Tuple[float, float]]
        for path_r_value, path_area_fraction in assembly_paths:
            for area_fraction, r_value in layer_paths:
                new_assembly_paths.append((path_r_value + r_value, path_area_fraction * area_fraction))
        assembly_paths = new_assembly_paths

    total_u_value = 0.0
    for path_r_value, path_area_fraction in assembly_paths:
        if path_r_value > 0:
            total_u_value += path_area_fraction / path_r_value

    if total_u_value > 0:
        return 1.0 / total_u_value
    return 0.0


def get_r_value_lower_limit(_hb_materials, _r_si=0.0, _r_se=0.0):
    # type: (Iterable[Any], float, float) -> float
    """Return the ISO 6946 LOWER-limit (isothermal planes) R-value of a stack of layers.

    Each layer is combined in parallel by area, and the layer resistances are summed in series.
    This is the value a consumer gets when it reads the area-weighted equivalent conductivity of
    each hybrid layer and sums the layers, and it is the pessimistic bound on a framed assembly.

    Arguments:
    ----------
        * _hb_materials (Iterable[Any]): The construction's honeybee-energy materials, in order.
        * _r_si (float): Optional interior surface (film) resistance (m2k/W). Default: 0.0.
        * _r_se (float): Optional exterior surface (film) resistance (m2k/W). Default: 0.0.

    Returns:
    --------
        * float: The lower-limit R-value (m2k/W).
    """
    return _r_value_lower_limit_from_paths(_get_paths_by_layer(_hb_materials), _r_si, _r_se)


def get_r_value_upper_limit(_hb_materials, _r_si=0.0, _r_se=0.0):
    # type: (Iterable[Any], float, float) -> float
    """Return the ISO 6946 UPPER-limit (parallel path) R-value of a stack of layers.

    Each path runs through every layer and the paths are combined in parallel by area. Framing in
    different layers is read as staggered, so the paths are the cartesian product of the layers'
    paths.

    Arguments:
    ----------
        * _hb_materials (Iterable[Any]): The construction's honeybee-energy materials, in order.
        * _r_si (float): Optional interior surface (film) resistance (m2k/W). Default: 0.0.
        * _r_se (float): Optional exterior surface (film) resistance (m2k/W). Default: 0.0.

    Returns:
    --------
        * float: The upper-limit R-value (m2k/W).

    Raises:
    -------
        * TooManyHeatFlowPathsError: If the cartesian product would exceed MAX_HEAT_FLOW_PATHS.
    """
    return _r_value_upper_limit_from_paths(_get_paths_by_layer(_hb_materials), _r_si, _r_se)


def get_r_value_mean_of_limits(_hb_materials, _r_si=0.0, _r_se=0.0):
    # type: (Iterable[Any], float, float) -> float
    """Return the ISO 6946 mean-of-limits R-value of a stack of layers.

    This is the value designPH and PHPP report for an assembly with framed layers.

    Arguments:
    ----------
        * _hb_materials (Iterable[Any]): The construction's honeybee-energy materials, in order.
        * _r_si (float): Optional interior surface (film) resistance (m2k/W). Default: 0.0.
        * _r_se (float): Optional exterior surface (film) resistance (m2k/W). Default: 0.0.

    Returns:
    --------
        * float: The mean of the upper- and lower-limit R-values (m2k/W).
    """
    paths_by_layer = _get_paths_by_layer(_hb_materials)
    r_value_upper = _r_value_upper_limit_from_paths(paths_by_layer, _r_si, _r_se)
    r_value_lower = _r_value_lower_limit_from_paths(paths_by_layer, _r_si, _r_se)
    return (r_value_upper + r_value_lower) / 2.0


def get_error_percent(_hb_materials, _r_si=0.0, _r_se=0.0):
    # type: (Iterable[Any], float, float) -> float
    """Return the spread between the ISO 6946 limits, as the percentage designPH prints.

    Arguments:
    ----------
        * _hb_materials (Iterable[Any]): The construction's honeybee-energy materials, in order.
        * _r_si (float): Optional interior surface (film) resistance (m2k/W). Default: 0.0.
        * _r_se (float): Optional exterior surface (film) resistance (m2k/W). Default: 0.0.

    Returns:
    --------
        * float: (R-upper - R-lower) / (2 * R-mean) * 100. Zero for a construction with no
            thermally inhomogeneous layers.
    """
    paths_by_layer = _get_paths_by_layer(_hb_materials)
    r_value_upper = _r_value_upper_limit_from_paths(paths_by_layer, _r_si, _r_se)
    r_value_lower = _r_value_lower_limit_from_paths(paths_by_layer, _r_si, _r_se)
    r_value_mean = (r_value_upper + r_value_lower) / 2.0

    if r_value_mean <= 0:
        return 0.0
    return (r_value_upper - r_value_lower) / (2.0 * r_value_mean) * 100.0


def get_equivalent_conductivity(_r_value, _thickness):
    # type: (float, float) -> float
    """Return the conductivity of the single layer which has the given R-value and thickness.

    Used to collapse a whole construction into one equivalent layer for a tool which cannot hold
    the real layers (designPH beyond three paths, or a Flixo-style single made-up material).

    Arguments:
    ----------
        * _r_value (float): The R-value to reproduce (m2k/W).
        * _thickness (float): The thickness of the equivalent layer (m).

    Returns:
    --------
        * float: The equivalent conductivity (W/mk). Zero if either input is non-positive.
    """
    if _r_value <= 0 or _thickness <= 0:
        return 0.0
    return _thickness / _r_value
