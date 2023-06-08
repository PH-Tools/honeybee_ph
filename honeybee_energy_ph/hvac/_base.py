# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBE-PH HVAC Base Class"""

import uuid
from copy import copy

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7

class _PhHVACBase(object):
    """Base class for any HB-Energy-PH HVAC Objects"""

    def __init__(self):
        self._identifier = uuid.uuid4()
        self.user_data = {}
        self._display_name = self.identifier

    @property
    def identifier(self):
        return str(self._identifier)

    @identifier.setter
    def identifier(self, _in):
        self._identifier = _in

    @property
    def display_name(self):
        """Get or set a string for the object name without any character restrictions.
        If not set, this will be equal to the identifier.
        """
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        try:
            self._display_name = str(value)
        except UnicodeEncodeError:  # Python 2 machine lacking the character set
            self._display_name = value  # keep it as unicode

    @property
    def identifier_short(self):
        # type: () -> str
        return str(self.identifier).split("-")[0]

    @property
    def key(self):
        return self.identifier

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return "HBEPH_{}: ID-{}".format(self.__class__.__name__, self.identifier_short)

    def ToString(self):
        return str(self)

    def __repr__(self):
        return "{}(identifier={!r}, user_data={!r})".format(
            self.__class__.__name__, self.identifier_short, self.user_data
        )
    
    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d["identifier"] = copy(self.identifier)
        d["display_name"] = copy(self.display_name)
        d["user_data"] = copy(self.user_data)
        return d
    
    def from_dict(self, _input_dict):
        # type: (Dict[str, Any]) -> _PhHVACBase
        obj = self.__class__()
        obj.identifier = _input_dict["identifier"]
        obj.display_name = _input_dict["display_name"]
        obj.user_data = _input_dict["user_data"]
        return obj

    def __copy__(self):
        return self.duplicate()
    
    def duplicate(self):
        # type: () -> _PhHVACBase
        obj = self.__class__()

        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.user_data = copy(self.user_data)

        return obj
    
    def __eq__(self, other):
        # type: (_PhHVACBase) -> bool
        for k, v in self.__dict__.items():
            if v != getattr(other, k):
                if str(v) != str(getattr(other, k)): # Handle UUID Identifier
                    return False
        return True
    