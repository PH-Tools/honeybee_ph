# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Project Team-Member Classes."""

try:
    from typing import Dict, Any, Optional
except ImportError:
    pass  # Python 2.7


class ProjectTeamMember:
    def __init__(
        self,
        _name=None,
        _street=None,
        _city=None,
        _post_code=None,
        _telephone=None,
        _email=None,
        _license_number=None,
    ):
        # type: (Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]) -> None
        self.name = _name
        self.street = _street
        self.city = _city
        self.post_code = _post_code
        self.telephone = _telephone
        self.email = _email
        self.license_number = _license_number

    def duplicate(self):
        # type: () -> ProjectTeamMember
        new_obj = ProjectTeamMember(
            self.name,
            self.street,
            self.city,
            self.post_code,
            self.telephone,
            self.email,
            self.license_number,
        )
        return new_obj

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d["name"] = self.name
        d["street"] = self.street
        d["city"] = self.city
        d["post_code"] = self.post_code
        d["telephone"] = self.telephone
        d["email"] = self.email
        d["license_number"] = self.license_number
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> ProjectTeamMember
        new_obj = cls(
            _input_dict["name"],
            _input_dict["street"],
            _input_dict["city"],
            _input_dict["post_code"],
            _input_dict["telephone"],
            _input_dict["email"],
            _input_dict["license_number"],
        )
        return new_obj

    def __str__(self):
        return "{}(name={}, street={})".format(
            self.__class__.__name__, self.name, self.street
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class ProjectTeam:
    def __init__(self):
        # type: () -> None
        self.customer = ProjectTeamMember()
        self.building = ProjectTeamMember()
        self.owner = ProjectTeamMember()
        self.designer = ProjectTeamMember()
        self.project_date = ""
        self.owner_is_client = False
        self.year_constructed = 0
        self.image = None

    def duplicate(self):
        # type: () -> ProjectTeam
        new_obj = ProjectTeam()
        new_obj.customer = self.customer.duplicate()
        new_obj.building = self.building.duplicate()
        new_obj.owner = self.owner.duplicate()
        new_obj.designer = self.designer.duplicate()
        return new_obj

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d["customer"] = self.customer.to_dict()
        d["building"] = self.building.to_dict()
        d["owner"] = self.owner.to_dict()
        d["designer"] = self.designer.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> ProjectTeam
        new_obj = cls()
        new_obj.customer = ProjectTeamMember.from_dict(
            _input_dict.get("customer", ProjectTeamMember())
        )
        new_obj.building = ProjectTeamMember.from_dict(
            _input_dict.get("building", ProjectTeamMember())
        )
        new_obj.owner = ProjectTeamMember.from_dict(
            _input_dict.get("owner", ProjectTeamMember())
        )
        new_obj.designer = ProjectTeamMember.from_dict(
            _input_dict.get("designer", ProjectTeamMember())
        )
        return new_obj
