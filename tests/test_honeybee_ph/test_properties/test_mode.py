from honeybee_ph.properties.model import ModelPhProperties
from honeybee_ph.team import ProjectTeam


class FakeHost(object):
    def __init__(self, name="fake_host"):
        self.display_name = name
        self.rooms = []


def test_ModelPhProperties():
    host = FakeHost()
    model_ph_properties = ModelPhProperties(host)
    assert model_ph_properties.host == host
    assert model_ph_properties.id_num == 0
    assert model_ph_properties.team != None


def test_ModelPhProperties_duplicate():
    host = FakeHost()
    model_ph_properties = ModelPhProperties(host)
    model_ph_properties.id_num = 1
    model_ph_properties.team = ProjectTeam()
    new_model_ph_properties = model_ph_properties.duplicate(host)
    assert new_model_ph_properties.host == host
    assert new_model_ph_properties.id_num == 1
    assert new_model_ph_properties.team != None


def test_ModelPhProperties_get_bldg_segment_dicts():
    host = FakeHost()
    model_ph_properties = ModelPhProperties((host))
    assert model_ph_properties._get_bldg_segment_dicts() == []


def test_ModelPhProperties_unabridged_dict_round_trip():
    host = FakeHost()
    model_ph_properties = ModelPhProperties(host)
    model_ph_properties.id_num = 1
    model_ph_properties.team = ProjectTeam()
    d1 = model_ph_properties.to_dict(abridged=True)
    new_model_ph_properties = ModelPhProperties.from_dict(d1["ph"], host)
    assert new_model_ph_properties.host == host
    assert new_model_ph_properties.id_num == 1
    assert new_model_ph_properties.team != None


def test_ModelPhProperties_load_properties_from_dict():
    host = FakeHost()
    model_ph_properties = ModelPhProperties(host)
    model_ph_properties.id_num = 1
    model_ph_properties.team = ProjectTeam()
    d1 = model_ph_properties.to_dict(abridged=False)
    d2 = {"properties": d1}

    bldg_segments, team = ModelPhProperties.load_properties_from_dict(d2)
    assert bldg_segments == {}
    assert team != None
