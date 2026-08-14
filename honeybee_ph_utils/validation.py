# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Shared validation predicates for Honeybee-PH data models."""

import math
from numbers import Real

try:
    from typing import Any
except ImportError:
    pass  # IronPython 2.7


def is_finite_real(value):
    # type: (Any) -> bool
    """Return True for finite real numbers, excluding booleans."""
    return not isinstance(value, bool) and isinstance(value, Real) and not math.isnan(value) and not math.isinf(value)
