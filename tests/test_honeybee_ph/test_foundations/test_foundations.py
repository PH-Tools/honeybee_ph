from honeybee_ph import foundations


def test_default_foundation_round_trip():
    f1 = foundations.PhFoundation()
    f1.user_data["test_key"] = "test_value"
    d1 = f1.to_dict()
    f2 = foundations.PhFoundation.from_dict(d1)

    assert "test_key" in f2.user_data
    assert f2.to_dict() == d1


def test_default_foundation_duplicate():
    f1 = foundations.PhFoundation()
    f1.user_data["test_key"] = "test_value"
    f2 = f1.duplicate()

    assert "test_key" in f2.user_data
    assert f2.to_dict() == f1.to_dict()


def test_default_heated_basement_round_trip():
    f1 = foundations.PhHeatedBasement()
    f1.user_data["test_key"] = "test_value"
    d1 = f1.to_dict()
    f2 = foundations.PhHeatedBasement.from_dict(d1)

    assert "test_key" in f2.user_data
    assert f2.to_dict() == d1


def test_default_heated_basement_duplicate():
    f1 = foundations.PhHeatedBasement()
    f1.user_data["test_key"] = "test_value"
    f2 = f1.duplicate()

    assert "test_key" in f2.user_data
    assert f2.to_dict() == f1.to_dict()


def test_default_unheated_basement_round_trip():
    f1 = foundations.PhUnheatedBasement()
    f1.user_data["test_key"] = "test_value"
    d1 = f1.to_dict()
    f2 = foundations.PhUnheatedBasement.from_dict(d1)

    assert "test_key" in f2.user_data
    assert f2.to_dict() == d1


def test_default_unheated_basement_duplicate():
    f1 = foundations.PhUnheatedBasement()
    f1.user_data["test_key"] = "test_value"
    f2 = f1.duplicate()

    assert "test_key" in f2.user_data
    assert f2.to_dict() == f1.to_dict()


def test_default_slab_on_grade_round_trip():
    f1 = foundations.PhSlabOnGrade()
    f1.user_data["test_key"] = "test_value"
    d1 = f1.to_dict()
    f2 = foundations.PhSlabOnGrade.from_dict(d1)

    assert "test_key" in f2.user_data
    assert f2.to_dict() == d1


def test_default_slab_on_grade_duplicate():
    f1 = foundations.PhSlabOnGrade()
    f1.user_data["test_key"] = "test_value"
    f2 = f1.duplicate()

    assert "test_key" in f2.user_data
    assert f2.to_dict() == f1.to_dict()


def test_default_crawlspace_round_trip():
    f1 = foundations.PhVentedCrawlspace()
    f1.user_data["test_key"] = "test_value"
    d1 = f1.to_dict()
    f2 = foundations.PhVentedCrawlspace.from_dict(d1)

    assert "test_key" in f2.user_data
    assert f2.to_dict() == d1


def test_default_crawlspace_duplicate():
    f1 = foundations.PhVentedCrawlspace()
    f1.user_data["test_key"] = "test_value"
    f2 = f1.duplicate()

    assert "test_key" in f2.user_data
    assert f2.to_dict() == f1.to_dict()


# -----------------------------------------------------------------------------
# -- PHPP 10 'Ground' inputs (Issue #111)


def test_interior_wall_to_heated_is_only_on_the_three_types_phpp_uses():
    """PHPP has no AwI cell for a heated basement: it is inside the envelope."""
    for foundation in (
        foundations.PhSlabOnGrade(),
        foundations.PhUnheatedBasement(),
        foundations.PhVentedCrawlspace(),
    ):
        assert foundation.interior_wall_to_heated_area_m2 == 0.0
        assert foundation.interior_wall_to_heated_u_value == 0.0

    assert not hasattr(foundations.PhHeatedBasement(), "interior_wall_to_heated_area_m2")
    assert not hasattr(foundations.PhHeatedBasement(), "interior_wall_to_heated_u_value")


def test_crawlspace_wind_inputs_default_to_the_phpp_values():
    f1 = foundations.PhVentedCrawlspace()

    assert f1.wind_velocity_at_10m_m_s == 4.0
    assert f1.wind_shield_factor == 0.05


def test_slab_perimeter_insulation_defaults_to_none():
    """PHPP ships Ground!H25:H27 blank; a slab must not export insulation nobody authored."""
    f1 = foundations.PhSlabOnGrade()

    assert f1.perim_insulation_width_or_depth_m == 0.0
    assert f1.perim_insulation_thickness_m == 0.0
    assert f1.perim_insulation_conductivity == 0.0


def test_crawlspace_exposed_perimeter_defaults_to_zero():
    assert foundations.PhVentedCrawlspace().crawlspace_floor_exposed_perimeter_m == 0.0


def test_phpp_10_inputs_survive_a_round_trip_and_duplicate():
    f1 = foundations.PhVentedCrawlspace()
    f1.interior_wall_to_heated_area_m2 = 12.5
    f1.interior_wall_to_heated_u_value = 0.35
    f1.wind_velocity_at_10m_m_s = 6.0
    f1.wind_shield_factor = 0.10

    f2 = foundations.PhVentedCrawlspace.from_dict(f1.to_dict())
    f3 = f1.duplicate()

    for restored in (f2, f3):
        assert restored.interior_wall_to_heated_area_m2 == 12.5
        assert restored.interior_wall_to_heated_u_value == 0.35
        assert restored.wind_velocity_at_10m_m_s == 6.0
        assert restored.wind_shield_factor == 0.10
        assert restored.to_dict() == f1.to_dict()


def test_slab_and_unheated_basement_interior_wall_round_trip():
    for cls in (foundations.PhSlabOnGrade, foundations.PhUnheatedBasement):
        f1 = cls()
        f1.interior_wall_to_heated_area_m2 = 8.0
        f1.interior_wall_to_heated_u_value = 0.25

        f2 = cls.from_dict(f1.to_dict())

        assert f2.interior_wall_to_heated_area_m2 == 8.0
        assert f2.interior_wall_to_heated_u_value == 0.25
        assert f2.to_dict() == f1.to_dict()


def test_hbjson_written_before_issue_111_still_loads():
    """Old files carry none of the new keys; each must fall back to its default."""
    legacy_keys = (
        "interior_wall_to_heated_area_m2",
        "interior_wall_to_heated_u_value",
        "wind_velocity_at_10m_m_s",
        "wind_shield_factor",
    )

    for cls in (
        foundations.PhSlabOnGrade,
        foundations.PhUnheatedBasement,
        foundations.PhVentedCrawlspace,
    ):
        d = cls().to_dict()
        for key in legacy_keys:
            d.pop(key, None)

        restored = foundations.PhFoundationFactory.from_dict(d)

        assert restored.interior_wall_to_heated_area_m2 == 0.0
        assert restored.interior_wall_to_heated_u_value == 0.0

    crawlspace_dict = foundations.PhVentedCrawlspace().to_dict()
    for key in legacy_keys:
        crawlspace_dict.pop(key, None)
    restored_crawlspace = foundations.PhFoundationFactory.from_dict(crawlspace_dict)

    assert restored_crawlspace.wind_velocity_at_10m_m_s == 4.0
    assert restored_crawlspace.wind_shield_factor == 0.05
