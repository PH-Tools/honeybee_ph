from honeybee_energy.material.opaque import EnergyMaterial

from honeybee_energy_ph.properties.materials.opaque import PhDivisionCell, PhDivisionGrid


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

    grid_2 = grid_1.duplicate()
    assert grid_1.to_dict() == grid_2.to_dict()
    assert grid_1.get_cell_material(0, 0) == grid_2.get_cell_material(0, 0)
    assert grid_1.get_cell_material(0, 1) == grid_2.get_cell_material(0, 1)
    assert grid_1.get_cell_material(1, 0) == grid_2.get_cell_material(1, 0)
    assert grid_1.get_cell_material(1, 1) == grid_2.get_cell_material(1, 1)
