from pathlib import Path
import pytest
from PHX.from_HBJSON import read_HBJSON_file


def test_read_default_single_zone_model():
    file_path = Path('tests', '_source_hbjson', 'Default_Model_Single_Zone.hbjson')
    d = read_HBJSON_file.read_hb_json_from_file(file_path)
    assert d


def test_read_default_single_zone_room():
    file_path = Path('tests', '_source_hbjson', 'Default_Room_Single_Zone.json')
    with pytest.raises(read_HBJSON_file.HBJSONModelReadError):
        read_HBJSON_file.read_hb_json_from_file(file_path)


def test_read_not_a_real_file():
    file_path = Path('tests', '_source_hbjson', 'This_file_does_not_exist.hbjson')
    with pytest.raises(FileNotFoundError):
        read_HBJSON_file.read_hb_json_from_file(file_path)
