# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

""""""
from typing import Optional, List
from collections.abc import Callable

from PHX.to_WUFI_XML import xml_schemas
from PHX.to_WUFI_XML.xml_writables import xml_writable


class NoXMLSchemaFoundError(Exception):
    def __init__(self, _schema_module, _hbobj, _schema_nm):
        self.message = (
            f'\n  Error: Cannot find an XML write schema for the object: "{_hbobj}"'
            f'\n  of type "{type(_hbobj)}" using the schema name of: "{_schema_nm}"'
            f'\n  in file: "{_schema_module.__file__}". Please check the schemas.'
        )
        super(NoXMLSchemaFoundError, self).__init__(self.message)


def get_HB_object_conversion_schema(_hb_object, _schema_name: Optional[str]) -> Callable:
    """Returns the appropriate XML write schema function for the Honeybee-object.

    Arguments:
    ----------
        * _hb_object (Any): The Object to find the WUFI-XML write schema for.
        * _schema_name (str | None): Optional user-defined name of the XML schema to use.
            If None is supplied, will use the object name preceded by an underscore. Ie:
            "Room" will search for "_Room".
    Returns:
    --------
        * schema_function (Callable[])

    Raises:
    -------
        * NoXMLSchemaFoundError: If no valid XML conversion schema is found for the 
            designated object.
    """

    # -- Schema Name
    if _schema_name is None:
        _schema_name = "_{}".format(_hb_object.__class__.__name__)

    # -- Schema Function
    schema_function = getattr(xml_schemas, _schema_name, None)
    if not schema_function:
        raise NoXMLSchemaFoundError(
            xml_schemas, _hb_object, _schema_name)

    return schema_function


def convert_HB_object_to_xml_writables_list(_hb_object, _schema_nm: Optional[str] = None) -> List[xml_writable]:
    """Returns a list of the Honeybee-Object's Properties in WUFI-XML format.

        * _hb_object (?): The Honeybee-object to convert into XML text.
        * _schema_nm (str | None): The name of the conversion schema to use for the object.

    Returns:
    --------
        * list[to_WUFI_XML.xml_writables.xml_writable]:

        ie: [
            XML_Node('IdentNr', 2),
            XML_Node('Name', 'My-Object'),
            XML_List( ... ),
            ...
            ]
    """

    # -- Get the right XML conversion function for the object
    conversion_schema = get_HB_object_conversion_schema(_hb_object, _schema_nm)

    # # -- Convert the object to an XML Node List
    return conversion_schema(_hb_object)
