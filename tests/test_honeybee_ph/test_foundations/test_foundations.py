from honeybee_ph import foundations


def test_default_foundation_round_trip():
    f1 = foundations.PhFoundation()
    d1 = f1.to_dict()
    f2 = foundations.PhFoundation.from_dict(d1)

    assert f2.to_dict() == d1

def test_default_foundation_duplicate():
    f1 = foundations.PhFoundation()
    f2 = f1.duplicate()

    assert f2.to_dict() == f1.to_dict()

def test_default_heated_basement_round_trip():
    f1 = foundations.PhHeatedBasement()
    d1 = f1.to_dict()
    f2 = foundations.PhHeatedBasement.from_dict(d1)

    assert f2.to_dict() == d1

def test_default_heated_basement_duplicate():
    f1 = foundations.PhHeatedBasement()
    f2 = f1.duplicate()

    assert f2.to_dict() == f1.to_dict()

def test_default_unheated_basement_round_trip():
    f1 = foundations.PhUnheatedBasement()
    d1 = f1.to_dict()
    f2 = foundations.PhUnheatedBasement.from_dict(d1)

    assert f2.to_dict() == d1

def test_default_unheated_basement_duplicate():
    f1 = foundations.PhUnheatedBasement()
    f2 = f1.duplicate()

    assert f2.to_dict() == f1.to_dict()

def test_default_slab_on_grade_round_trip():
    f1 = foundations.PhSlabOnGrade()
    d1 = f1.to_dict()
    f2 = foundations.PhSlabOnGrade.from_dict(d1)

    assert f2.to_dict() == d1

def test_default_slab_on_grade_duplicate():
    f1 = foundations.PhSlabOnGrade()
    f2 = f1.duplicate()

    assert f2.to_dict() == f1.to_dict()

def test_default_crawlspace_round_trip():
    f1 = foundations.PhVentedCrawlspace()
    d1 = f1.to_dict()
    f2 = foundations.PhVentedCrawlspace.from_dict(d1)

    assert f2.to_dict() == d1

def test_default_crawlspace_duplicate():
    f1 = foundations.PhVentedCrawlspace()
    f2 = f1.duplicate()

    assert f2.to_dict() == f1.to_dict()