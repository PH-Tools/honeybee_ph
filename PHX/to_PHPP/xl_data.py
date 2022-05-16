# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Basic datatypes / structures relevant for Excel"""

from typing import Union, Optional
import string

xl_writable = Optional[Union[str, float, int, list, tuple]]
xl_range_value = Optional[Union[str, float, int]]


class XlItem:
    __slots__ = ('sheet_name', 'range', 'value')

    def __init__(self, sheet_name: str, range: str, value: xl_writable):
        self.sheet_name = sheet_name
        self.range = range
        self.value = value

    def __str__(self):
        return f'{self.__class__.__name__}({self.sheet_name}, {self.range}, {self.value})'

    def __repr__(self):
        return f'{self.__class__.__name__}(sheet_name={self.sheet_name}, range={self.range}, value={self.value})'


def xl_ord(_col: str) -> int:
    """ord() which supports excel columns beyond Z (AA, AB, ...)"""
    num = 0
    for c in _col.upper():
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num + 64


def xl_chr(_i: int) -> str:
    """chr() which supports excel columns beyond Z (AA, AB, ...)"""
    letters = ''
    num = _i - 64
    while num:
        mod = (num - 1) % 26
        letters += chr(mod + 65)
        num = (num - 1) // 26
    return ''.join(reversed(letters))


def col_offset(_col: str, _offset: int) -> str:
    """Return a column character, offset from the base by a specified amount."""
    base = xl_ord(_col)
    new = base + _offset
    return xl_chr(new)
