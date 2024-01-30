# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""This is called during __init__ and extends the base honeybee class Properties with a new ._ph slot"""

from honeybee_energy.properties.extension import (
    AllAirSystemProperties,
    DOASSystemProperties,
    ElectricEquipmentProperties,
    EnergyMaterialNoMassProperties,
    EnergyMaterialProperties,
    EnergyMaterialVegetationProperties,
    HeatCoolSystemProperties,
    IdealAirSystemProperties,
    LightingProperties,
    OpaqueConstructionProperties,
    PeopleProperties,
    ServiceHotWaterProperties,
    SHWSystemProperties,
    WindowConstructionProperties,
    WindowConstructionShadeProperties,
)

# -- honeybee_energy properties objects
from honeybee_energy.schedule.ruleset import ScheduleRulesetProperties

from honeybee_energy_ph.properties.construction.opaque import (
    OpaqueConstructionPhProperties,
)
from honeybee_energy_ph.properties.construction.window import (
    WindowConstructionPhProperties,
)
from honeybee_energy_ph.properties.construction.windowshade import (
    WindowConstructionShadePhProperties,
)
from honeybee_energy_ph.properties.hot_water.hw_program import ServiceHotWaterPhProperties
from honeybee_energy_ph.properties.hot_water.hw_system import SHWSystemPhProperties
from honeybee_energy_ph.properties.hvac.allair import AllAirSystemPhProperties
from honeybee_energy_ph.properties.hvac.doas import DOASSystemPhProperties
from honeybee_energy_ph.properties.hvac.heatcool import HeatCoolSystemPhProperties
from honeybee_energy_ph.properties.hvac.idealair import IdealAirSystemPhProperties
from honeybee_energy_ph.properties.load.equipment import ElectricEquipmentPhProperties
from honeybee_energy_ph.properties.load.lighting import LightingPhProperties
from honeybee_energy_ph.properties.load.people import PeoplePhProperties
from honeybee_energy_ph.properties.materials.opaque import (
    EnergyMaterialNoMassPhProperties,
    EnergyMaterialPhProperties,
    EnergyMaterialVegetationPhProperties,
)

# -- honeybee_energy_ph properties objects
from honeybee_energy_ph.properties.ruleset import ScheduleRulesetPhProperties
from honeybee_energy_ph.properties.space import SpaceEnergyProperties
from honeybee_ph.properties.space import SpaceProperties

# Step 1)
# set a private ._ph attribute on each relevant HB-Energy Property class to None
setattr(SpaceProperties, "_energy", None)
setattr(ScheduleRulesetProperties, "_ph", None)
setattr(OpaqueConstructionProperties, "_ph", None)
setattr(EnergyMaterialProperties, "_ph", None)
setattr(EnergyMaterialNoMassProperties, "_ph", None)
setattr(EnergyMaterialVegetationProperties, "_ph", None)
setattr(WindowConstructionProperties, "_ph", None)
setattr(WindowConstructionShadeProperties, "_ph", None)
setattr(ServiceHotWaterProperties, "_ph", None)
setattr(SHWSystemProperties, "_ph", None)
setattr(ElectricEquipmentProperties, "_ph", None)
setattr(PeopleProperties, "_ph", None)
setattr(LightingProperties, "_ph", None)
setattr(IdealAirSystemProperties, "_ph", None)
setattr(AllAirSystemProperties, "_ph", None)
setattr(DOASSystemProperties, "_ph", None)
setattr(HeatCoolSystemProperties, "_ph", None)

# Step 2)
# create methods to define the public .property.<extension> @property instances on each obj.properties container


def space_energy_properties(self):
    if self._energy is None:
        self._energy = SpaceEnergyProperties(self.host)
    return self._energy


def schedule_ruleset_ph_properties(self):
    if self._ph is None:
        self._ph = ScheduleRulesetPhProperties(self.host)
    return self._ph


def opaque_construction_ph_properties(self):
    if self._ph is None:
        self._ph = OpaqueConstructionPhProperties()
    return self._ph


def energy_material_ph_properties(self):
    if self._ph is None:
        self._ph = EnergyMaterialPhProperties()
    return self._ph


def energy_material_no_mass_ph_properties(self):
    if self._ph is None:
        self._ph = EnergyMaterialNoMassPhProperties()
    return self._ph


def energy_material_vegetation_ph_properties(self):
    if self._ph is None:
        self._ph = EnergyMaterialVegetationPhProperties()
    return self._ph


def window_construction_ph_properties(self):
    if self._ph is None:
        self._ph = WindowConstructionPhProperties(self.host)
    return self._ph


def window_construction_shade_ph_properties(self):
    if self._ph is None:
        self._ph = WindowConstructionShadePhProperties(self.host)
    return self._ph


def hot_water_program_ph_properties(self):
    if self._ph is None:
        self._ph = ServiceHotWaterPhProperties(self.host)
    return self._ph


def hot_water_system_ph_properties(self):
    if self._ph is None:
        self._ph = SHWSystemPhProperties(self.host)
    return self._ph


def elec_equip_ph_properties(self):
    if self._ph is None:
        self._ph = ElectricEquipmentPhProperties(self.host)
    return self._ph


def people_ph_properties(self):
    if self._ph is None:
        self._ph = PeoplePhProperties(self.host)
    return self._ph


def lighting_ph_properties(self):
    if self._ph is None:
        self._ph = LightingPhProperties(self.host)
    return self._ph


def hvac_ideal_air_system_ph_properties(self):
    if self._ph is None:
        self._ph = IdealAirSystemPhProperties(self.host)
    return self._ph


def hvac_all_air_system_ph_properties(self):
    if self._ph is None:
        self._ph = AllAirSystemPhProperties(self.host)
    return self._ph


def hvac_doas_system_ph_properties(self):
    if self._ph is None:
        self._ph = DOASSystemPhProperties(self.host)
    return self._ph


def hvac_heatcool_system_ph_properties(self):
    if self._ph is None:
        self._ph = HeatCoolSystemPhProperties(self.host)
    return self._ph


# Step 3)
# add public .energy or .ph @property methods to the appropriate Properties classes
setattr(SpaceProperties, "energy", property(space_energy_properties))
setattr(ScheduleRulesetProperties, "ph", property(schedule_ruleset_ph_properties))
setattr(OpaqueConstructionProperties, "ph", property(opaque_construction_ph_properties))
setattr(WindowConstructionProperties, "ph", property(window_construction_ph_properties))
setattr(
    WindowConstructionShadeProperties,
    "ph",
    property(window_construction_shade_ph_properties),
)
setattr(EnergyMaterialProperties, "ph", property(energy_material_ph_properties))
setattr(
    EnergyMaterialNoMassProperties, "ph", property(energy_material_no_mass_ph_properties)
)
setattr(
    EnergyMaterialVegetationProperties,
    "ph",
    property(energy_material_vegetation_ph_properties),
)
setattr(ServiceHotWaterProperties, "ph", property(hot_water_program_ph_properties))
setattr(SHWSystemProperties, "ph", property(hot_water_system_ph_properties))
setattr(ElectricEquipmentProperties, "ph", property(elec_equip_ph_properties))
setattr(PeopleProperties, "ph", property(people_ph_properties))
setattr(LightingProperties, "ph", property(lighting_ph_properties))
setattr(IdealAirSystemProperties, "ph", property(hvac_ideal_air_system_ph_properties))
setattr(AllAirSystemProperties, "ph", property(hvac_all_air_system_ph_properties))
setattr(DOASSystemProperties, "ph", property(hvac_doas_system_ph_properties))
setattr(HeatCoolSystemProperties, "ph", property(hvac_heatcool_system_ph_properties))
