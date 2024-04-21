import pytest

from honeybee_energy_ph.hvac.hot_water import (
    PhHotWaterHeater,
    PhPipeBranch,
    PhPipeDiameter,
    PhPipeElement,
    PhPipeMaterial,
    PhPipeSegment,
    PhPipeTrunk,
    PhSHWHeaterBoiler,
    PhSHWHeaterBoilerWood,
    PhSHWHeaterBuilder,
    PhSHWHeaterDistrict,
    PhSHWHeaterElectric,
    PhSHWHeaterHeatPump,
    PhSHWTank,
    PhSHWTankType,
)


def test_PipeDiameter_raises_exception():
    with pytest.raises(Exception):
        PhPipeDiameter()


def test_PipeMaterial_raises_exception():
    with pytest.raises(Exception):
        PhPipeMaterial()


def test_PipeSegment_raises_exception():
    with pytest.raises(Exception):
        PhPipeSegment()


def test_PipeElement_raises_exception():
    with pytest.raises(Exception):
        PhPipeElement()


def test_PipeBranch_raises_exception():
    with pytest.raises(Exception):
        PhPipeBranch()


def test_PipeTrunk_raises_exception():
    with pytest.raises(Exception):
        PhPipeTrunk()


def test_SHWTankType_raises_exception():
    with pytest.raises(Exception):
        PhSHWTankType()


def test_SHWTank_raises_exception():
    with pytest.raises(Exception):
        PhSHWTank()


def test_HotWaterHeater_raises_exception():
    with pytest.raises(Exception):
        PhHotWaterHeater()


def test_SHWHeaterElectric_raises_exception():
    with pytest.raises(Exception):
        PhSHWHeaterElectric()


def test_SHWHeaterBoiler_raises_exception():
    with pytest.raises(Exception):
        PhSHWHeaterBoiler()


def test_SHWHeaterBoilerWood_raises_exception():
    with pytest.raises(Exception):
        PhSHWHeaterBoilerWood()


def test_SHWHeaterDistrict_raises_exception():
    with pytest.raises(Exception):
        PhSHWHeaterDistrict()


def test_SHWHeaterHeatPump_raises_exception():
    with pytest.raises(Exception):
        PhSHWHeaterHeatPump()


def test_SHWHeaterBuilder_raises_exception():
    with pytest.raises(Exception):
        PhSHWHeaterBuilder()
