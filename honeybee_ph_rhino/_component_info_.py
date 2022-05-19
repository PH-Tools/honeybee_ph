# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Names and meta-data for all the Honeybee-PH Grasshopper Components.
These are called when the component is instantiated within the Grasshopper canvas.
"""

RELEASE_VERSION = "HONEYBEE-PH v0.1"
CATEGORY = "Honeybee-PH"
SUB_CATGORIES = {
    0: "00 | Utils",
    4: "04 | Honeybee-PH",
    5: "05 | Temp",
    6: "06 | Temp",
}
COMPONENT_PARAMS = {
    "HBPH - Merge Rooms": {
        "NickName": "Merge HB Rooms",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Bldg Segment": {
        "NickName": "PH Bldg Segment",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Phius Certification": {
        "NickName": "Phius Cert.",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Phius Climate": {
        "NickName": "PH Climate",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create Spaces": {
        "NickName": "PH Spaces",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Vent. Schedule": {
        "NickName": "PH Vent. Sched.",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Operation Period": {
        "NickName": "PH Op. Period",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    # -- Spaces
    "HBPH - Get FloorSegment Data": {
        "NickName": "Get Seg. Data",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create Spaces": {
        "NickName": "Create PH Spaces",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Add Spaces": {
        "NickName": "Add PH Spaces",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Ventilator": {
        "NickName": "PH Ventilator",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Write WUFI XML": {
        "NickName": "Write WUFI XML",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create SHW Tank": {
        "NickName": "Create SHW Tank",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Add SHW Tank": {
        "NickName": "Add SHW Tank",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create SHW Heater": {
        "NickName": "Create SHW Heater",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Add SHW Heater": {
        "NickName": "Add SHW Heater",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create PH Equipment": {
        "NickName": "Create PH Equipment",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Add PH Equipment": {
        "NickName": "Add PH Equipment",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Set Res Occupancy": {
        "NickName": "Set Res Occupancy",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Phius MF Res Calculator": {
        "NickName": "Phius MF Res Calc",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Phius Program Finder": {
        "NickName": "Phius Programs",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create Conversion Factor": {
        "NickName": "Factor",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Add Mech Systems": {
        "NickName": "Add Mech",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create Heating System": {
        "NickName": "Create Heating",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create Cooling System": {
        "NickName": "Create Cooling",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create Ventilation System": {
        "NickName": "Create Vent",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create PH Window Frame Element": {
        "NickName": "Create Frame Element",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create PH Window Frame": {
        "NickName": "Create Frame",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create PH Glazing": {
        "NickName": "Create Glazing",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - Create PH Window Construction": {
        "NickName": "Create PH Win Const",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "HBPH - PHI Certification": {
        "NickName": "PHI Cert.",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },

}


class ComponentNameError(Exception):
    def __init__(self, _name, error):
        self.message = 'Error: Cannot get Component Params for: "{}"'.format(
            _name)
        print(error)
        super(ComponentNameError, self).__init__(self.message)


def set_component_params(ghenv, dev=False):
    # type (ghenv, Optional[str | bool]) -> None
    """
    Sets the visible attributes of the Grasshopper Component (Name, Date, etc..)

    Arguments:
    __________
        * ghenv: The Grasshopper Component 'ghenv' variable.
        * dev: (str | bool) Default=False. If False, will use the RELEASE_VERSION value as the
            'message' shown on the bottom of the component in the Grasshopper scene.
            If a string is passed in, will use that for the 'message' shown instead.

    Returns:
    --------
        * None:
    """

    try:
        compo_name = ghenv.Component.Name
        sub_cat_num = COMPONENT_PARAMS.get(
            compo_name, {}).get("SubCategory", 1)
        sub_cat_name = SUB_CATGORIES.get(sub_cat_num)
    except Exception as e:
        raise ComponentNameError(compo_name, e)

    # ------ Set the visible message
    if dev:
        msg = "DEV | {}".format(str(dev))
    else:
        msg = COMPONENT_PARAMS.get(compo_name, {}).get("Message")

    ghenv.Component.Message = msg

    # ------ Set the othere stuff
    ghenv.Component.NickName = COMPONENT_PARAMS.get(
        compo_name, {}).get("NickName")
    ghenv.Component.Category = CATEGORY
    ghenv.Component.SubCategory = sub_cat_name
    ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
