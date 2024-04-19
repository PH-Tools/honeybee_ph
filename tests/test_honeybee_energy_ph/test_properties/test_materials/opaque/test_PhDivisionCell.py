from honeybee_energy.material.opaque import EnergyMaterial

from honeybee_energy_ph.properties.materials.opaque import PhDivisionCell


def test_ph_division_cell_dict_round_trip():
    hb_mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    cell_1 = PhDivisionCell(0, 1, hb_mat_1)

    d = cell_1.to_dict()
    cell_2 = PhDivisionCell.from_dict(d)
    assert cell_2.to_dict() == d


def test_ph_division_cell_duplicate():
    hb_mat_1 = EnergyMaterial("mat_1", thickness=1, conductivity=1, density=999, specific_heat=999)
    cell_1 = PhDivisionCell(0, 1, hb_mat_1)

    cell_2 = cell_1.duplicate()
    assert cell_2.to_dict() == cell_1.to_dict()
    assert cell_2.material == cell_1.material
    assert cell_2.row == cell_1.row
    assert cell_2.column == cell_1.column
    assert cell_2.material == cell_1.material
