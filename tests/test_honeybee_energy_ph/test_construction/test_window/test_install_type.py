from uuid import uuid4

from honeybee_energy_ph.construction import window


def test_default_PhApertureInstallType():
    install_type = window.PhApertureInstallType(str(uuid4()))
    assert install_type.psi_install == 0.0
    assert install_type.source == ""
    assert install_type


def test_PhApertureInstallType_display_name():
    install_type = window.PhApertureInstallType(str(uuid4()))
    install_type.display_name = "Phius mid-wall"
    assert install_type.display_name == "Phius mid-wall"
    assert "Phius mid-wall" in str(install_type)
    assert repr(install_type) == str(install_type)
    assert install_type.ToString() == str(install_type)


def test_PhApertureInstallType_to_from_dict_roundtrip():
    install_type = window.PhApertureInstallType(str(uuid4()))
    install_type.display_name = "Buried Jamb"
    install_type.psi_install = 0.052
    install_type.source = "Phius 1.4.4.6"
    install_type.user_data["test_key"] = "test_value"

    d = install_type.to_dict()
    new_install_type = window.PhApertureInstallType.from_dict(d)

    assert new_install_type is not install_type
    assert new_install_type.to_dict() == d
    assert new_install_type.identifier == install_type.identifier
    assert new_install_type.display_name == "Buried Jamb"
    assert new_install_type.psi_install == 0.052
    assert new_install_type.source == "Phius 1.4.4.6"
    assert "test_key" in new_install_type.user_data


def test_PhApertureInstallType_from_legacy_dict_without_new_keys():
    """A dict missing the psi_install / source keys should fall back to defaults."""
    install_type = window.PhApertureInstallType(str(uuid4()))
    d = install_type.to_dict()
    del d["psi_install"]
    del d["source"]

    new_install_type = window.PhApertureInstallType.from_dict(d)
    assert new_install_type.psi_install == 0.0
    assert new_install_type.source == ""


def test_duplicate_PhApertureInstallType():
    install_type = window.PhApertureInstallType(str(uuid4()))
    install_type.display_name = "Party Wall"
    install_type.psi_install = 0.0
    install_type.source = "no install psi at party wall"
    install_type.user_data["test_key"] = "test_value"

    new_install_type = install_type.duplicate()

    assert new_install_type is not install_type
    assert new_install_type.identifier == install_type.identifier
    assert new_install_type.display_name == "Party Wall"
    assert new_install_type.psi_install == 0.0
    assert new_install_type.source == "no install psi at party wall"
    assert "test_key" in new_install_type.user_data
    assert new_install_type.user_data is not install_type.user_data
