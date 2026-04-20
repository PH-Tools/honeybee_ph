# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Base class for Honeybee-PH Objects with some generic methods and attributes."""

import uuid
from copy import copy


class _Base(object):
    """Base class for all Honeybee-PH model objects.

    Provides a unique identifier, user-facing display name, and a user_data
    dictionary for arbitrary metadata. All PH model classes inherit from this.

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

    def set_base_attrs_from_source(self, _source):
        # type: (_Base) -> _Base
        """Copy identifier, user_data, and display_name from another _Base instance.

        Arguments:
        ----------
            * _source (_Base): The source object to copy base attributes from.

        Returns:
        --------
            * _Base: This object (self), with base attributes updated.
        """
        self._identifier = _source._identifier
        self.user_data = copy(_source.user_data)
        self._display_name = _source._display_name
        return self

    def __str__(self):
        return "HBPH_{}: ID-{}".format(self.__class__.__name__, self.identifier_short)

    def ToString(self):
        return str(self)

    def __repr__(self):
        return "{}(identifier={!r}, user_data={!r})".format(
            self.__class__.__name__, self.identifier_short, self.user_data
        )
