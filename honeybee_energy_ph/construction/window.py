# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""" """

from honeybee.properties import FaceProperties, _Properties
from honeybee_energy.construction.window import WindowConstruction as HB_WindowConstruction


class WindowConstructionPHProperties(FaceProperties):
    def __init__(self, *args, **kwargs):
        super(WindowConstructionPHProperties, self).__init__(*args, **kwargs)
        self.id_num = 0


class WindowConstructionProperties(_Properties):
    def __repr__(self):
        return "PHX_WindowConstructionProperties: {!r}".format(self.host)


class PHX_WindowConstruction(HB_WindowConstruction):
    """Subclass honeybee_energy's WindowConstruction so it can have .properties"""

    __slots__ = ("properties",)

    def __init__(self, *args, **kwargs):
        super(PHX_WindowConstruction, self).__init__(*args, **kwargs)
        self.properties = WindowConstructionProperties(self)

    @classmethod
    def from_hb_construction(cls, _hb_construction):
        # type: (HB_WindowConstruction) -> PHX_WindowConstruction
        obj = cls(
            _hb_construction.identifier,
            _hb_construction.materials,
        )

        return obj

    def __repr__(self):
        return "PHX_WindowConstruction: {}".format(self.display_name)
