# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Phius Source Energy Factor Library"""

# -- As per "Phius Core_Phius Zero_Final Modeling Protocol v1.1.pdf"
# -- https://www.phius.org/PHIUS+2021/Phius%20Core_Phius%20Zero_Final%20Modeling%20Protocol%20v1.1.pdf

factors_2021 = {
    "OIL": {"value": 1.1, "unit": "kWh/kWh"},
    "NATURAL_GAS": {"value": 1.1, "unit": "kWh/kWh"},
    "LPG": {"value": 1.1, "unit": "kWh/kWh"},
    "HARD_COAL": {"value": 1.1, "unit": "kWh/kWh"},
    "WOOD": {"value": 0.2, "unit": "kWh/kWh"},
    "ELECTRICITY_MIX": {"value": 1.8, "unit": "kWh/kWh"},
    "ELECTRICITY_PV": {"value": 1.7, "unit": "kWh/kWh"},
    "HARD_COAL_CGS_70_CHP": {"value": 0.8, "unit": "kWh/kWh"},
    "HARD_COAL_CGS_35_CHP": {"value": 1.1, "unit": "kWh/kWh"},
    "HARD_COAL_CGS_0_CHP": {"value": 1.5, "unit": "kWh/kWh"},
    "GAS_CGS_70_CHP": {"value": 0.7, "unit": "kWh/kWh"},
    "GAS_CGS_35_CHP": {"value": 1.1, "unit": "kWh/kWh"},
    "GAS_CGS_0_CHP": {"value": 1.5, "unit": "kWh/kWh"},
    "OIL_CGS_70_CHP": {"value": 0.8, "unit": "kWh/kWh"},
    "OIL_CGS_35_CHP": {"value": 1.1, "unit": "kWh/kWh"},
    "OIL_CGS_0_CHP": {"value": 1.5, "unit": "kWh/kWh"},
}
