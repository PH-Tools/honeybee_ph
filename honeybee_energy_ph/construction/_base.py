# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Base class for all Constructions"""

try:
    from typing import Optional, Any
except ImportError:
    pass  # Python 2.7

from honeybee.typing import (
    valid_ep_string,
    clean_ep_string,
)


class _Base(object):
    def __init__(self, _identifier):
        self.id_num = 0
        self._identifier = _identifier  # type: str
        self._display_name = None  # type: Optional[str]
        self._user_data = {}  # type: dict

    @property
    def identifier(self):
        """Get the text string for unique construction identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = valid_ep_string(
            clean_ep_string(str(identifier)), "construction identifier"
        )

    @property
    def display_name(self):
        """Get or set a string for the object name without any character restrictions.

        If not set, this will be equal to the identifier.
        """
        if self._display_name is None:
            return self._identifier
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        try:
            self._display_name = str(value)
        except UnicodeEncodeError:  # Python 2 machine lacking the character set
            self._display_name = value  # keep it as unicode

    @property
    def user_data(self):
        # type: () -> dict
        """Get an optional dictionary for additional meta data for this object.

        This will be None until it has been set. All keys and values of this
        dictionary should be of a standard Python type to ensure correct
        serialization of the object to/from JSON (eg. str, float, int, list, dict)
        """
        return self._user_data

    @user_data.setter
    def user_data(self, value):
        # type: (dict) -> None
        if value is not None:
            assert isinstance(value, dict), (
                "Expected dictionary for honeybee_energy_ph"
                "object user_data. Got {}.".format(type(value))
            )
        self._user_data = value

    def to_dict(self):
        # type: () -> dict
        """Return all the base attribute values as a dict."""
        d = {}
        d["id_num"] = self.id_num
        d["identifier"] = str(self.identifier)
        d["display_name"] = self.display_name
        d["user_data"] = self.user_data
        return d

    def set_base_attrs_from_dict(self, _input_dict):
        # type: (dict[str, Any]) -> None
        """Set all the Base attribute values from an input dict."""
        self.id_num = _input_dict["id_num"]
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.user_data = _input_dict["user_data"]
        return None

    def set_base_attrs_from_obj(self, other):
        # type: (_Base) -> None
        """Sets the base attributes based on another object. Used during __copy__."""
        self.id_num = other.id_num
        self.identifier = other.identifier
        self.display_name = other.display_name
        self.user_data = other.user_data.copy()
        return None

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
