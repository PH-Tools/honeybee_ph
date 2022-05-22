# honeybee_energy_ph
These modules extend the [Honeybee-Energy](https://github.com/ladybug-tools/honeybee-energy) classes in order to allow for the modeling of detailed Passive House style attributes. Wherever possible, the classes here seek to align with and add to the existing HB API rather than create entirely new entities.

# Usage
The classes here will automatically extend the existing Honeybee-Energy objects at import time. This is done through the [_extend_honeybee_energy_ph.py](https://github.com/PH-Tools/honeybee_ph/blob/phpp_exporter/honeybee_energy_ph/_extend_honeybee_energy_ph.py) module which will be called by Honeybee-Energy at import time.

# Python Version:
All Classes should be written to comply with Python 2.7 (IronPython) format <u>only</u>. Because these classes are used within the McNeel Rhinoceros/Grasshopper platform, all classes must be backwards compatible to Python 2.7 / IronPython.

Note: It is recommended to include type hints for documentation purposes on all classes and functions. For details on type hints in Python 2.7, See: [MYPY Type hints in Python 2](https://mypy.readthedocs.io/en/stable/cheat_sheet.html)

<i>Note: Grasshopper IronPython does NOT include the 'typing' module for some reason - ensure that no modules 'import typing' or it will raise an error when Grasshopper attempts to import. Nest all 'import typing' inside a try...except.</i>