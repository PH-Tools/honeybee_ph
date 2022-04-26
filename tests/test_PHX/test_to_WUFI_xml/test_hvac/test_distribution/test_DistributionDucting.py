from PHX.to_WUFI_XML import xml_schemas


def test_Duct_Schema(reset_class_counters):
    result = xml_schemas._Duct(None)
    assert result == []
