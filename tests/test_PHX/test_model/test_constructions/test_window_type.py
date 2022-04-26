from PHX.model import constructions


def test_default_window_type(reset_class_counters):
    w1 = constructions.PhxConstuctionWindow()
    assert w1.id_num == 1
    w2 = constructions.PhxConstuctionWindow()
    assert w2.id_num == 2

    assert w1 != w2
