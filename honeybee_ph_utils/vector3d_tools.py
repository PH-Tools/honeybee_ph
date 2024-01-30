# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Tools for working with Ladybug.geometry3d.Vector3D objects."""

import math

try:
    from typing import Union
except ImportError:
    pass  # Python 2.7

try:
    from ladybug_geometry.geometry3d.pointvector import Vector2D, Vector3D
except ImportError as e:
    raise ImportError("Failed to import ladybug_geometry: " + str(e))


def vector_equal(vector_a, vector_b, _tolerance):
    # type: (Vector3D, Vector3D, float) -> bool
    """Return True if two Vector3Ds are equal within tolerance."""

    return all(abs(vector_a[i] - vector_b[i]) <= _tolerance for i in range(len(vector_a)))


def cross_product(vector_a, vector_b):
    # type: (Vector3D, Vector3D) -> Vector3D
    """Return the cross product of two Vector3Ds."""

    return Vector3D(
        vector_a.y * vector_b.z - vector_a.z * vector_b.y,  # type: ignore
        vector_a.z * vector_b.x - vector_a.x * vector_b.z,  # type: ignore
        vector_a.x * vector_b.y - vector_a.y * vector_b.x,  # type: ignore
    )


def dot_product(vector_a, vector_b):
    # type: (Union[Vector2D, Vector3D], Union[Vector2D, Vector3D]) -> float
    """Return the dot product of two Vector3Ds."""

    return sum(vector_a[i] * vector_b[i] for i in range(len(vector_a)))


def magnitude(vector):
    # type: (Vector3D) -> float
    """Return the magnitude of a Vector3D."""

    return sum(vector[i] ** 2 for i in range(len(vector))) ** 0.5


def normalize(vector):
    # type: (Vector3D) -> Vector3D
    """Return a normalized Vector3D."""

    mag = magnitude(vector)
    try:
        return Vector3D(*[vector[i] / mag for i in range(len(vector))])
    except ZeroDivisionError:
        return Vector3D(0, 0, 0)


def angle_between_2D_vectors(_vector1, _vector2):
    # type: (Union[Vector3D, Vector2D], Union[Vector3D, Vector2D]) -> float
    """Return the angle (in radians) between two 2D vectors."""

    # Calculate the dot product between the X-axis vectors
    cos_theta = dot_product(_vector1, _vector2)

    # Ensure cos_theta is within [-1, 1] to avoid invalid arc-cos input
    cos_theta = max(min(cos_theta, 1), -1)

    # Calculate the angle in radians
    theta_radians = math.acos(cos_theta)

    return theta_radians
