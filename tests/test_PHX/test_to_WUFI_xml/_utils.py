# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Utility / cleanup functions used during tests"""

from typing import List


def xml_string_to_list(_xml_string: str) -> List[str]:
    """Returns a list of the XML items, with the header and footer removed as well."""

    xml_string_items = _xml_string.replace('\t', '').rstrip().lstrip().split('\n')

    # -- remove the [<?xml version="1.0" ?>', '<>', ...... '</>'] items
    xml_string_items = xml_string_items[2:]
    xml_string_items = xml_string_items[:-1]
    return xml_string_items
