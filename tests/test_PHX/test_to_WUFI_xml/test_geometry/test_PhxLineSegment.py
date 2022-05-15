import pytest
from PHX.model import geometry


def test_simple_line_length_x(reset_class_counters):
    l1 = geometry.PhxLineSegment(
        geometry.PhxVertix(0, 0, 0),
        geometry.PhxVertix(1, 0, 0)
    )
    assert l1.length == 1

    l2 = geometry.PhxLineSegment(
        geometry.PhxVertix(-45, 0, 0),
        geometry.PhxVertix(12.658, 0, 0)
    )
    assert l2.length == 57.658


def test_simple_line_length_y(reset_class_counters):
    l1 = geometry.PhxLineSegment(
        geometry.PhxVertix(0, 0, 0),
        geometry.PhxVertix(0, 1, 0)
    )
    assert l1.length == 1

    l2 = geometry.PhxLineSegment(
        geometry.PhxVertix(0, -45, 0),
        geometry.PhxVertix(0, 12.658, 0)
    )
    assert l2.length == 57.658


def test_simple_line_length_z(reset_class_counters):
    l1 = geometry.PhxLineSegment(
        geometry.PhxVertix(0, 0, 0),
        geometry.PhxVertix(0, 0, 1)
    )
    assert l1.length == 1

    l2 = geometry.PhxLineSegment(
        geometry.PhxVertix(0, 0, -45),
        geometry.PhxVertix(0, 0, 12.658)
    )
    assert l2.length == 57.658


def test_simple_line_length_xyz(reset_class_counters):
    l1 = geometry.PhxLineSegment(
        geometry.PhxVertix(0, 0, 0),
        geometry.PhxVertix(1, 1, 1)
    )
    assert l1.length - 1.73205 < 0.00001

    l2 = geometry.PhxLineSegment(
        geometry.PhxVertix(-12, 46.7, -4.3),
        geometry.PhxVertix(123, 8.4, 12.658)
    )
    assert l2.length - 141.35 < 0.001
