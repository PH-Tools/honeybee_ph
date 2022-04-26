from PHX.to_WUFI_XML import xml_writables


def test_XML_Node():
    n1 = xml_writables.XML_Node('test_1', 1)
    n2 = xml_writables.XML_Node('test_2', 2)

    assert n1 != n2
    assert n1
    assert n2
    assert not n1.attr_name
    assert not n1.attr_value

    n3 = xml_writables.XML_Node('test_3', 3, 'attr_name1', 'attr_val1')
    n4 = xml_writables.XML_Node('test_4', 4, 'attr_name2', 'attr_val2')

    assert n1 != n2 != n3 != n4
    assert n3
    assert n4


def test_XML_List():
    # --
    n1 = xml_writables.XML_Node('test_1', 1)
    n2 = xml_writables.XML_Node('test_2', 2)
    nodes_1 = [n1, n2]
    l1 = xml_writables.XML_List('list_1', nodes_1)

    assert l1.attr_value == 2  # automatic count for WUFI's 'Count' attr
    for node in l1.node_items:
        assert node in nodes_1

    # --
    n3 = xml_writables.XML_Node('test_3', 3)
    n4 = xml_writables.XML_Node('test_4', 4)
    nodes_2 = [n3, n4]
    l2 = xml_writables.XML_List('list_2', nodes_2)

    l2.attr_value = 'test_value'  # set the attr_val
    assert l2.attr_value == 'test_value'
    for node in l2.node_items:
        assert node in nodes_2

    # --
    n5 = xml_writables.XML_Node('test_5', 5)
    n6 = xml_writables.XML_Node('test_6', 6)
    nodes_3 = [n5, n6]
    l3 = xml_writables.XML_List('list_3', nodes_3, _attr_value='test_value')

    assert l3.attr_value == 'test_value'
    for node in l3.node_items:
        assert node in nodes_3
