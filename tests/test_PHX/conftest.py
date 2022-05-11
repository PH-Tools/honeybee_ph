import importlib
from pathlib import Path
import pytest

from PHX.model import (building, project, geometry, schedules, certification,
                       constructions, elec_equip, components)
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


def _reset_phx_class_counters():
    project.PhxVariant._count = 0
    geometry.PhxVertix._count = 0
    geometry.PhxPolygon._count = 0
    schedules.UtilizationPatternVent._count = 0
    certification.PhxPHBuilding._count = 0
    constructions.PhxConstructionOpaque._count = 0
    constructions.PhxConstructionWindow._count = 0
    building.PhxZone._count = 0
    components.PhxComponentBase._count = 0
    elec_equip.PhxElectricalDevice._count = 0
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
    water.PhxHotWaterTank._count = 0

    ventilation.PhxDeviceVentilation._count = 0


def _reload_phx_classes():
    """reload all of the PHX model classes. This is similar to the 'reset_class_counters
    except that it will reset all of the PHX modules back to starting position. This is
    used for running the xml-reference-case testers, since otherwise the id-number 
    counters will not line up correctly.
    """
    importlib.reload(geometry)
    importlib.reload(building)
    importlib.reload(project)
    importlib.reload(geometry)
    importlib.reload(schedules)
    importlib.reload(certification)
    importlib.reload(constructions)
    importlib.reload(elec_equip)
    importlib.reload(components)


@pytest.fixture
def reset_class_counters():
    """Re-set class's _count variable in order to test id-num incrementing properly"""
    _reset_phx_class_counters()
    try:
        yield
    finally:
        _reset_phx_class_counters()


@pytest.fixture(params=[
    (
        Path('tests', '_source_hbjson',
             'Default_Model_Single_Zone.hbjson'),
        Path('tests', '_reference_xml',
             'Default_Model_Single_Zone.xml')
    ),
    (
        Path('tests', '_source_hbjson',
             'Default_Room_Multiple_Zones_with_Apertures_Single_BldgSegment.hbjson'),
        Path('tests', '_reference_xml',
             'Default_Room_Multiple_Zones_with_Apertures_Single_BldgSegment.xml')
    ),
    (
        Path('tests', '_source_hbjson',
             'Default_Room_Multiple_Zones_with_Apertures.hbjson'),
        Path('tests', '_reference_xml',
             'Default_Room_Multiple_Zones_with_Apertures.xml')
    ),
    (
        Path('tests', '_source_hbjson',
             'Default_Room_Single_Zone_with_Apertures.hbjson'),
        Path('tests', '_reference_xml',
             'Default_Room_Single_Zone_with_Apertures.xml')
    ),
    (
        Path('tests', '_source_hbjson',
             'Default_Room_Single_Zone_with_Shades.hbjson'),
        Path('tests', '_reference_xml',
             'Default_Room_Single_Zone_with_Shades.xml')
    ),
])
def to_xml_reference_cases(request):
    """Yields file-paths to reference test-cases"""
    _reload_phx_classes()
    try:
        yield request.param
    finally:
        _reload_phx_classes()
