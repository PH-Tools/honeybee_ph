# honeybee_ph_rhino
These modules include McNeel Rhino-3D specific classes which are only relevant for users working in the Rhino-3D / Grasshopper environment. The primary object used is the [gh_io.IGH](https://github.com/PH-Tools/honeybee_ph/blob/761d2d49e30c17950e739cf11aee964c8ded220f/honeybee_ph_rhino/gh_io.py#L60) Grasshopper Interface, which serves to hide Grasshopper specific API calls from the other packages which utilize these services. This is done to allow for testing of modules outside Grasshopper.

There are also IO Controller classes which are used by various Grasshopper Components for managing user-input objects and data.

# Usage
All classes here are designed to be used from within a GHPython Grasshopper Component and will not function outside that environment.

# Python Version:
All Classes should be written to comply with Python 2.7 (IronPython) format <u>only</u>. Because these classes are used within the McNeel Rhinoceros/Grasshopper platform, all classes must be backwards compatible to Python 2.7 / IronPython.

Note: It is recommended to include type hints for documentation purposes on all classes and functions. For details on type hints in Python 2.7, See: [MYPY Type hints in Python 2](https://mypy.readthedocs.io/en/stable/cheat_sheet.html)

<i>Note: Grasshopper IronPython does NOT include the 'typing' module for some reason - ensure that no modules 'import typing' or it will raise an error when Grasshopper attempts to import. Nest all 'import typing' inside a try...except.</i>