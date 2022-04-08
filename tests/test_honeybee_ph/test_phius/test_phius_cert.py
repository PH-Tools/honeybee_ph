import honeybee_ph.phius


def test_phius_cert():
    phius_cert = honeybee_ph.phius.PhiusCertification()
    assert phius_cert


def test_phius_cert_serialiation_default():
    phius_cert = honeybee_ph.phius.PhiusCertification()
    d = phius_cert.to_dict()
    new_obj = honeybee_ph.phius.PhiusCertification.from_dict(d)

    assert new_obj.to_dict() == d


def test_phius_cert_serialiation_customized():
    phius_cert = honeybee_ph.phius.PhiusCertification()

    # -- Customize / reset the attrs
    phius_cert.certification_criteria = 3
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

    d = phius_cert.to_dict()
    new_obj = honeybee_ph.phius.PhiusCertification.from_dict(d)

    assert new_obj.to_dict() == d
