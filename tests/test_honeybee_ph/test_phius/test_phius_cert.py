from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_ph import phius


def test_phius_cert():
    phius_cert = phius.PhiusCertification()
    assert phius_cert


def test_phius_cert_serialization_default():
    phius_cert = phius.PhiusCertification()
    d = phius_cert.to_dict()
    new_obj = phius.PhiusCertification.from_dict(d)

    assert new_obj.user_data == {}
    assert new_obj.to_dict() == d


def test_phius_cert_serialization_customized():
    phius_cert = phius.PhiusCertification()

    # -- Customize / reset the attrs
    phius_cert.certification_program = 3
    phius_cert.localization_selection_type = 2

    phius_cert.PHIUS2021_heating_demand = 446.7
    phius_cert.PHIUS2021_cooling_demand = 123.4
    phius_cert.PHIUS2021_heating_load = 12.3
    phius_cert.PHIUS2021_cooling_load = 45.6

    phius_cert.building_status.value = 2
    phius_cert.building_type.value = 3

    phius_cert.int_gains_evap_per_person = 45
    phius_cert.int_gains_flush_heat_loss = False
    phius_cert.int_gains_num_toilets = 2
    phius_cert.int_gains_toilet_room_util_pat = None
    phius_cert.int_gains_use_school_defaults = True
    phius_cert.int_gains_dhw_marginal_perf_ratio = None

    phius_cert.icfa_override = 345.67

    phius_cert.user_data["test_key"] = "test_value"

    d = phius_cert.to_dict()
    new_obj = phius.PhiusCertification.from_dict(d)

    assert "test_key" in new_obj.user_data
    assert new_obj.to_dict() == d


def test_move_phius_cert():
    phius_cert = phius.PhiusCertification()
    new_cert = phius_cert.move(Vector3D(1, 2, 3))

    assert new_cert.to_dict() == phius_cert.to_dict()


def test_rotate_phius_cert():
    phius_cert = phius.PhiusCertification()
    new_cert = phius_cert.rotate(Vector3D(0, 0, 0), 90, Point3D(0, 0, 0))

    assert new_cert.to_dict() == phius_cert.to_dict()


def test_rotate_xy_phius_cert():
    phius_cert = phius.PhiusCertification()
    new_cert = phius_cert.rotate_xy(90, Point3D(0, 0, 0))

    assert new_cert.to_dict() == phius_cert.to_dict()


def test_reflect_phius_cert():
    phius_cert = phius.PhiusCertification()
    new_cert = phius_cert.reflect(Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0)))

    assert new_cert.to_dict() == phius_cert.to_dict()


def test_scale_phius_cert():
    phius_cert = phius.PhiusCertification()
    new_cert = phius_cert.scale(2, Point3D(0, 0, 0))
    assert new_cert.to_dict() == phius_cert.to_dict()

    phius_cert.icfa_override = 100
    new_cert = phius_cert.scale(2, Point3D(0, 0, 0))

    assert new_cert.to_dict() != phius_cert.to_dict()
    assert new_cert.icfa_override == 200
