from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_ph import phi


def test_phi_cert():
    phi_cert = phi.PhiCertification()
    assert phi_cert


def test_phi_cert_serialization_default():
    phi_cert = phi.PhiCertification()
    d = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(d)

    assert new_obj.to_dict() == d


def test_phi_cert_serialization_with_user_data():
    phi_cert = phi.PhiCertification()
    phi_cert.user_data["test_key"] = "test_value"
    d = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(d)

    assert "test_key" in new_obj.user_data
    assert new_obj.to_dict() == d


def test_phi_cert_serialization_customized():
    phi_cert = phi.PhiCertification(phpp_version=9)

    phi_cert_attributes = phi_cert.attributes  # type: phi.PHPPSettings9
    phi_cert_attributes.building_category_type = "1"
    phi_cert_attributes.tfa_override = 436.89

    d = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(d)

    assert new_obj.to_dict() == d


def test_move_phi_cert():
    phi_cert = phi.PhiCertification()
    new_cert = phi_cert.move(Vector3D(1, 2, 3))

    assert new_cert.to_dict() == phi_cert.to_dict()


def test_rotate_phi_cert():
    phi_cert = phi.PhiCertification()
    new_cert = phi_cert.rotate(Vector3D(0, 0, 0), 90, Point3D(0, 0, 0))

    assert new_cert.to_dict() == phi_cert.to_dict()


def test_rotate_xy_phi_cert():
    phi_cert = phi.PhiCertification()
    new_cert = phi_cert.rotate_xy(90, Point3D(0, 0, 0))

    assert new_cert.to_dict() == phi_cert.to_dict()


def test_reflect_phi_cert():
    phi_cert = phi.PhiCertification()
    new_cert = phi_cert.reflect(Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0)))

    assert new_cert.to_dict() == phi_cert.to_dict()


def test_scale_phi_cert():
    phi_cert = phi.PhiCertification()
    new_cert = phi_cert.scale(2, Point3D(0, 0, 0))
    assert new_cert.to_dict() == phi_cert.to_dict()

    phi_cert.attributes.tfa_override = 100
    new_cert = phi_cert.scale(2, Point3D(0, 0, 0))
    assert new_cert.to_dict() != phi_cert.to_dict()
    assert new_cert.attributes.tfa_override == 200
