import pytest

from honeybee_energy_ph.hvac.ducting import PhDuctElement, PhDuctSegment


def test_duct_element_raises_exception():
    with pytest.raises(Exception):
        PhDuctElement()


def test_duct_segment_raises_exception():
    with pytest.raises(Exception):
        PhDuctSegment()
