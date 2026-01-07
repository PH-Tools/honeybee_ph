"""Extra Boundary Condition objects for Passive House models.

Note to developers:
    See _extend_honeybee_energy_ph to see where these boundary conditions are added to
    honeybee.boundarycondition module.
"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython2.7

try:
    from honeybee.altnumber import Autocalculate, autocalculate
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_energy.boundarycondition import OtherSideTemperature
except ImportError as e:
    raise ImportError("\nFailed to import honeybee-energy:\n\t{}".format(e))


class PhAdditionalZone(OtherSideTemperature):
    """For surfaces exposed to attached zones with different temperature settings.

    This class extends the basic honeybee-energy OtherSideTemperature boundary condition
    by adding properties specific to Passive House modeling, such as zone-name, zone-type,
    and temperature-reduction-factor.
    """

    __slots__ = ("identifier", "zone_name", "zone_type", "zone_id_num", "temperature_reduction_factor")

    def __init__(
        self,
        identifier="",
        temperature=autocalculate,
        heat_transfer_coefficient=0,
        zone_name="",
        zone_type="",
        temperature_reduction_factor=1.0,
    ):
        # type: (str, float | Autocalculate, float, str, str, float) -> None
        """Initialize PhAdditionalZone boundary condition."""
        super(PhAdditionalZone, self).__init__(
            temperature=temperature, heat_transfer_coefficient=heat_transfer_coefficient
        )
        self.identifier = identifier
        self.zone_id_num = 0
        self.zone_name = zone_name
        self.zone_type = zone_type
        self.temperature_reduction_factor = temperature_reduction_factor

    def to_dict(self):
        # type: () -> dict
        parent_dict = super(PhAdditionalZone, self).to_dict()  # type: dict[str, Any]
        parent_dict.update(
            {
                "identifier": self.identifier,
                "zone_name": self.zone_name,
                "zone_type": self.zone_type,
                "zone_id_num": self.zone_id_num,
                "temperature_reduction_factor": self.temperature_reduction_factor,
            }
        )
        return parent_dict

    @classmethod
    def from_dict(cls, data):
        # type: (dict) -> PhAdditionalZone
        """Initialize PhAdditionalZone BoundaryCondition from a dictionary.

        Args:
            data: A dictionary representation of the boundary condition.
        """
        assert (
            data["type"] == "PhAdditionalZone"
        ), "Expected dictionary for PhAdditionalZone " "boundary condition. Got {}.".format(data["type"])
        temperature = (
            autocalculate
            if "temperature" not in data or data["temperature"] == autocalculate.to_dict()
            else data["temperature"]
        )
        return cls(
            identifier=data["identifier"],
            temperature=temperature,
            heat_transfer_coefficient=data["heat_transfer_coefficient"],
            zone_name=data["zone_name"],
            zone_type=data["zone_type"],
            temperature_reduction_factor=data["temperature_reduction_factor"],
        )

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        temperature_key = "Autocalculate" if isinstance(self.temperature, Autocalculate) else self.temperature
        return (
            temperature_key,
            self.heat_transfer_coefficient,
            self.zone_name,
            self.zone_type,
            self.temperature_reduction_factor,
            self.zone_id_num,
            self.identifier,
        )

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, PhAdditionalZone) and self.__key() == other.__key()
