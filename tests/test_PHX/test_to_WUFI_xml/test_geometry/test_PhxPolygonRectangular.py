from PHX.model import geometry
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_polygon_rectangular_no_vertices(reset_class_counters):
    p1 = geometry.PhxPolygonRectangular(
        _display_name='no_name',
        area=100.0,
        center=geometry.PhxVertix(0.0, 0.0, 0.0),
        normal_vector=geometry.PhxVector(0.0, 0.0, 1.0),
        plane=geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    result = generate_WUFI_XML_from_object(p1, _header="", _schema_name="_PhxPolygon")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]


def test_multiple_default_polygon_rectangular_no_vertices(reset_class_counters):
    p1 = geometry.PhxPolygonRectangular(
        'no_name',
        100.0,
        geometry.PhxVertix(0.0, 0.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p2 = geometry.PhxPolygonRectangular(
        'no_name',
        100.0,
        geometry.PhxVertix(0.0, 0.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )

    result1 = generate_WUFI_XML_from_object(p1, _header="", _schema_name="_PhxPolygon")
    assert xml_string_to_list(result1) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]

    result2 = generate_WUFI_XML_from_object(p2, _header="", _schema_name="_PhxPolygon")
    assert xml_string_to_list(result2) == [
        '<IdentNr>2</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]


def test_polygon_then_polygon_rectangular_no_vertices(reset_class_counters):
    p1 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(0.0, 0.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p2 = geometry.PhxPolygonRectangular(
        'no_name',
        100.0,
        geometry.PhxVertix(0.0, 0.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p3 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(0.0, 0.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )

    result1 = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result1) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]

    result2 = generate_WUFI_XML_from_object(p2, _header="", _schema_name="_PhxPolygon")
    assert xml_string_to_list(result2) == [
        '<IdentNr>2</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]

    result3 = generate_WUFI_XML_from_object(p3, _header="", _schema_name="_PhxPolygon")
    assert xml_string_to_list(result3) == [
        '<IdentNr>3</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]
