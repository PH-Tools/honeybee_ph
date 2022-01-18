# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to build up an XML file from a Honeybee Object"""

from typing import Union
from xml.dom.minidom import Document, Element
from PHX.project import Project
import to_WUFI_XML.xml_writables
import to_WUFI_XML.xml_converter


def _xml_str(_: Union[str, bool]) -> str:
    """Util: Handle converting Boolean values to xml text format properly"""

    if isinstance(_, bool):
        if _:
            return "true"
        else:
            return "false"
    else:
        return str(_)


def add_node_attributes(_data: to_WUFI_XML.xml_writables.xml_writable, _element: Element) -> None:
    """Sets in any Node Attribute data on the Element, if any is found.

    Arguments:
    ----------
        * _data (PyPH_WUFI.xml_writables.xml_writable): The XML Data object to use as the source
        * _elememt (xml.dom.minidom.Element): The XML Element to set the Attributes for.
    """

    if _data.attr_value is not None:
        _element.setAttributeNS(
            None, str(_data.attr_name), str(_data.attr_value))


def _add_text_node(_doc: Document, _parent_node: Element, _data: to_WUFI_XML.xml_writables.xml_writable) -> None:
    """Adds a basic text-node ie: "<node_name>node_value</node_name>" to the XML Parent Node.

    Arguments:
    ----------
        * _doc (xml.dom.minidom.Document): The XML document to operate on.
        * _parent_node (xml.dom.minidom.Element): The XML element to use as the 'parent' node.
        * _data (to_WUFI_XML.xml_writables.xml_writable): The new XML_writable object to add to the 'parent' node.
    """

    # -- 1) Create the new text-node
    new_text_node = _doc.createTextNode(_xml_str(_data.node_value))

    # -- 2) Create a new Element
    new_element = _doc.createElementNS(None, _xml_str(_data.node_name))

    # -- 3) Add the new text-node to the new Element
    new_element.appendChild(new_text_node)

    # ---4) Add the Optional Node Attributes
    add_node_attributes(_data, new_element)

    # --- 5) Add the Element to the parent
    _parent_node.appendChild(new_element)


def add_children(_doc: Document, _parent_node: Element, _item: to_WUFI_XML.xml_writables.xml_writable) -> None:
    """Adds 'child' nodes to the XML Document and parent node recursively.

    If the _item passed in is a basic type like a string or number (to_WUFI_XML.xml_writables.XML_Node),
    it will just get added directly to the XML document. If the _item is an Object (to_WUFI_XML.xml_writables.XML_Object), 
    the functuon 'to_WUFI_XML.xml_converter.convert_HB_object_to_xml_writables_list()' will get called on the object, 
    and all returned attributes will be added to the XML document. If _item is a list (to_WUFI_XML.xml_writables.XML_List) 
    then each item in the list gets added to the XML document in turn.

    Arguments:
    ----------
        * _doc (xml.dom.minidom.doc): The XML Document to operate on.
        * _parent_node (xml.dom.minidom.Element): The XML element to use as the 'parent' node.
        * _item (to_WUFI_XML.xml_writables.xml_writable): The XML Data Node/Object/List to add to the parent node.
    """

    if isinstance(_item, to_WUFI_XML.xml_writables.XML_Node):
        # -- Basic Node, write out the value
        _add_text_node(_doc, _parent_node, _item)

    elif isinstance(_item, to_WUFI_XML.xml_writables.XML_Object):
        # -- Add a new node for the object, then try and add all its fields
        new_parent_node = _doc.createElementNS(None, _xml_str(_item.node_name))
        add_node_attributes(_item, new_parent_node)
        _parent_node.appendChild(new_parent_node)

        for item in to_WUFI_XML.xml_converter.convert_HB_object_to_xml_writables_list(
            _item.node_object, _item.schema_name
        ):
            add_children(_doc, new_parent_node, item)

    elif isinstance(_item, to_WUFI_XML.xml_writables.XML_List):
        # -- Add a new node for the 'container', and then add each item in the list
        new_parent_node = _doc.createElementNS(None, _xml_str(_item.node_name))
        add_node_attributes(_item, new_parent_node)
        _parent_node.appendChild(new_parent_node)

        for each_item in _item.node_items:
            add_children(_doc, new_parent_node, each_item)


def generate_WUFI_XML_for_Project(_project: Project) -> str:
    """Create all the XML Nodes as text for the input Honeybee Model

    Arguments:
    ----------
        * _project (Project): The WUFI Project to generate the XML Text for

    Returns:
    --------
        * (str) The XML Nodes as text.
    """

    doc = Document()
    root = doc.createElementNS(None, "WUFIplusProject")
    doc.appendChild(root)

    for item in to_WUFI_XML.xml_converter.convert_HB_object_to_xml_writables_list(_project):
        add_children(doc, root, item)

    return doc.toprettyxml()
