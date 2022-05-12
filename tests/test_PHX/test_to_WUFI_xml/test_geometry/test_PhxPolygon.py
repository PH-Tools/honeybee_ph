from PHX.model import geometry
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_polygon_no_vertices(reset_class_counters):
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
    result = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]


def test_default_polygon_edit_normal_vector(reset_class_counters):
    p1 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(0.0, 0.0, 0.0),
        geometry.PhxVector(1.3, 4.5, 12),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(0, 0, 1),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    result = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>1.3</NormalVectorX>',
        '<NormalVectorY>4.5</NormalVectorY>',
        '<NormalVectorZ>12</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="0"/>',
    ]


def test_default_polygon_with_two_vertices(reset_class_counters):
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
    v1 = geometry.PhxVertix(0, 1, 1)
    v2 = geometry.PhxVertix(1, 0, 0)
    p1.add_vertix(v1)
    p1.add_vertix(v2)

    result = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="2">',
        '<IdentNr index="0">3</IdentNr>',
        '<IdentNr index="1">4</IdentNr>',
        '</IdentNrPoints>',
        '<IdentNrPolygonsInside count="0"/>'
    ]


def test_default_polygon_with_single_polygon_inside(reset_class_counters):
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
    p2 = geometry.PhxPolygon(
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
    p1.add_child_poly_id(p2.id_num)

    result = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="1">',
        '<IdentNr index="0">2</IdentNr>',
        '</IdentNrPolygonsInside>'
    ]


def test_default_polygon_with_multiple_polygon_inside(reset_class_counters):
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
    p2 = geometry.PhxPolygon(
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
    p1.add_child_poly_id(p2.id_num)
    p1.add_child_poly_id(p3.id_num)

    result = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="0"/>',
        '<IdentNrPolygonsInside count="2">',
        '<IdentNr index="0">2</IdentNr>',
        '<IdentNr index="1">3</IdentNr>',
        '</IdentNrPolygonsInside>'
    ]
