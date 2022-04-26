from PHX.model.hvac import cooling, _base, collection
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxCoolingPanel(reset_class_counters):
    d1 = cooling.PhxCoolingPanel()
    sys = _base.PhxMechanicalSubSystem()
    sys.device = d1
    coll = collection.PhxMechanicalEquipmentCollection()
    coll.add_new_mech_subsystem(sys.identifier, sys)
    result = generate_WUFI_XML_from_object(coll, _header="")
    assert xml_string_to_list(result) == [
        '<Systems count="1">',
        '<System index="0">',
        '<Name>Ideal Air System</Name>',
        '<Type choice="User defined (ideal system)">1</Type>',
        '<IdentNr>1</IdentNr>',
        '<ZonesCoverage count="1">',
        '<ZoneCoverage index="0">',
        '<IdentNrZone>1.0</IdentNrZone>',
        '<CoverageHeating>1.0</CoverageHeating>',
        '<CoverageCooling>1.0</CoverageCooling>',
        '<CoverageVentilation>1.0</CoverageVentilation>',
        '<CoverageHumidification>1.0</CoverageHumidification>',
        '<CoverageDehumidification>1.0</CoverageDehumidification>',
        '</ZoneCoverage>',
        '</ZonesCoverage>',
        '<Devices count="1">',
        '<Device index="0">',
        '<Name>_unnamed_equipment_</Name>',
        '<IdentNr>1</IdentNr>',
        '<SystemType>5</SystemType>',
        '<TypeDevice>5</TypeDevice>',
        '<UsedFor_Heating>false</UsedFor_Heating>',
        '<UsedFor_DHW>false</UsedFor_DHW>',
        '<UsedFor_Cooling>true</UsedFor_Cooling>',
        '<UsedFor_Ventilation>false</UsedFor_Ventilation>',
        '<UsedFor_Humidification>false</UsedFor_Humidification>',
        '<UsedFor_Dehumidification>false</UsedFor_Dehumidification>',
        '<PH_Parameters>',
        '<AuxiliaryEnergy>None</AuxiliaryEnergy>',
        '<AuxiliaryEnergyDHW>None</AuxiliaryEnergyDHW>',
        '<InConditionedSpace>true</InConditionedSpace>',
        '<AnnualCOP>4</AnnualCOP>',
        '<TotalSystemPerformanceRatioHeatGenerator>0.25</TotalSystemPerformanceRatioHeatGenerator>',
        '<HPType>3</HPType>',
        '</PH_Parameters>',
        '<DHW_Parameters>',
        '<CoverageWithinSystem>0.0</CoverageWithinSystem>',
        '<Unit>0.0</Unit>',
        '<Selection>1</Selection>',
        '</DHW_Parameters>',
        '<Heating_Parameters>',
        '<CoverageWithinSystem>0.0</CoverageWithinSystem>',
        '<Unit>0.0</Unit>',
        '<Selection>1</Selection>',
        '</Heating_Parameters>',
        '</Device>',
        '</Devices>',
        '<PHDistribution>',
        '<DistributionCooling>',
        '<PanelCooling>true</PanelCooling>',
        '<DehumdificationCOP>4</DehumdificationCOP>',
        '</DistributionCooling>',
        '<UseDefaultValues>true</UseDefaultValues>',
        '<DeviceInConditionedSpace>true</DeviceInConditionedSpace>',
        '</PHDistribution>',
        '</System>',
        '</Systems>'
    ]
