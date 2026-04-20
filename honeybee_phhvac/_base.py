# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment Base Class"""

import uuid
from copy import copy

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7


class _PhHVACBase(object):
    """Base class for all Honeybee-PH HVAC equipment objects.

    Provides a unique identifier, user-facing display name, and user_data
    dictionary. All PH-HVAC device and system classes inherit from this.

    Attributes:
        user_data (Dict): Arbitrary user-supplied metadata dictionary.
    """

    def __init__(self):
        self._identifier = uuid.uuid4()
        self.user_data = {}
        self._display_name = self.identifier

    @property
    def identifier(self):
        # type: () -> str
        """The globally unique identifier string for this object."""
        return str(self._identifier)

    @identifier.setter
    def identifier(self, _in):
        self._identifier = _in

    @property
    def display_name(self):
        # type: () -> str
        """User-facing name for this object, without character restrictions.

        If not set, defaults to the identifier.
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
        """The first segment of the identifier (before the first hyphen)."""
        return str(self.identifier).split("-")[0]

    @property
    def key(self):
        # type: () -> str
        """The dictionary key for this object (same as identifier)."""
        return self.identifier

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return "HB-PH-HVAC_{}: ID-{}".format(self.__class__.__name__, self.identifier_short)

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
            try:
                if v != getattr(other, k):
                    if str(v) != str(getattr(other, k)):  # Handle UUID Identifier
                        return False
            except AttributeError:
                return False
        return True
