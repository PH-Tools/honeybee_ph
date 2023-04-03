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

    phi_cert_attributes = phi_cert.attributes # type: phi.PHPPSettings9
    phi_cert_attributes.building_category_type = "1"

    d = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(d)

    assert new_obj.to_dict() == d
