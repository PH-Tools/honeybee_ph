from PHX.model import constructions
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxConstructionWindow(reset_class_counters):
    w1 = constructions.PhxConstructionWindow()
    result = generate_WUFI_XML_from_object(w1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<Name></Name>',
        '<Uw_Detailed>>true</Uw_Detailed>>',
        '<GlazingFrameDetailed>true</GlazingFrameDetailed>',
        '<FrameFactor>0.75</FrameFactor>',
        '<U_Value>1.0</U_Value>',
        '<U_Value_Glazing>1.0</U_Value_Glazing>',
        '<MeanEmissivity>0.1</MeanEmissivity>',
        '<g_Value>0.4</g_Value>',
        '<SHGC_Hemispherical>0.4</SHGC_Hemispherical>',
        '<U_Value_Frame>1.0</U_Value_Frame>',
        '<Frame_Width_Left>0.1</Frame_Width_Left>',
        '<Frame_Psi_Left>0.0</Frame_Psi_Left>',
        '<Frame_U_Left>1.0</Frame_U_Left>',
        '<Glazing_Psi_Left>0.0</Glazing_Psi_Left>',
        '<Frame_Width_Right>0.1</Frame_Width_Right>',
        '<Frame_Psi_Right>0.0</Frame_Psi_Right>',
        '<Frame_U_Right>1.0</Frame_U_Right>',
        '<Glazing_Psi_Right>0.0</Glazing_Psi_Right>',
        '<Frame_Width_Top>0.1</Frame_Width_Top>',
        '<Frame_Psi_Top>0.0</Frame_Psi_Top>',
        '<Frame_U_Top>1.0</Frame_U_Top>',
        '<Glazing_Psi_Top>0.0</Glazing_Psi_Top>',
        '<Frame_Width_Bottom>0.1</Frame_Width_Bottom>',
        '<Frame_Psi_Bottom>0.0</Frame_Psi_Bottom>',
        '<Frame_U_Bottom>1.0</Frame_U_Bottom>',
        '<Glazing_Psi_Bottom>0.0</Glazing_Psi_Bottom>'
    ]
