# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Preview Python Object and sub-objects"""

import uuid


def object_preview(_obj, _full=False, _level=1):
    # type: (object, bool, int) ->  None
    """"Recursively print all of an object's attributes and child-objects (and attributes).

    Arguments:
    ----------
        * _obj (obect): A python object to print the attributes of.
        * _full (bool): default=False. True=Print all the 'backend' attributes like 'identifier'.
            False=ignnore the 'backend' attributes.
        * _level (int): default=1. The 'inset' level from the left.

    Return:
    -------
        * None

    """

    if not hasattr(_obj, "__dict__"):
        print("{} object has no __dict__ attribute?".format(_obj))
        return None

    print("{}CLASS:: {}".format(" " * _level, _obj.__class__.__name__))

    for k, v in _obj.__dict__.items():
        if not _full:
            # Skip over some of the basic Honeybee-PH back-end attributes
            if type(v) == type(uuid.uuid4()):
                continue
            if "identifier" in k:
                continue
            if "user_data" == k:
                continue
            if "_host" == k:
                continue

        if hasattr(v, "__dict__"):
            print("{}+ [ {} ] ::: {}".format(" " * _level, k, v))

            # Reciursively step through all the child objects
            object_preview(v, _full, _level=_level + 8)
        else:
            print("{}> {} ::: {}".format(" " * _level, k, v))
