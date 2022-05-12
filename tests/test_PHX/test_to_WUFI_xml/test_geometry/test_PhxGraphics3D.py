from PHX.model import geometry
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxGraphics3D(reset_class_counters):
    g1 = geometry.PhxGraphics3D()
    result = generate_WUFI_XML_from_object(g1, _header="")
    assert xml_string_to_list(result) == [
        '<Vertices count="0"/>',
        '<Polygons count="0"/>'
    ]


def test_PhxGraphics3D_with_single_polygon(reset_class_counters):
    g1 = geometry.PhxGraphics3D()

    v1 = geometry.PhxVertix(0, 0, 0)
    v2 = geometry.PhxVertix(1, 2, 3)
    v3 = geometry.PhxVertix(0.5, 0.25, 0.333)

    p1 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(1.0, 1.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(1, 1, 0),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p1.add_vertix(v1)
    p1.add_vertix(v2)
    p1.add_vertix(v3)

    g1.add_polygons(p1)

    result = generate_WUFI_XML_from_object(g1, _header="")
    assert xml_string_to_list(result) == [
        '<Vertices count="3">',
        '<Vertix index="0">',
        '<IdentNr>1</IdentNr>',
        '<X>0</X>',
        '<Y>0</Y>',
        '<Z>0</Z>',
        '</Vertix>',
        '<Vertix index="1">',
        '<IdentNr>2</IdentNr>',
        '<X>1</X>',
        '<Y>2</Y>',
        '<Z>3</Z>',
        '</Vertix>',
        '<Vertix index="2">',
        '<IdentNr>3</IdentNr>',
        '<X>0.5</X>',
        '<Y>0.25</Y>',
        '<Z>0.333</Z>',
        '</Vertix>',
        '</Vertices>',
        '<Polygons count="1">',
        '<Polygon index="0">',
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="3">',
        '<IdentNr index="0">1</IdentNr>',
        '<IdentNr index="1">2</IdentNr>',
        '<IdentNr index="2">3</IdentNr>',
        '</IdentNrPoints>',
        '<IdentNrPolygonsInside count="0"/>',
        '</Polygon>',
        '</Polygons>']


def test_PhxGraphics3D_with_multiple_polygon(reset_class_counters):
    g1 = geometry.PhxGraphics3D()

    v1 = geometry.PhxVertix(0, 0, 0)
    v2 = geometry.PhxVertix(1, 2, 3)
    v3 = geometry.PhxVertix(0.5, 0.25, 0.333)
    v4 = geometry.PhxVertix(0, 0, 0)

    p1 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(1.0, 1.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(1, 1, 0),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p2 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(1.0, 1.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(1, 1, 0),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p3 = geometry.PhxPolygon(
        'no_name',
        100.0,
        geometry.PhxVertix(1.0, 1.0, 0.0),
        geometry.PhxVector(0.0, 0.0, 1.0),
        geometry.PhxPlane(
            geometry.PhxVector(0, 0, 1),
            geometry.PhxVertix(1, 1, 0),
            geometry.PhxVector(1, 0, 0),
            geometry.PhxVector(0, 1, 0)
        ),
    )
    p1.add_vertix(v1)
    p2.add_vertix(v2)
    p3.add_vertix(v3)
    p3.add_vertix(v4)

    g1.add_polygons([p1, p2, p3])

    result = generate_WUFI_XML_from_object(g1, _header="")
    assert xml_string_to_list(result) == [
        '<Vertices count="4">',
        '<Vertix index="0">',
        '<IdentNr>1</IdentNr>',
        '<X>0</X>',
        '<Y>0</Y>',
        '<Z>0</Z>',
        '</Vertix>',
        '<Vertix index="1">',
        '<IdentNr>2</IdentNr>',
        '<X>1</X>',
        '<Y>2</Y>',
        '<Z>3</Z>',
        '</Vertix>',
        '<Vertix index="2">',
        '<IdentNr>3</IdentNr>',
        '<X>0.5</X>',
        '<Y>0.25</Y>',
        '<Z>0.333</Z>',
        '</Vertix>',
        '<Vertix index="3">',
        '<IdentNr>4</IdentNr>',
        '<X>0</X>',
        '<Y>0</Y>',
        '<Z>0</Z>',
        '</Vertix>',
        '</Vertices>',
        '<Polygons count="3">',
        '<Polygon index="0">',
        '<IdentNr>1</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="1">',
        '<IdentNr index="0">1</IdentNr>',
        '</IdentNrPoints>',
        '<IdentNrPolygonsInside count="0"/>',
        '</Polygon>',
        '<Polygon index="1">',
        '<IdentNr>2</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="1">',
        '<IdentNr index="0">2</IdentNr>',
        '</IdentNrPoints>',
        '<IdentNrPolygonsInside count="0"/>',
        '</Polygon>',
        '<Polygon index="2">',
        '<IdentNr>3</IdentNr>',
        '<NormalVectorX>0.0</NormalVectorX>',
        '<NormalVectorY>0.0</NormalVectorY>',
        '<NormalVectorZ>1.0</NormalVectorZ>',
        '<IdentNrPoints count="2">',
        '<IdentNr index="0">3</IdentNr>',
        '<IdentNr index="1">4</IdentNr>',
        '</IdentNrPoints>',
        '<IdentNrPolygonsInside count="0"/>',
        '</Polygon>',
        '</Polygons>']
