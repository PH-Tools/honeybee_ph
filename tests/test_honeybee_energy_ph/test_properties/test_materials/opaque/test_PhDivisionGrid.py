from honeybee_energy.material.opaque import EnergyMaterial
from pytest import approx

from honeybee_energy_ph.properties.materials.opaque import PhDivisionGrid


def test_empty_ph_division_grid_dict_round_trip():
    grid_1 = PhDivisionGrid()
    d = grid_1.to_dict()

    grid_2 = PhDivisionGrid.from_dict(d)
    assert grid_2.to_dict() == d


def test_populated_ph_division_grid_dict_round_trip():
    grid_1 = PhDivisionGrid()
    grid_1.set_column_widths([1, 1])
    grid_1.set_row_heights([1, 1])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid_1.set_cell_material(0, 0, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid_1.set_cell_material(0, 1, mat_2)

    grid_1.steel_stud_spacing_mm = 406.4

    # --
    d = grid_1.to_dict()
    grid_2 = PhDivisionGrid.from_dict(d)
    assert grid_2.to_dict() == d
    assert len(grid_1.cells) == 2
    assert len(grid_2.cells) == 2
    assert grid_1.get_cell_material(0, 0) == grid_2.get_cell_material(0, 0)
    assert grid_1.get_cell_material(0, 1) == grid_2.get_cell_material(0, 1)
    assert grid_1.get_cell_material(1, 0) == grid_2.get_cell_material(1, 0)
    assert grid_1.get_cell_material(1, 1) == grid_2.get_cell_material(1, 1)


def test_ph_division_grid_duplicate():
    grid_1 = PhDivisionGrid()
    grid_1.set_column_widths([1, 1])
    grid_1.set_row_heights([1, 1])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid_1.set_cell_material(0, 0, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid_1.set_cell_material(0, 1, mat_2)

    grid_1.steel_stud_spacing_mm = 600

    grid_2 = grid_1.duplicate()
    assert grid_1.to_dict() == grid_2.to_dict()
    assert grid_1.get_cell_material(0, 0) == grid_2.get_cell_material(0, 0)
    assert grid_1.get_cell_material(0, 1) == grid_2.get_cell_material(0, 1)
    assert grid_1.get_cell_material(1, 0) == grid_2.get_cell_material(1, 0)
    assert grid_1.get_cell_material(1, 1) == grid_2.get_cell_material(1, 1)


def test_ph_division_get_cell_area():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    assert grid.get_cell_area(0, 0) == 2.4 * 1.2
    assert grid.get_cell_area(0, 1) == 2.4 * 0.8
    assert grid.get_cell_area(1, 0) == 0.4 * 1.2
    assert grid.get_cell_area(1, 1) == 0.4 * 0.8


def test_ph_division_get_cell_material():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid.set_cell_material(0, 0, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid.set_cell_material(0, 1, mat_2)

    assert grid.get_cell_material(0, 0) == mat_1
    assert grid.get_cell_material(0, 1) == mat_2
    assert grid.get_cell_material(1, 0) is None
    assert grid.get_cell_material(1, 1) is None


def test_ph_divisions_get_base_material():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid.set_cell_material(0, 0, mat_1)
    grid.set_cell_material(0, 1, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid.set_cell_material(1, 0, mat_2)
    grid.set_cell_material(1, 1, mat_2)

    mat_1_area = grid.get_cell_area(0, 0) + grid.get_cell_area(0, 1)
    mat_2_area = grid.get_cell_area(1, 0) + grid.get_cell_area(1, 1)
    assert mat_1_area > mat_2_area
    assert grid.get_base_material() == mat_1


def test_ph_divisions_get_equivalent_conductivity_1():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid.set_cell_material(0, 0, mat_1)
    grid.set_cell_material(0, 1, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1, density=999, specific_heat=999)
    grid.set_cell_material(1, 0, mat_2)
    grid.set_cell_material(1, 1, mat_2)

    assert grid.get_equivalent_conductivity() == 1.0


def test_ph_divisions_get_equivalent_conductivity_2():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=0.2, density=999, specific_heat=999)
    grid.set_cell_material(0, 0, mat_1)
    grid.set_cell_material(0, 1, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1.4, density=999, specific_heat=999)
    grid.set_cell_material(1, 0, mat_2)
    grid.set_cell_material(1, 1, mat_2)

    assert grid.get_equivalent_conductivity() == approx(0.3714285714285714)


def test_ph_divisions_get_width_m():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=0.2, density=999, specific_heat=999)
    grid.set_cell_material(0, 0, mat_1)
    grid.set_cell_material(0, 1, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1.4, density=999, specific_heat=999)
    grid.set_cell_material(1, 0, mat_2)
    grid.set_cell_material(1, 1, mat_2)

    # Test Column 1
    cell_0_0 = grid.get_cell(0, 0)
    assert cell_0_0 is not None
    assert grid.get_cell_width_m(cell_0_0) == 2.4

    cell_0_1 = grid.get_cell(0, 1)
    assert cell_0_1 is not None
    assert grid.get_cell_width_m(cell_0_1) == 2.4

    # Test Column 2
    cell_1_0 = grid.get_cell(1, 0)
    assert cell_1_0 is not None
    assert grid.get_cell_width_m(cell_1_0) == 0.4

    cell_1_1 = grid.get_cell(1, 1)
    assert cell_1_1 is not None
    assert grid.get_cell_width_m(cell_1_1) == 0.4


def test_ph_divisions_get_height_m():
    grid = PhDivisionGrid()
    grid.set_column_widths([2.4, 0.4])
    grid.set_row_heights([1.2, 0.8])

    mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=0.2, density=999, specific_heat=999)
    grid.set_cell_material(0, 0, mat_1)
    grid.set_cell_material(0, 1, mat_1)

    mat_2 = EnergyMaterial("mat_2", thickness=1, conductivity=1.4, density=999, specific_heat=999)
    grid.set_cell_material(1, 0, mat_2)
    grid.set_cell_material(1, 1, mat_2)

    # Test Row 1
    cell_0_0 = grid.get_cell(0, 0)
    assert cell_0_0 is not None
    assert grid.get_cell_height_m(cell_0_0) == 1.2

    cell_1_0 = grid.get_cell(1, 0)
    assert cell_1_0 is not None
    assert grid.get_cell_height_m(cell_1_0) == 1.2

    # Test Row 2
    cell_0_1 = grid.get_cell(0, 1)
    assert cell_0_1 is not None
    assert grid.get_cell_height_m(cell_0_1) == 0.8

    cell_1_1 = grid.get_cell(1, 1)
    assert cell_1_1 is not None
    assert grid.get_cell_height_m(cell_1_1) == 0.8
