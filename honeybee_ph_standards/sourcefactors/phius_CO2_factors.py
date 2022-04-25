# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Phius CO2-Emission Factor Library"""

# -- As per "Phius Core_Phius Zero_Final Modeling Protocol v1.1.pdf"
# -- https://www.phius.org/PHIUS+2021/Phius%20Core_Phius%20Zero_Final%20Modeling%20Protocol%20v1.1.pdf

factors_2021 = {
    "OIL": {"value": 309.9966, "unit": "g/kWh"},
    "NATURAL_GAS": {"value": 250.0171, "unit": "g/kWh"},
    "LPG": {"value": 270.0102, "unit": "g/kWh"},
    "HARD_COAL": {"value": 439.9864, "unit": "g/kWh"},
    "WOOD": {"value": 53.4289, "unit": "g/kWh"},
    "ELECTRICITY_MIX": {"value": 680.0068, "unit": "g/kWh"},
    "ELECTRICITY_PV": {"value": 250.0171, "unit": "g/kWh"},
    "HARD_COAL_CGS_70_CHP": {"value": 239.9864, "unit": "g/kWh"},
    "HARD_COAL_CGS_35_CHP": {"value": 319.9932, "unit": "g/kWh"},
    "HARD_COAL_CGS_0_CHP": {"value": 409.9966, "unit": "g/kWh"},
    "GAS_CGS_70_CHP": {"value": -70.0102, "unit": "g/kWh"},
    "GAS_CGS_35_CHP": {"value": 129.9898, "unit": "g/kWh"},
    "GAS_CGS_0_CHP": {"value": 319.9932, "unit": "g/kWh"},
    "OIL_CGS_70_CHP": {"value": 100, "unit": "g/kWh"},
    "OIL_CGS_35_CHP": {"value": 250.0171, "unit": "g/kWh"},
    "OIL_CGS_0_CHP": {"value": 409.9966, "unit": "g/kWh"},
}
