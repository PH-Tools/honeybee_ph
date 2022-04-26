from PHX.to_WUFI_XML import xml_schemas
import pytest


def test_DistributionHeating_Class(reset_class_counters):
    with pytest.raises(NotImplementedError):
        result = xml_schemas.DistributionHeating()


def test_DistributionHeating_Schema(reset_class_counters):
    with pytest.raises(NotImplementedError):
        result = xml_schemas._DistributionHeating(None)
