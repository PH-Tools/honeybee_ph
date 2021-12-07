# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing Honeybee-Energy | Load | Lighting"""

from honeybee_energy.load.lighting import Lighting

class PH_Lighting(Lighting):
    __slots__ = ('_test_attr')
    
    def __init__(self, *args, **kwargs):
        super(PH_Lighting, self).__init__(*args, **kwargs)
        self._test_attr = 'this is a test'
    
    @classmethod
    def from_hb_lighting(cls, _hb_lighting):
        new_ph_obj = cls(
            identifier=_hb_lighting.identifier,
            watts_per_area=_hb_lighting.watts_per_area,
            schedule=_hb_lighting.schedule,
            return_air_fraction=_hb_lighting.return_air_fraction,
            radiant_fraction=_hb_lighting.radiant_fraction,
            visible_fraction=_hb_lighting.visible_fraction,)
        
        return new_ph_obj
    
    def ToString(self):
        return 'My New PH_Lighting Object'
    
    def __copy__(self):
        new_hb_obj = super(PH_Lighting, self).__copy__()
        new_ph_obj = PH_Lighting.from_hb_lighting(new_hb_obj)
        new_ph_obj._test_attr = self._test_attr
        return new_ph_obj