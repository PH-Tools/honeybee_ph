from honeybee_ph import phi


def test_phi_cert():
    phi_cert = phi.PhiCertification()
    assert phi_cert


def test_phi_cert_serialization_default():
    phi_cert = phi.PhiCertification()
    d = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(d)

    assert new_obj.to_dict() == d


def test_phi_cert_serialization_customized():
    phi_cert = phi.PhiCertification()

    phi_cert.attributes.building_category_type = "1"

    d = phi_cert.to_dict()
    new_obj = phi.PhiCertification.from_dict(d)

    assert new_obj.to_dict() == d
