from honeybee_ph.team import ProjectTeam, ProjectTeamMember


def test_ProjectTeamMember():
    team_member = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    assert team_member.name == "John Doe"
    assert team_member.street == "123 Main St."
    assert team_member.city == "Anytown"
    assert team_member.post_code == "12345"
    assert team_member.telephone == "555-555-5555"
    assert team_member.email == ""
    assert team_member.license_number == ""


def test_ProjectTeam_customer():
    team = ProjectTeam()
    team.customer = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    assert team.customer.name == "John Doe"
    assert team.customer.street == "123 Main St."
    assert team.customer.city == "Anytown"
    assert team.customer.post_code == "12345"
    assert team.customer.telephone == "555-555-5555"
    assert team.customer.email == ""
    assert team.customer.license_number == ""


def test_ProjectTeam_owner():
    team = ProjectTeam()
    team.owner = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    assert team.owner.name == "John Doe"
    assert team.owner.street == "123 Main St."
    assert team.owner.city == "Anytown"
    assert team.owner.post_code == "12345"
    assert team.owner.telephone == "555-555-5555"
    assert team.owner.email == ""
    assert team.owner.license_number == ""


def test_ProjectTeam_building():
    team = ProjectTeam()
    team.building = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    assert team.building.name == "John Doe"
    assert team.building.street == "123 Main St."
    assert team.building.city == "Anytown"
    assert team.building.post_code == "12345"
    assert team.building.telephone == "555-555-5555"
    assert team.building.email == ""
    assert team.building.license_number == ""


def test_ProjectTeam_designer():
    team = ProjectTeam()
    team.designer = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    assert team.designer.name == "John Doe"
    assert team.designer.street == "123 Main St."
    assert team.designer.city == "Anytown"
    assert team.designer.post_code == "12345"
    assert team.designer.telephone == "555-555-5555"
    assert team.designer.email == ""
    assert team.designer.license_number == ""


def test_ProjectTeam_duplicate():
    team = ProjectTeam()
    team.customer = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team.owner = ProjectTeamMember(
        "Jane Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team.building = ProjectTeamMember(
        "Joe Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team.designer = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team_dup = team.duplicate()
    assert team_dup.customer.name == "John Doe"
    assert team_dup.customer.street == "123 Main St."
    assert team_dup.customer.city == "Anytown"
    assert team_dup.customer.post_code == "12345"
    assert team_dup.customer.telephone == "555-555-5555"
    assert team_dup.customer.email == ""
    assert team_dup.customer.license_number == ""
    assert team_dup.owner.name == "Jane Doe"
    assert team_dup.owner.street == "123 Main St."
    assert team_dup.owner.city == "Anytown"
    assert team_dup.owner.post_code == "12345"
    assert team_dup.owner.telephone == "555-555-5555"
    assert team_dup.owner.email == ""
    assert team_dup.owner.license_number == ""
    assert team_dup.building.name == "Joe Doe"
    assert team_dup.building.street == "123 Main St."
    assert team_dup.building.city == "Anytown"
    assert team_dup.building.post_code == "12345"
    assert team_dup.building.telephone == "555-555-5555"
    assert team_dup.building.email == ""
    assert team_dup.building.license_number == ""
    assert team.designer.name == "John Doe"
    assert team.designer.street == "123 Main St."
    assert team.designer.city == "Anytown"
    assert team.designer.post_code == "12345"
    assert team.designer.telephone == "555-555-5555"
    assert team.designer.email == ""
    assert team.designer.license_number == ""


def test_ProjectTeamMember_to_from_dict():
    team = ProjectTeam()
    team.customer = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team.owner = ProjectTeamMember(
        "Jane Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team.building = ProjectTeamMember(
        "Joe Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )
    team.designer = ProjectTeamMember(
        "John Doe", "123 Main St.", "Anytown", "12345", "555-555-5555", ""
    )

    team_dict = team.to_dict()
    team_dup = ProjectTeam.from_dict(team_dict)
    assert team_dup.to_dict() == team_dict
