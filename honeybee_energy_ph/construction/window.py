# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""" """

from honeybee.properties import FaceProperties, _Properties
from honeybee_energy.construction.window import WindowConstruction as HB_WindowConstruction


class WindowConstructionPhProperties:
    def __init__(self):
        self.id_num = 0

    def __repr__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)


class WindowConstructionProperties(_Properties):

    def __init__(self, host):
        super(WindowConstructionProperties, self).__init__(host)
        self._ph = WindowConstructionPhProperties()

    @property
    def ph(self):
        return self._ph

    def __repr__(self):
        return "{}(host={!r})".format(self.__class__.__name__, self.host)


class PH_WindowConstruction(HB_WindowConstruction):
    """Subclass honeybee_energy's WindowConstruction so it can have .properties"""

    __slots__ = ("_properties",)

    def __init__(self, *args, **kwargs):
        super(PH_WindowConstruction, self).__init__(*args, **kwargs)
        self._properties = WindowConstructionProperties(self)

    @property
    def properties(self):
        return self._properties

    @classmethod
    def from_hb_construction(cls, _hb_construction):
        # type: (HB_WindowConstruction) -> PH_WindowConstruction
        obj = cls(
            _hb_construction.identifier,
            _hb_construction.materials,
        )

        return obj

    def __repr__(self):
        return "PH_WindowConstruction: {}".format(self.display_name)
