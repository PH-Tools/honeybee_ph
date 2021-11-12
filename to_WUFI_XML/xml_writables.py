# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Classes used to build XML Node Objects which are used during XML Output"""

from typing import Union, Iterable, Any

# Type Alias
xml_writable = Union[str, float, int, bool, None]


class XML_Node:
    """A single node text/numeric item. Optional Attribute data"""

    def __init__(
        self, _node_name: str, _node_value: xml_writable, _attr_name: str = None, _attr_value: xml_writable = None
    ):
        self.node_name = _node_name
        self.node_value = _node_value
        self.attr_name = _attr_name
        self.attr_value = _attr_value


class XML_List:
    """A List of XML Writable objects. Used to add 'count' info to the list parent node"""

    def __init__(
        self, _node_name: str, _node_items: Iterable, _attr_name: str = "count", _attr_value: xml_writable = None
    ):
        self.node_name = _node_name
        self.node_items = _node_items
        self.attr_name = _attr_name
        self._attr_value = _attr_value

    @property
    def attr_value(self):
        if self._attr_value is not None:
            return self._attr_value
        else:
            # -- Used to automate the 'Index' node attr on List items
            return len(self.node_items)

    @attr_value.setter
    def attr_value(self, _in):
        self._attr_value = _in


class XML_Object:
    """XML Writable Object. Object fields will be writen out as child nodes"""

    def __init__(
        self,
        _node_name: str,
        _node_object: Any,
        _attr_name: str = None,
        _attr_value: xml_writable = None,
        _schema_name: str = None,
    ):
        """
        Arguments:
        ----------
            * _node_name (str): The XML name for the node.
            * _node_object (Any): The Honeybee Object to write to the node.
            * _attr_name (str | None): Optional XML node attribue name.
            * _attr_value (str | None): Optional XML node attribute value.
            * _schema_name (str | None): Optional explict name for xml_schema function to use when writing to XML.
                If None is passed, uses the class name preceded by and underscore.
        """

        self.node_name = _node_name
        self.node_object = _node_object
        self.attr_name = _attr_name
        self.attr_value = _attr_value
        self.schema_name = _schema_name


# For type hints...
xml_writable = Union[XML_Node, XML_List, XML_Object]
