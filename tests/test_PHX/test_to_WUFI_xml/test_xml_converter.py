import pytest
from PHX.to_WUFI_XML import xml_converter, xml_schemas
from PHX.model import project


def test_get_PHX_object_conversion_schema_with_valid_PHX():
    phx_obj = project.PhxProject()
    correct_func = xml_schemas._PhxProject
    found_func = xml_converter.get_PHX_object_conversion_schema(phx_obj)

    assert found_func == correct_func


def test_get_PHX_object_conversion_schema_with_valid_PHX_schema_name_override():
    phx_obj = project.PhxProject()
    correct_func = xml_schemas._PhxBuilding
    found_func = xml_converter.get_PHX_object_conversion_schema(phx_obj, '_PhxBuilding')

    assert found_func == correct_func


def test_get_PHX_object_conversion_schema_with_valid_PHX_error():
    class NotPhx:
        ...

    phx_obj = NotPhx()
    with pytest.raises(xml_converter.NoXMLSchemaFoundError):
        found_func = xml_converter.get_PHX_object_conversion_schema(phx_obj)
