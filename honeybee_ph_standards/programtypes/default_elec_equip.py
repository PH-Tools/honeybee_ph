# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Default data for Residential PH Electrical Appliances (PHI and Phius)."""

from honeybee_energy_ph.load._ph_equip_types import (
    PhClothesDryerType,
    PhClothesWasherType,
    PhCookingType,
    PhDishwasherType,
)

ph_default_equip = {
    "PhDishwasher": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,  # Year
            "energy_demand": 0,  # kWh
            "energy_demand_per_use": 1.1,
            "combined_energy_factor": 0,
            "capacity_type": 1,  # Standard
            "capacity": 12,
            "water_connection": PhDishwasherType("2-COLD WATER CONNECTION"),
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,  # Year
            "energy_demand": 269,  # kWh
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "capacity_type": 1,  # Standard
            "capacity": 12,
            "water_connection": PhDishwasherType("2-COLD WATER CONNECTION"),
        },
    },
    "PhClothesWasher": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,  # Year
            "energy_demand": 0,
            "energy_demand_per_use": 1.1,
            "combined_energy_factor": 0,
            "capacity": 0.1274,
            "modified_energy_factor": 2.7,
            "water_connection": PhClothesWasherType("2-COLD WATER CONNECTION"),
            "utilization_factor": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,  # Year
            "energy_demand": 120,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "capacity": 0.1274,
            "modified_energy_factor": 2.7,
            "water_connection": PhClothesWasherType("2-COLD WATER CONNECTION"),
            "utilization_factor": 1.0,
        },
    },
    "PhClothesDryer": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,  # CEF - Combined Energy Factor
            "energy_demand": 0,
            "energy_demand_per_use": 3.5,
            "combined_energy_factor": 3.93,
            "dryer_type": PhClothesDryerType("4-CONDENSATION DRYER"),
            "gas_consumption": 0,
            "gas_efficiency_factor": 2.67,
            "field_utilization_factor_type": 1,  # Timer controls
            "field_utilization_factor": 1.18,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,  # CEF - Combined Energy Factor
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 3.93,
            "dryer_type": PhClothesDryerType("5-ELECTRIC EXHAUST AIR DRYER"),
            "gas_consumption": 0,
            "gas_efficiency_factor": 2.67,
            "field_utilization_factor_type": 1,  # Timer controls
            "field_utilization_factor": 1.18,
        },
    },
    "PhRefrigerator": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 4,  # PH case Units
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Day
            "energy_demand": 0,
            "energy_demand_per_use": 0.78,
            "combined_energy_factor": 0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 4,  # PH case Units
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Day
            "energy_demand": 1.0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
        },
    },
    "PhFreezer": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 4,  # PH case Units
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Day
            "energy_demand": 1.0795, # 394 kWh/year
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 4,  # PH case Units
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Day
            "energy_demand": 1.0795, # 394 kWh/year
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
        },
    },
    "PhFridgeFreezer": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 4,  # PH case Units
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Day
            "energy_demand": 0,
            "energy_demand_per_use": 1.0,
            "combined_energy_factor": 0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 4,  # PH case Units
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Day
            "energy_demand": 1.22,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
        },
    },
    "PhCooktop": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0.0,  # kWh/use
            "energy_demand_per_use": 0.25,  # kWh/use
            "combined_energy_factor": 0,
            "cooktop_type": PhCookingType("1-ELECTRICITY"),
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 1,  # PH case occupants
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0.2,  # kWh/use
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "cooktop_type": PhCookingType("1-ELECTRICITY"),
        },
    },
    "PhPhiusMEL": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 3,  # Bedrooms
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 3,  # Bedrooms
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
        },
    },
    "PhPhiusLightingInterior": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 6,  # PH case floor area
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 6,  # PH case floor area
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
    },
    "PhPhiusLightingExterior": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 6,  # PH case floor area
            "quantity": 1,
            "in_conditioned_space": False,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 6,  # PH case floor area
            "quantity": 1,
            "in_conditioned_space": False,
            "reference_energy_norm": 1,  # Use
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
    },
    "PhPhiusLightingGarage": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 2,
            "quantity": 0,
            "in_conditioned_space": False,
            "reference_energy_norm": 2,
            "energy_demand": 100,
            "energy_demand_per_use": 100,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 2,
            "quantity": 0,
            "in_conditioned_space": False,
            "reference_energy_norm": 2,
            "energy_demand": 100,
            "energy_demand_per_use": 100,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
    },
    "PhCustomAnnualElectric": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 5,
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 5,
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
    },
    "PhCustomAnnualLighting": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 5,
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 5,
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
    },
    "PhCustomAnnualMEL": {
        "PHI": {
            "comment": "default",
            "reference_quantity": 5,
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
        "PHIUS": {
            "comment": "default",
            "reference_quantity": 5,
            "quantity": 1,
            "in_conditioned_space": True,
            "reference_energy_norm": 2,
            "energy_demand": 0,
            "energy_demand_per_use": 0,
            "combined_energy_factor": 0,
            "frac_high_efficiency": 1.0,
        },
    },
}
