# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""A simplified custom Enum class since IronPython doesn't have an enum."""

try:
    from typing import Any, Union
except ImportError:
    pass  # IronPython


class ValueNotAllowedError(Exception):
    """Error raised when a value is not in the allowed list of a CustomEnum.

    Attributes:
        message (str): Human-readable error message showing the invalid
            value and the allowed options.
    """

    def __init__(self, _in, _enum):
        self.message = "Value: {} not allowed for enum {}.\nValid input: {} ".format(
            str(_in), _enum.__class__.__name__, _enum.allowed
        )
        super(ValueNotAllowedError, self).__init__(self.message)


class CustomEnum(object):
    """A simplified custom Enum class since IronPython doesn't have an enum.

    Subclass this and set ``allowed`` to a list of uppercase string values.
    Values can be set by name or by 1-based integer index.

    Attributes:
        allowed (list[str]): Class-level list of permitted string values.
        index_offset (int): Offset applied when converting integer input
            to a list index. Default: -1 (1-based indexing).

    Example usage:
    ```python
    class PhFoundationType(enumerables.CustomEnum):
        allowed = [
            "1-HEATED_BASEMENT",
            "2-UNHEATED_BASEMENT",
            "3-SLAB_ON_GRADE",
            "4-VENTED_CRAWLSPACE",
            "5-NONE",
        ]

        def __init__(self, _value=1):
            # type: (Union[str, int]) -> None
            super(PhFoundationType, self).__init__(_value)

    new_foundation_type = PhFoundationType("1-HEATED_BASEMENT")
    ```
    """

    allowed = []  # type: list[str]

    def __init__(self, _value="", _index_offset=-1):
        # type: (Union[str, int], int) -> None

        # Standard offset is 1 since most listings start at 1 (but not all)
        self.index_offset = _index_offset

        self._value = ""
        self.value = _value

    @property
    def allowed_upper(self):
        # type: () -> list[str]
        """Uppercase versions of all allowed values."""
        return [_.upper() for _ in self.allowed]

    @property
    def value(self):
        # type: () -> str
        """The current enum value as an uppercase string."""
        return str(self._value)

    @value.setter
    def value(self, _in):
        # type: (Union[str, int]) -> None
        """Allows the user to set the .value as one of the allowed values. If an
        integer is passed in, will attempt to find the corresponding value from the
        allowed-values list (1-based, ie: user-input '1' -> self.allowed.index(0) ).
        """

        if str(_in).upper() in self.allowed_upper:
            self._value = str(_in).upper()
        else:
            try:
                input = int(_in) + self.index_offset
                self._value = self.allowed_upper[input]
            except:
                raise ValueNotAllowedError(_in, self)

    @property
    def number(self):
        # type: () -> int
        """Returns the index pos of self.value (usually 1-based)"""
        return self.allowed_upper.index(self.value) - self.index_offset

    def __str__(self):
        return "{}(_value={} [number={}])".format(self.__class__.__name__, self.value, self.number)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}
        d["value"] = self.value
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, Any]) -> CustomEnum
        obj = cls(_dict.get("value", 1))
        return obj

    def __eq__(self, other):
        # type: (CustomEnum) -> bool
        return self.value == other.value and self.__class__ == other.__class__

    def __hash__(self):
        # type: () -> int
        return hash(self.value) + hash(self.__class__)
