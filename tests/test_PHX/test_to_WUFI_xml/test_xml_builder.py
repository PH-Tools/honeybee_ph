from PHX.to_WUFI_XML import xml_builder
from PHX.model import geometry


def test_generate_WUFI_XML_from_object():
    phx_obj = geometry.PhxVertix()
    txt = xml_builder.generate_WUFI_XML_from_object(phx_obj)
    txt = txt.replace("\n", '').replace("\t", '')

    assert txt == '<?xml version="1.0" ?><WUFIplusProject><IdentNr>1</IdentNr><X>0.0</X><Y>0.0</Y><Z>0.0</Z></WUFIplusProject>'
