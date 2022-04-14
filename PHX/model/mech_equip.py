# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Dict, Optional, Union, Any
from PHX.model.mech_equip_enums import SystemType, DeviceType, HeatPumpType


@dataclass
class PhxUsageProfile:
    """Is the device used to provide..."""
    space_heating: bool = False
    dhw_heating: bool = False
    cooling: bool = False
    ventilation: bool = False
    humidification: bool = False
    dehumidification: bool = False


class PhxMechanicalEquipment:
    """Base class for PHX Mechanical Devices (heaters, tanks, ventilators)"""
    _count: int = 0

    def __init__(self):
        self.system_type_num: SystemType = SystemType.ELECTRIC
        self.device_type_num: DeviceType = DeviceType.ELECTRIC

        self.display_name: str = '_unnamed_equipment_'
        self.id_num: int = self._count
        self.quantity: int = 0
        self.unit = 0.0
        self.in_conditioned_space: bool = True
        self.percent_coverage: float = 0.0
        self.usage_profile: PhxUsageProfile = PhxUsageProfile(
            False, False, False, False, False, False)
        self.aux_energy = 0.0
        self.aux_energy_dhw = 0.0
        self.params = None

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipment, cls).__new__(cls, *args, **kwargs)


# -----------------------------------------------------------------------------
# Ventilation


class PhxVentilator(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.VENTILATION
        self.device_type_num: DeviceType = DeviceType.VENTILATION
        self.usage_profile.ventilation = True

        # -- Device Params
        self.heat_recovery_efficiency: float = 0.0
        self.moisture_recovery_efficiency: float = 0.0
        self.fan_power: float = 0.55
        self.frost_protection_reqd: bool = True
        self.frost_temp: float = -5.0


# -----------------------------------------------------------------------------
# Heaters


class PhxHeaterElectric(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.ELECTRIC
        self.device_type_num: DeviceType = DeviceType.ELECTRIC


class PhxHeaterBoilerFossil(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.BOILER
        self.device_type_num: DeviceType = DeviceType.BOILER


class PhxHeaterBoilerWood(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.BOILER
        self.device_type_num: DeviceType = DeviceType.BOILER


PhxHeaterBoiler = Union[PhxHeaterBoilerFossil, PhxHeaterBoilerWood]


class PhxHeaterDistrictHeat(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.DISTRICT_HEAT
        self.device_type_num: DeviceType = DeviceType.DISTRICT_HEAT


class PhxHeaterHeatPumpParamsAnnual:
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    annual_COP: Optional[float] = None
    total_system_perf_ratio: Optional[float] = None


class PhxHeaterHeatPumpParamsMonthly:
    hp_type: HeatPumpType = HeatPumpType.RATED_MONTHLY
    COP_1: Optional[float] = None
    COP_2: Optional[float] = None
    ambient_temp_1: Optional[float] = None
    ambient_temp_2: Optional[float] = None


class PhxHeaterHeatPumpParamsHotWater:
    hp_type: HeatPumpType = HeatPumpType.HOT_WATER
    annual_COP: Optional[float] = None
    annual_system_perf_ratio: Optional[float] = None
    annual_energy_factor: Optional[float] = None


class PhxHeaterHeatPumpParamsCombined:
    hp_type: HeatPumpType = HeatPumpType.COMBINED


PhxHeaterHeatPumpParams = Union[PhxHeaterHeatPumpParamsAnnual,
                                PhxHeaterHeatPumpParamsMonthly,
                                PhxHeaterHeatPumpParamsHotWater,
                                PhxHeaterHeatPumpParamsCombined, ]


class PhxHeaterHeatPump(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.HEAT_PUMP
        self.device_type_num: DeviceType = DeviceType.HEAT_PUMP
        self.params: Optional[PhxHeaterHeatPumpParams] = None

    @classmethod
    def annual(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsAnnual()
        return new_obj

    @classmethod
    def monthly(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsMonthly()
        return new_obj

    @classmethod
    def hot_water(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsHotWater()
        return new_obj

    @classmethod
    def combined(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsCombined()
        return new_obj


PhxHeater = Union[PhxHeaterElectric,
                  PhxHeaterBoilerFossil,
                  PhxHeaterBoilerWood,
                  PhxHeaterDistrictHeat,
                  PhxHeaterHeatPump,
                  ]

# -----------------------------------------------------------------------------
# Water Storage


class PhxHotWaterTank(PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.system_type_num: SystemType = SystemType.WATER_STORAGE
        self.device_type_num: DeviceType = DeviceType.WATER_STORAGE

        # -- Device Params
        self.solar_losses: float = 0.0  # W/K
        self.storage_loss_rate: float = 0.0  # W
        self.standby_losses: float = 0.0  # W/K

        self.storage_capacity: float = 0.0  # Liter
        self.input_option: int = 1

        self.in_conditioned_space: bool = True
        self.tank_room_temp: float = 20.0
        self.tank_water_temp: float = 55.0

        self.aux_energy: float = 0.0
        self.aux_energy_dhw: float = 0.0


# -----------------------------------------------------------------------------

@dataclass
class PhxZoneCoverage:
    """Percentage of the load-type covered by the device."""
    zone_num: float = 1.0
    heating: float = 1.0
    cooling: float = 1.0
    ventilation: float = 1.0
    humidification: float = 1.0
    dehumidification: float = 1.0


@dataclass
class PhxMechanicalEquipmentCollection:
    """A collection of all the mechanical equipment (ERV, DHW, etc..) in the project"""
    _count: ClassVar[int] = 0
    id_num: int = 0
    display_name: str = "Ideal Air System"
    sys_type_num: int = 1
    sys_type_str: str = "User defined (ideal system)"

    zone_coverage: PhxZoneCoverage = field(default_factory=PhxZoneCoverage)
    _equipment: Dict[str, PhxMechanicalEquipment] = field(default_factory=dict)

    @property
    def equipment(self):
        return self._equipment.values()

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PhxMechanicalEquipmentCollection, cls).__new__(cls, *args, **kwargs)

    def equipment_in_collection(self, _equipment_key) -> bool:
        return _equipment_key in self._equipment.keys()

    def get_mech_equipment_by_key(self, _key: str) -> Optional[PhxMechanicalEquipment]:
        return self._equipment.get(_key, None)

    def add_new_mech_equipment(self, _key: str, _equipment: PhxMechanicalEquipment) -> None:
        """Adds a new PHX Mechanical Equipment device to the collection.

        Arguments:
        ----------
            * _key (str): The key to use when storing the new mechanical equipment
            * _equipment (PhxMechanicalEquipment): The new PHX mechanical equipment to 
                add to the collection.

        Returns:
        --------
            * None
        """
        self._equipment[_key] = _equipment
