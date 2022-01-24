# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH - ScheduleRuleset with .properties slot added. 

I wish there was a better way, but since hb-energy objects do not have a 
.properties, need to subclass them and add that first.
"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython

from honeybee_energy_ph.properties.ruleset import ScheduleRulesetProperties
from honeybee_energy.schedule.ruleset import ScheduleRuleset


class PH_ScheduleRuleset_FromDictError(Exception):
    def __init__(self, _expected_type, _input_type):
        self.msg = 'Error: from_dict expected "{}". Got: {}'.format(
            _expected_type, _input_type)
        super(PH_ScheduleRuleset_FromDictError, self).__init__(self.msg)


class PH_ScheduleRuleset(ScheduleRuleset):
    """Subclassing honeybee-energy ScheduleRuleset in order to add .properties slot."""

    def __init__(self, identifier, default_day_schedule, schedule_rules=None,
                 schedule_type_limit=None, holiday_schedule=None,
                 summer_designday_schedule=None, winter_designday_schedule=None):
        # -- Initialize the hb-energy base-class
        super(PH_ScheduleRuleset, self).__init__(identifier, default_day_schedule,
                                                 schedule_rules, schedule_type_limit, holiday_schedule,
                                                 summer_designday_schedule, winter_designday_schedule)

        # -- Add the new properties slot
        self._properties = ScheduleRulesetProperties(self)

    @property
    def properties(self):
        """Get object properties, including Radiance, Energy and other properties."""
        return self._properties

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = super(PH_ScheduleRuleset, self).to_dict(abridged)
        d['type'] = "ScheduleRulesetAbridged" if abridged else "ScheduleRuleset"
        d['properties'] = self.properties.to_dict(abridged)

        return d

    @classmethod
    def from_dict(cls, data):
        # type: (Any) -> PH_ScheduleRuleset
        data = data.copy()

        if data['type'] != 'ScheduleRuleset':
            raise PH_ScheduleRuleset_FromDictError(
                'PH_ScheduleRuleset', data.get('type'))

        ph_ruleset = super(PH_ScheduleRuleset, cls).from_dict(data)
        if data.get('properties', {}).get('type') == 'ScheduleRulesetProperties':
            ph_ruleset.properties._load_extension_attr_from_dict(data['properties'])

        return ph_ruleset

    @classmethod
    def from_dict_abridged(cls, data, schedule_type_limits):
        # type: (Any, Any) -> PH_ScheduleRuleset
        data = data.copy()

        if data['type'] == 'ScheduleRulesetAbridged':
            # -- Reset the type before passing to the parent.
            data['type'] = 'ScheduleRulesetAbridged'
        else:
            raise PH_ScheduleRuleset_FromDictError(
                'ScheduleRulesetAbridged', data.get('type'))

        ph_ruleset = super(PH_ScheduleRuleset, cls).from_dict_abridged(
            data, schedule_type_limits)
        if data.get('properties', {}).get('type') == 'SchdeduleRulesetPropertiesAbridged':
            ph_ruleset.properties._load_extension_attr_from_dict(data['properties'])

        return ph_ruleset

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        return '{}: {} [default day: {}] [{} rules]'.format(
            self.__class__.__name__, self.display_name,
            self.default_day_schedule.display_name, len(self._schedule_rules))
