import math

import pytest
from ladybug_geometry.geometry2d.pointvector import Vector2D
from ladybug_geometry.geometry3d.pointvector import Vector3D

from honeybee_ph_utils.vector3d_tools import angle_between_2D_vectors, cross_product, dot_product, magnitude, normalize


def test_cross_product() -> None:
    # Test case 1: Cross product of two orthogonal vectors
    vector_a = Vector3D(1, 0, 0)
    vector_b = Vector3D(0, 1, 0)
    result = cross_product(vector_a, vector_b)
    expected_result = Vector3D(0, 0, 1)
    assert result == expected_result

    # Test case 2: Cross product of two parallel vectors
    vector_a = Vector3D(1, 0, 0)
    vector_b = Vector3D(2, 0, 0)
    result = cross_product(vector_a, vector_b)
    expected_result = Vector3D(0, 0, 0)
    assert result == expected_result

    # Test case 3: Cross product of two arbitrary vectors
    vector_a = Vector3D(1, 2, 3)
    vector_b = Vector3D(4, 5, 6)
    result = cross_product(vector_a, vector_b)
    expected_result = Vector3D(-3, 6, -3)
    assert result == expected_result

    # Test case 4: Cross product of two negative vectors
    vector_a = Vector3D(-1, -2, -3)
    vector_b = Vector3D(-4, -5, -6)
    result = cross_product(vector_a, vector_b)
    expected_result = Vector3D(-3, 6, -3)
    assert result == expected_result

    # Test case 5: Cross product of two zero vectors
    vector_a = Vector3D(0, 0, 0)
    vector_b = Vector3D(0, 0, 0)
    result = cross_product(vector_a, vector_b)
    expected_result = Vector3D(0, 0, 0)
    assert result == expected_result


def test_dot_product() -> None:
    # Test case 1: Dot product of two orthogonal vectors
    vector_a = Vector3D(1, 0, 0)
    vector_b = Vector3D(0, 1, 0)
    result = dot_product(vector_a, vector_b)
    expected_result = 0.0
    assert result == expected_result

    # Test case 2: Dot product of two parallel vectors
    vector_a = Vector3D(1, 0, 0)
    vector_b = Vector3D(2, 0, 0)
    result = dot_product(vector_a, vector_b)
    expected_result = 2.0
    assert result == expected_result

    # Test case 3: Dot product of two arbitrary vectors
    vector_a = Vector3D(1, 2, 3)
    vector_b = Vector3D(4, 5, 6)
    result = dot_product(vector_a, vector_b)
    expected_result = 32.0
    assert result == expected_result

    # Test case 4: Dot product of two negative vectors
    vector_a = Vector3D(-1, -2, -3)
    vector_b = Vector3D(-4, -5, -6)
    result = dot_product(vector_a, vector_b)
    expected_result = 32.0
    assert result == expected_result

    # Test case 5: Dot product of two zero vectors
    vector_a = Vector3D(0, 0, 0)
    vector_b = Vector3D(0, 0, 0)
    result = dot_product(vector_a, vector_b)
    expected_result = 0.0
    assert result == expected_result


def test_magnitude() -> None:
    # Test case 1: Magnitude of a vector with positive values
    vector = Vector3D(3, 4, 5)
    result = magnitude(vector)
    expected_result = 7.0710678118654755
    assert result == expected_result

    # Test case 2: Magnitude of a vector with negative values
    vector = Vector3D(-3, -4, -5)
    result = magnitude(vector)
    expected_result = 7.0710678118654755
    assert result == expected_result

    # Test case 3: Magnitude of a vector with zero values
    vector = Vector3D(0, 0, 0)
    result = magnitude(vector)
    expected_result = 0.0
    assert result == expected_result


def test_normalize() -> None:
    # Test case 1: Normalize a vector with negative values
    vector = Vector3D(0, 2, 0)
    result = normalize(vector)
    expected_result = Vector3D(0, 1, 0)
    assert result == expected_result

    # Test case 2: Normalize a vector with zero values
    vector = Vector3D(0, 0, 0)
    result = normalize(vector)
    expected_result = Vector3D(0, 0, 0)
    assert result == expected_result

    # Test case 3: Normalize a vector with negative values
    vector = Vector3D(-1, -2, -3)
    result = normalize(vector)
    expected_result = Vector3D(-0.2672612419124244, -0.5345224838248488, -0.8017837257372732)  # type: ignore
    assert result == expected_result


# -----------------------------------------------------------------------------
# -- Test parallel vectors
def test_counterclockwise_angle_between_two_parallel_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(0))  # No Rotation
    assert angle_between_2D_vectors(v1, v2) == 0.00

    v3 = Vector2D(1, 0)
    v4 = v3.rotate(math.radians(0))  # No Rotation
    assert angle_between_2D_vectors(v3, v4) == 0.00


# -- Test positive rotation
def test_counterclockwise_angle_between_two_positive_90_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(90))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(90))


def test_counterclockwise_angle_between_two_positive_45_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(45))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(45))


def test_counterclockwise_angle_between_two_positive_180_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(180))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(180))


def test_counterclockwise_angle_between_two_positive_270_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(270))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(90))


# -- Test negative rotation
def test_counterclockwise_angle_between_two_negative_90_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(-90))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(90))


def test_counterclockwise_angle_between_two_negative_180_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(-180))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(180))


def test_counterclockwise_angle_between_two_negative_270_degree_vectors() -> None:
    v1 = Vector2D(0, 1)
    v2 = v1.rotate(math.radians(-270))  # Rotate counter-clockwise
    assert angle_between_2D_vectors(v1, v2) == pytest.approx(math.radians(90))
