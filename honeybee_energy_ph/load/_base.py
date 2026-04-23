# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBE-PH Appliance (Elec Equip.) Base Class"""

import uuid


class _Base(object):
    """Base class for any HB-Energy-PH appliance / electric equipment object.

    Provides auto-generated UUID identifier, display_name, and user_data.

    Attributes:
        identifier (str): Auto-generated UUID string.
        display_name (str): Human-readable name (falls back to identifier).
        user_data (dict): Optional metadata dictionary.
    """

    def __init__(self):
        self._identifier = uuid.uuid4()
        self.user_data = {}
        self._display_name = self.identifier

    @property
    def identifier(self):
        # type: () -> str
        """Unique identifier string (UUID)."""
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
        """First segment of the UUID (for display)."""
        return str(self.identifier).split("-")[0]

    def __str__(self):
        return "HBEPH_{}: ID-{}".format(self.__class__.__name__, self.identifier_short)

    def ToString(self):
        return str(self)

    def __repr__(self):
        return "{}(identifier={!r}, user_data={!r})".format(
            self.__class__.__name__, self.identifier_short, self.user_data
        )
