from PHX.to_WUFI_XML import xml_schemas
import pytest


def test_DistributionDHW_Class(reset_class_counters):
    with pytest.raises(NotImplementedError):
        result = xml_schemas.DistributionDHW()


def test_DistributionDHW_Schema(reset_class_counters):
    with pytest.raises(NotImplementedError):
        result = xml_schemas._DistributionDHW(None)
