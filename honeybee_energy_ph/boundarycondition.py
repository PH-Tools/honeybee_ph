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
    """Boundary condition for surfaces exposed to attached PH zones.

    Extends OtherSideTemperature with Passive House zone properties
    such as zone name, type, and temperature reduction factors.

    PHPP v10 carries FIVE temperature reduction factors for each custom
    exposure zone, not one, and reads each on a different worksheet. The four
    added alongside 'temperature_reduction_factor' are optional: leave one as
    None and the heating-demand factor is used in its place, which is both the
    common case (an adjacent zone at one temperature year-round) and the
    behavior of every model written before they existed.

    Attributes:
        identifier (str): Unique text identifier.
        zone_name (str): Name of the adjacent zone.
        zone_type (str): Classification of the adjacent zone.
        zone_id_num (int): Numeric ID for the adjacent zone.
        temperature_reduction_factor (float): The heating-demand factor, and
            the fallback for the four optional factors below. Default: 1.0.
        heating_load_reduction_factor (float | None): Heating-load factor, or
            None to use the heating-demand factor. Default: None.
        cooling_demand_reduction_factor (float | None): Cooling-demand factor,
            or None to use the heating-demand factor. Default: None.
        cooling_load_reduction_factor (float | None): Cooling-load factor, or
            None to use the heating-demand factor. Default: None.
        passive_cooling_reduction_factor (float | None): Passive-cooling
            factor, or None to use the heating-demand factor. Default: None.
        adjacent_zone_temperature_c (float | None): Temperature of the adjacent
            zone (deg. C). Carried for exporters which derive the factors from
            it rather than taking them directly. Default: None.
    """

    __slots__ = (
        "identifier",
        "zone_name",
        "zone_type",
        "zone_id_num",
        "temperature_reduction_factor",
        "heating_load_reduction_factor",
        "cooling_demand_reduction_factor",
        "cooling_load_reduction_factor",
        "passive_cooling_reduction_factor",
        "adjacent_zone_temperature_c",
    )

    def __init__(
        self,
        identifier="",
        temperature=autocalculate,
        heat_transfer_coefficient=0,
        zone_name="",
        zone_type="",
        temperature_reduction_factor=1.0,
        heating_load_reduction_factor=None,
        cooling_demand_reduction_factor=None,
        cooling_load_reduction_factor=None,
        passive_cooling_reduction_factor=None,
        adjacent_zone_temperature_c=None,
    ):
        # type: (str, float | Autocalculate, float, str, str, float, float | None, float | None, float | None, float | None, float | None) -> None
        """Initialize PhAdditionalZone boundary condition."""
        super(PhAdditionalZone, self).__init__(
            temperature=temperature, heat_transfer_coefficient=heat_transfer_coefficient
        )
        self.identifier = identifier
        self.zone_id_num = 0
        self.zone_name = zone_name
        self.zone_type = zone_type
        self.temperature_reduction_factor = temperature_reduction_factor
        self.heating_load_reduction_factor = heating_load_reduction_factor
        self.cooling_demand_reduction_factor = cooling_demand_reduction_factor
        self.cooling_load_reduction_factor = cooling_load_reduction_factor
        self.passive_cooling_reduction_factor = passive_cooling_reduction_factor
        self.adjacent_zone_temperature_c = adjacent_zone_temperature_c

    # -- Resolved factors. These are what an exporter writes; they apply the
    # -- "None means heating-demand" rule once, here, instead of in each
    # -- downstream tool.

    def _resolved(self, _factor):
        # type: (float | None) -> float
        """Return the factor, or the heating-demand factor when it is not set."""
        if _factor is None:
            return self.temperature_reduction_factor
        return _factor

    @property
    def heating_demand_factor(self):
        # type: () -> float
        """The resolved heating-demand temperature reduction factor."""
        return self.temperature_reduction_factor

    @property
    def heating_load_factor(self):
        # type: () -> float
        """The resolved heating-load temperature reduction factor."""
        return self._resolved(self.heating_load_reduction_factor)

    @property
    def cooling_demand_factor(self):
        # type: () -> float
        """The resolved cooling-demand temperature reduction factor."""
        return self._resolved(self.cooling_demand_reduction_factor)

    @property
    def cooling_load_factor(self):
        # type: () -> float
        """The resolved cooling-load temperature reduction factor."""
        return self._resolved(self.cooling_load_reduction_factor)

    @property
    def passive_cooling_factor(self):
        # type: () -> float
        """The resolved passive-cooling temperature reduction factor."""
        return self._resolved(self.passive_cooling_reduction_factor)

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
                "heating_load_reduction_factor": self.heating_load_reduction_factor,
                "cooling_demand_reduction_factor": self.cooling_demand_reduction_factor,
                "cooling_load_reduction_factor": self.cooling_load_reduction_factor,
                "passive_cooling_reduction_factor": self.passive_cooling_reduction_factor,
                "adjacent_zone_temperature_c": self.adjacent_zone_temperature_c,
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
        new_bc = cls(
            identifier=data["identifier"],
            temperature=temperature,
            heat_transfer_coefficient=data["heat_transfer_coefficient"],
            zone_name=data["zone_name"],
            zone_type=data["zone_type"],
            temperature_reduction_factor=data["temperature_reduction_factor"],
            # -- Added after the class shipped, so absent from older HBJSON.
            heating_load_reduction_factor=data.get("heating_load_reduction_factor", None),
            cooling_demand_reduction_factor=data.get("cooling_demand_reduction_factor", None),
            cooling_load_reduction_factor=data.get("cooling_load_reduction_factor", None),
            passive_cooling_reduction_factor=data.get("passive_cooling_reduction_factor", None),
            adjacent_zone_temperature_c=data.get("adjacent_zone_temperature_c", None),
        )
        # -- Not a constructor argument: it is export bookkeeping assigned after
        # -- the fact. It was written by to_dict() but never read back until now.
        new_bc.zone_id_num = data.get("zone_id_num", 0)
        return new_bc

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        temperature_key = "Autocalculate" if isinstance(self.temperature, Autocalculate) else self.temperature
        return (
            temperature_key,
            self.heat_transfer_coefficient,
            self.zone_name,
            self.zone_type,
            self.temperature_reduction_factor,
            self.heating_load_reduction_factor,
            self.cooling_demand_reduction_factor,
            self.cooling_load_reduction_factor,
            self.passive_cooling_reduction_factor,
            self.adjacent_zone_temperature_c,
            self.zone_id_num,
            self.identifier,
        )

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, PhAdditionalZone) and self.__key() == other.__key()
