# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility function for creating a simple Histrogram from a data set."""

try:
    from typing import Collection
except:
    pass  # IronPython

from collections import defaultdict, namedtuple


def generate_histogram(_data, _num_bins):
    # type: (Collection[float], int) -> dict[int, dict[str, float]]
    """Creates a Histogram of input data, in n-bins.

    Arguments:
    ----------
        * _data (Collection[float]): Collection of numeric values to use as the data source.
        * _num_bins (int): Number of bins to split the input data set into.

    Returns:
    --------
        * dict[int, dict[str, float]]: ie: 
            {
                0: {'average_value'=12.0, 'frequency'=0.25},
                1: {'average_value'=6.0, 'frequency'=0.34},
                2: ...
            },
    """

    # -- Bin the data
    binned_data = defaultdict(list)
    maximum = max(_data)
    minimum = min(_data)
    val_range = maximum - minimum

    if val_range == 0:
        binned_data[0] = _data
    else:
        for d in _data:
            normalized_value = (maximum - d) / val_range
            bin = round(normalized_value * (_num_bins - 1))
            binned_data[bin].append(d)

    # -- Format the data for output

    output = {}
    for k, v in binned_data.items():
        output[k] = {
            'average_value': (sum(v) / len(v)) if len(v) > 0 else 0,
            'frequency': len(v) / len(_data)
        }

    return output
