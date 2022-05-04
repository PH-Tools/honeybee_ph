from typing import Union, Optional

"""Basic datatypes / structures relevant for Excel"""

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
