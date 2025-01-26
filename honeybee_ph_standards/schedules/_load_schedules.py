# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility function to load HB-E-Schedule Objects from a JSON file."""

import json
import os

try:
    from honeybee_energy.schedule.ruleset import ScheduleRuleset
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy:\n\t{}".format(e))

def is_schedule(_json_object):
    # type: (dict) -> bool
    """Check if a JSON object is a valid 'ScheduleRuleset' dict."""
    if "type" not in _json_object:
        return False
    if not _json_object["type"] == "ScheduleRuleset":
        return False
    return True


def load_schedules_from_json_file(_schedules_filepath):
    # type: (str) -> dict[str, ScheduleRuleset]
    """Load a set of HBE-ScheduleRuleset object from a JSON file."""
    if not os.path.exists(_schedules_filepath):
        raise ValueError("File not found: {}".format(_schedules_filepath))

    with open(_schedules_filepath, "r") as json_file:
        all_schedules = (ScheduleRuleset.from_dict(d) for d in json.load(json_file) if is_schedule(d))
        return {_.identifier: _ for _ in all_schedules}
