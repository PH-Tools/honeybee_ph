import pytest
from honeybee_ph import foundations

def test_factory_error():
    f1 = foundations.PhFoundation()
    d1 = f1.to_dict()
    d1["foundation_type_value"] = "12-Not Allowed Type"

    factory = foundations.PhFoundationFactory()
    with pytest.raises(Exception):
        f2 = factory.from_dict(d1)

def test_factory_default():
    f1 = foundations.PhFoundation()
    d1 = f1.to_dict()

    factory = foundations.PhFoundationFactory()
    f2 = factory.from_dict(d1)

    assert f2.to_dict() == d1

def test_factory_heated_basement():
    f1 = foundations.PhHeatedBasement()
    d1 = f1.to_dict()

    factory = foundations.PhFoundationFactory()
    f2 = factory.from_dict(d1)

    assert f2.to_dict() == d1

def test_factory_unheated_basement():
    f1 = foundations.PhUnheatedBasement()
    d1 = f1.to_dict()

    factory = foundations.PhFoundationFactory()
    f2 = factory.from_dict(d1)

    assert f2.to_dict() == d1

def test_factory_slab_on_grade_basement():
    f1 = foundations.PhSlabOnGrade()
    d1 = f1.to_dict()

    factory = foundations.PhFoundationFactory()
    f2 = factory.from_dict(d1)

    assert f2.to_dict() == d1

def test_factory_crawlspace_basement():
    f1 = foundations.PhVentedCrawlspace()
    d1 = f1.to_dict()

    factory = foundations.PhFoundationFactory()
    f2 = factory.from_dict(d1)

    assert f2.to_dict() == d1