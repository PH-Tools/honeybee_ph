# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Preview Python Object and sub-objects"""

import uuid


def object_preview(_obj, _full=False, _level=1):

    if not hasattr(_obj, "__dict__"):
        print("{} object has no __dict__ attribute?".format(_obj))
        return None

    print("{}CLASS:: {}".format(" " * _level, _obj.__class__.__name__))
    for k, v in _obj.__dict__.items():
        if not _full:
            if type(v) == type(uuid.uuid4()):
                continue
            if "identifier" in k:
                continue
            if "user_data" == k:
                continue

        if hasattr(v, "__dict__"):
            print("{}+ [ {} ] ::: {}".format(" " * _level, k, v))
            object_preview(v, _full, _level=_level + 8)
        else:
            print("{}> {} ::: {}".format(" " * _level, k, v))
