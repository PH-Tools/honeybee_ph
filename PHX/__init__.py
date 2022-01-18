# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Domain-Model Classes

The data classes in this package match the strucure and relationships of a Passive House building and are created at write-time from the 
Honeybee model objects. The WUFI structure differs significantly from the Honeybee Model structure and so many 
translations and conversions need to take place. The objects here are subsequently passed along to the xml_schemas 
for writing to file, and these xml-schemas contain the actual WUFI XML node names and ordering.
"""
