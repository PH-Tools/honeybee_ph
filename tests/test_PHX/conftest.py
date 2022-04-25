import pytest
from PHX.model import project, geometry, schedules, certification, constructions, building, elec_equip
from PHX.model.loads.ventilation import PhxRoomVentilation
from PHX.model.hvac import _base, cooling, collection, water, ventilation, heating


@pytest.fixture
def polygon_1x1x0() -> geometry.PhxPolygon:
    p1 = geometry.PhxPolygon()
    p1.add_vertix(geometry.PhxVertix(0, 0, 0))
    p1.add_vertix(geometry.PhxVertix(0, 1, 0))
    p1.add_vertix(geometry.PhxVertix(1, 1, 0))
    p1.add_vertix(geometry.PhxVertix(1, 0, 0))
    return p1


@pytest.fixture
def polygon_2x2x0() -> geometry.PhxPolygon:
    p1 = geometry.PhxPolygon()
    p1.add_vertix(geometry.PhxVertix(0, 0, 0))
    p1.add_vertix(geometry.PhxVertix(0, 2, 0))
    p1.add_vertix(geometry.PhxVertix(2, 2, 0))
    p1.add_vertix(geometry.PhxVertix(2, 0, 0))
    return p1


@pytest.fixture
def reset_class_counters():
    """Re-set class's _count variable in order to test incrementing properly"""

    project.PhxVariant._count = 0
    geometry.PhxVertix._count = 0
    geometry.PhxPolygon._count = 0
    schedules.UtilizationPatternVent._count = 0
    certification.PhxPHBuilding._count = 0
    constructions.Assembly._count = 0
    constructions.WindowType._count = 0
    building.PhxZone._count = 0
    building.PhxComponent._count = 0
    elec_equip.PhxElectricalEquipment._count = 0
    PhxRoomVentilation._count = 0
    _base.PhxMechanicalEquipment._count = 0
    _base.PhxMechanicalSubSystem._count = 0

    collection.PhxMechanicalEquipmentCollection._count = 0

    cooling.PhxCoolingDevice._count = 0
    cooling.PhxCoolingVentilation._count = 0
    cooling.PhxCoolingRecirculation._count = 0
    cooling.PhxCoolingDehumidification._count = 0
    cooling.PhxCoolingPanel._count = 0

    heating.PhxHeatingDevice._count = 0
    heating.PhxHeaterElectric._count = 0
    heating.PhxHeaterBoilerFossil._count = 0
    heating.PhxHeaterBoilerWood._count = 0
    heating.PhxHeaterDistrictHeat._count = 0
    heating.PhxHeaterHeatPumpAnnual._count = 0
    heating.PhxHeaterHeatPumpMonthly._count = 0
    heating.PhxHeaterHeatPumpHotWater._count = 0
    heating.PhxHeaterHeatPumpCombined._count = 0

    water.PhxHotWaterDevice._count = 0

    ventilation.PhxVentilationDevice._count = 0

    yield

    project.PhxVariant._count = 0
    geometry.PhxVertix._count = 0
    geometry.PhxPolygon._count = 0
    schedules.UtilizationPatternVent._count = 0
    certification.PhxPHBuilding._count = 0
    constructions.Assembly._count = 0
    constructions.WindowType._count = 0
    building.PhxZone._count = 0
    building.PhxComponent._count = 0
    elec_equip.PhxElectricalEquipment._count = 0
    PhxRoomVentilation._count = 0
    _base.PhxMechanicalEquipment._count = 0
    _base.PhxMechanicalSubSystem._count = 0

    collection.PhxMechanicalEquipmentCollection._count = 0

    cooling.PhxCoolingDevice._count = 0
    cooling.PhxCoolingVentilation._count = 0
    cooling.PhxCoolingRecirculation._count = 0
    cooling.PhxCoolingDehumidification._count = 0
    cooling.PhxCoolingPanel._count = 0

    heating.PhxHeatingDevice._count = 0
    heating.PhxHeaterElectric._count = 0
    heating.PhxHeaterBoilerFossil._count = 0
    heating.PhxHeaterBoilerWood._count = 0
    heating.PhxHeaterDistrictHeat._count = 0
    heating.PhxHeaterHeatPumpAnnual._count = 0
    heating.PhxHeaterHeatPumpMonthly._count = 0
    heating.PhxHeaterHeatPumpHotWater._count = 0
    heating.PhxHeaterHeatPumpCombined._count = 0

    water.PhxHotWaterDevice._count = 0

    ventilation.PhxVentilationDevice._count = 0
