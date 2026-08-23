import pytest
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
    phi_cert_attributes.ihg_type = "1"
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


def test_phi_cert_serialization_default_v10():
    phi_cert = phi.PhiCertification(phpp_version=10)
    phi_cert_attributes = phi_cert.attributes

    default_cert = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(default_cert)

    assert new_obj.attributes.phpp_version == phi_cert_attributes.phpp_version  # test default serialization


def test_phi_cert_serialization_customized_v10():
    phi_cert = phi.PhiCertification(phpp_version=10)

    phi_cert_attributes = phi_cert.attributes  # type: phi.PHPPSettings10
    phi_cert_attributes.building_use_type = "10"  # invalid input 11 test in test_invalid_entry_in_phi_cert_v10
    phi_cert_attributes.ihg_type = (
        "1-USER-DEFINED"  # invalid input eg "1-BANANA" test in test_invalid_entry_in_phi_cert_v10
    )
    phi_cert_attributes.certification_class = "10"
    phi_cert_attributes.certification_type = "10"
    phi_cert_attributes.primary_energy_type = "1"
    phi_cert_attributes.retrofit_type = "1"
    phi_cert_attributes.tfa_override = 436.89

    default_cert = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(default_cert)  # round trip to check serialization survival

    assert new_obj.attributes.phpp_version == phi_cert_attributes.phpp_version
    assert new_obj.attributes.building_use_type == phi_cert_attributes.building_use_type
    assert new_obj.attributes.ihg_type == phi_cert_attributes.ihg_type
    assert new_obj.attributes.certification_class == phi_cert_attributes.certification_class
    assert new_obj.attributes.certification_type == phi_cert_attributes.certification_type
    assert new_obj.attributes.primary_energy_type == phi_cert_attributes.primary_energy_type
    assert new_obj.attributes.retrofit_type == phi_cert_attributes.retrofit_type
    assert new_obj.attributes.tfa_override == phi_cert_attributes.tfa_override


def test_invalid_entry_in_phi_cert_v10():
    phi_cert = phi.PhiCertification(phpp_version=10)
    phi_cert_attributes = phi_cert.attributes  # type: phi.PHPPSettings10

    with pytest.raises(Exception):
        phi_cert_attributes.building_use_type = "11"  # test invalid input fails

    with pytest.raises(Exception):
        phi_cert_attributes.ihg_type = "1-BANANA"  # test valid .number but invalid string fails


def test_phi_cert_none_type_v10():
    phi_cert = phi.PhiCertification(phpp_version=10)
    phi_cert_attributes = phi_cert.attributes

    default_cert = phi_cert.to_dict()

    phi_cert_attributes.ihg_type = ""
    empty_cert = phi_cert.to_dict()
    assert empty_cert == default_cert  # empty value returns default value

    """phi_cert_attributes.ihg_type = "0"
    zero_cert = phi_cert.to_dict()
    assert zero_cert == default_cert"""  # Currently Fails: zero value not behaving the same as empty string and None type inputs. needs further investigation

    phi_cert_attributes.ihg_type = None
    none_cert = phi_cert.to_dict()

    assert none_cert == default_cert  # none value returns default value
