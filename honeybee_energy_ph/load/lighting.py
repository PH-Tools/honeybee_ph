# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing Honeybee-Energy | Load | Lighting"""

from honeybee_energy.load.lighting import Lighting


class PH_Lighting(Lighting):
    __slots__ = ("_test_attr",)

    def __init__(self, *args, **kwargs):
        super(PH_Lighting, self).__init__(*args, **kwargs)
        self._test_attr = self.watts_per_area

    @classmethod
    def from_hb_lighting(cls, _hb_lighting):
        # type: (PH_Lighting, Lighting) -> PH_Lighting
        new_ph_obj = cls(
            identifier=_hb_lighting.identifier,
            watts_per_area=_hb_lighting.watts_per_area,
            schedule=_hb_lighting.schedule,
            return_air_fraction=_hb_lighting.return_air_fraction,
            radiant_fraction=_hb_lighting.radiant_fraction,
            visible_fraction=_hb_lighting.visible_fraction,
        )

        return new_ph_obj

    def __setattr__(self, attr_name, value):
        # type: (PH_Lighting, str, Any) -> None
        if attr_name == "watts_per_area":
            self._test_attr = value
        return super(PH_Lighting, self).__setattr__(attr_name, value)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

    def __copy__(self):
        # type: (PH_Lighting) -> PH_Lighting
        new_hb_obj = super(PH_Lighting, self).__copy__()
        new_ph_obj = PH_Lighting.from_hb_lighting(new_hb_obj)
        new_ph_obj._test_attr = self._test_attr
        return new_ph_obj

    def to_dict(self, abridged=False):
        # type: (PH_Lighting, bool) -> dict
        base = super(PH_Lighting, self).to_dict(abridged=abridged)
        base.update({"_test_attr": self._test_attr})
        return base
