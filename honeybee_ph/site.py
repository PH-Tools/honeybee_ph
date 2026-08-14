# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive-House Style Monthly Climate Data"""

import math
from copy import copy, deepcopy
from numbers import Real

try:
    from itertools import izip as zip  # type: ignore
except ImportError:
    pass  # Python3

try:
    from typing import Any, Collection, Dict, List, Optional, Union
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import _base


def _finite_value_issue(field_name, value):
    # type: (str, Any) -> Optional[str]
    if not _is_finite_real(value):
        return "{}: expected a finite numeric value; got {!r}.".format(field_name, value)
    return None


def _is_finite_real(value):
    # type: (Any) -> bool
    return not isinstance(value, bool) and isinstance(value, Real) and not math.isnan(value) and not math.isinf(value)


class Climate_MonthlyValueSet(_base._Base):
    """A set of 12 monthly climate values (temperature, radiation, etc.).

    Stores one value per calendar month. Used as a building block for
    temperature, radiation, and other monthly climate data collections.

    Attributes:
        january (float): January value.
        february (float): February value.
        march (float): March value.
        april (float): April value.
        may (float): May value.
        june (float): June value.
        july (float): July value.
        august (float): August value.
        september (float): September value.
        october (float): October value.
        november (float): November value.
        december (float): December value.
    """

    january = 0.0
    february = 0.0
    march = 0.0
    april = 0.0
    may = 0.0
    june = 0.0
    july = 0.0
    august = 0.0
    september = 0.0
    october = 0.0
    november = 0.0
    december = 0.0
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    def __init__(self, _values=None):
        # type: (Optional[Collection[float]]) -> None
        super(Climate_MonthlyValueSet, self).__init__()
        if _values is None:
            _values = [0.0] * 12
        self.values = _values

    @property
    def values(self):
        # type: () -> List[float]
        return [getattr(self, month) for month in self.months]

    @values.setter
    def values(self, _in):
        # type: (Collection[float]) -> None
        if (_in is None) or (len(_in) != 12):
            msg = "Error: Monthly data should be a collection of 12 numeric items.\n" "Got a {} of length: {}?".format(
                type(_in), len(_in)
            )
            raise Exception(msg)

        for val, month_name in zip(_in, self.months):
            setattr(self, month_name, val)

    def __copy__(self):
        # type: () -> Climate_MonthlyValueSet
        obj = Climate_MonthlyValueSet(self.values)
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Climate_MonthlyValueSet
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, float]
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        for month in self.months:
            d[month] = getattr(self, month)

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, float]) -> Climate_MonthlyValueSet
        obj = cls()
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        for month in cls.months:
            setattr(obj, month, _input_dict.get(month))

        return obj


class Climate_MonthlyTempCollection(_base._Base):
    """Collection of monthly temperature data sets.

    Default construction creates four independent monthly value sets. Explicitly
    supplied value sets are retained by identity.

    Attributes:
        air_temps (Climate_MonthlyValueSet): Monthly air temperatures in degrees C.
        dewpoints (Climate_MonthlyValueSet): Monthly dewpoint temperatures in degrees C.
        sky_temps (Climate_MonthlyValueSet): Monthly sky temperatures in degrees C.
        ground_temps (Climate_MonthlyValueSet): Monthly ground temperatures in degrees C.
    """

    def __init__(
        self,
        _air=None,
        _dewpoint=None,
        _sky=None,
        _ground=None,
    ):
        # type: (Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet]) -> None
        super(Climate_MonthlyTempCollection, self).__init__()
        self.air_temps = _air if _air is not None else Climate_MonthlyValueSet()
        self.dewpoints = _dewpoint if _dewpoint is not None else Climate_MonthlyValueSet()
        self.sky_temps = _sky if _sky is not None else Climate_MonthlyValueSet()
        self.ground_temps = _ground if _ground is not None else Climate_MonthlyValueSet()

    def __copy__(self):
        # type: () -> Climate_MonthlyTempCollection
        obj = Climate_MonthlyTempCollection(
            self.air_temps.duplicate(),
            self.dewpoints.duplicate(),
            self.sky_temps.duplicate(),
            self.ground_temps.duplicate(),
        )
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Climate_MonthlyTempCollection
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Dict[str, float]]
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["air_temps"] = self.air_temps.to_dict()
        d["dewpoints"] = self.dewpoints.to_dict()
        d["sky_temps"] = self.sky_temps.to_dict()
        d["ground_temps"] = self.ground_temps.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Dict[str, float]]) -> Climate_MonthlyTempCollection
        obj = cls(
            _air=Climate_MonthlyValueSet.from_dict(_input_dict["air_temps"]),
            _dewpoint=Climate_MonthlyValueSet.from_dict(_input_dict["dewpoints"]),
            _sky=Climate_MonthlyValueSet.from_dict(_input_dict["sky_temps"]),
            _ground=Climate_MonthlyValueSet.from_dict(_input_dict["ground_temps"]),
        )
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        return obj


class Climate_MonthlyRadiationCollection(_base._Base):
    """Collection of monthly solar radiation data by orientation.

    Default construction creates five independent monthly value sets. Explicitly
    supplied value sets are retained by identity.

    Attributes:
        north (Climate_MonthlyValueSet): Monthly north-facing radiation in kWh/m2.
        east (Climate_MonthlyValueSet): Monthly east-facing radiation in kWh/m2.
        south (Climate_MonthlyValueSet): Monthly south-facing radiation in kWh/m2.
        west (Climate_MonthlyValueSet): Monthly west-facing radiation in kWh/m2.
        glob (Climate_MonthlyValueSet): Monthly global horizontal radiation in kWh/m2.
    """

    def __init__(
        self,
        _north=None,
        _east=None,
        _south=None,
        _west=None,
        _glob=None,
    ):
        # type: (Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet], Optional[Climate_MonthlyValueSet]) -> None
        super(Climate_MonthlyRadiationCollection, self).__init__()
        self.north = _north if _north is not None else Climate_MonthlyValueSet()
        self.east = _east if _east is not None else Climate_MonthlyValueSet()
        self.south = _south if _south is not None else Climate_MonthlyValueSet()
        self.west = _west if _west is not None else Climate_MonthlyValueSet()
        self.glob = _glob if _glob is not None else Climate_MonthlyValueSet()

    def __copy__(self):
        # type: () -> Climate_MonthlyRadiationCollection
        obj = Climate_MonthlyRadiationCollection(
            self.north.duplicate(),
            self.east.duplicate(),
            self.south.duplicate(),
            self.west.duplicate(),
            self.glob.duplicate(),
        )
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Climate_MonthlyRadiationCollection
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Dict[str, float]]
        d = {}
        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["north"] = self.north.to_dict()
        d["east"] = self.east.to_dict()
        d["south"] = self.south.to_dict()
        d["west"] = self.west.to_dict()
        d["glob"] = self.glob.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Dict[str, float]]) -> Climate_MonthlyRadiationCollection
        obj = cls(
            _north=Climate_MonthlyValueSet.from_dict(_input_dict["north"]),
            _east=Climate_MonthlyValueSet.from_dict(_input_dict["east"]),
            _south=Climate_MonthlyValueSet.from_dict(_input_dict["south"]),
            _west=Climate_MonthlyValueSet.from_dict(_input_dict["west"]),
            _glob=Climate_MonthlyValueSet.from_dict(_input_dict["glob"]),
        )
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        return obj


class Climate_PeakLoadValueSet(_base._Base):
    """A set of peak load climate data for a single design condition.

    Attributes:
        temp (float): Design temperature in degrees C.
        rad_north (float): North-facing radiation in W/m2.
        rad_east (float): East-facing radiation in W/m2.
        rad_south (float): South-facing radiation in W/m2.
        rad_west (float): West-facing radiation in W/m2.
        rad_global (float): Global horizontal radiation in W/m2.
        dewpoint (Optional[float]): Dewpoint temperature in degrees C.
        sky_temp (Optional[float]): Sky temperature in degrees C.
        ground_temp (Optional[float]): Ground temperature in degrees C.
    """

    def __init__(
        self,
        _temp=0.0,
        _rad_north=0.0,
        _rad_east=0.0,
        _rad_south=0.0,
        _rad_west=0.0,
        _rad_global=0.0,
        _dewpoint_temp=None,
        _sky_temp=None,
        _ground_temp=None,
    ):
        # type: (float, float, float, float, float, float, Optional[float], Optional[float], Optional[float]) -> None
        super(Climate_PeakLoadValueSet, self).__init__()
        self.temp = _temp
        self.rad_north = _rad_north
        self.rad_east = _rad_east
        self.rad_south = _rad_south
        self.rad_west = _rad_west
        self.rad_global = _rad_global
        self.dewpoint = _dewpoint_temp
        self.sky_temp = _sky_temp
        self.ground_temp = _ground_temp

    def __copy__(self):
        # type: () -> Climate_PeakLoadValueSet
        obj = Climate_PeakLoadValueSet(
            self.temp,
            self.rad_north,
            self.rad_east,
            self.rad_south,
            self.rad_west,
            self.rad_global,
            self.dewpoint,
            self.sky_temp,
            self.ground_temp,
        )
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Climate_PeakLoadValueSet
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, float]
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["temp"] = self.temp
        d["rad_north"] = self.rad_north
        d["rad_east"] = self.rad_east
        d["rad_south"] = self.rad_south
        d["rad_west"] = self.rad_west
        d["rad_global"] = self.rad_global
        d["dewpoint"] = self.dewpoint
        d["sky_temp"] = self.sky_temp
        d["ground_temp"] = self.ground_temp

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, float]) -> Climate_PeakLoadValueSet
        obj = cls()

        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        obj.temp = _input_dict["temp"]
        obj.rad_north = _input_dict["rad_north"]
        obj.rad_east = _input_dict["rad_east"]
        obj.rad_south = _input_dict["rad_south"]
        obj.rad_west = _input_dict["rad_west"]
        obj.rad_global = _input_dict["rad_global"]
        obj.dewpoint = _input_dict["dewpoint"]
        obj.sky_temp = _input_dict["sky_temp"]
        obj.ground_temp = _input_dict["ground_temp"]

        return obj


class Climate_PeakLoadCollection(_base._Base):
    """Collection of peak heating and cooling load design conditions.

    Default construction creates four independent peak-load value sets. Explicitly
    supplied value sets are retained by identity.

    Attributes:
        heat_load_1 (Climate_PeakLoadValueSet): Primary heating design condition.
        heat_load_2 (Climate_PeakLoadValueSet): Secondary heating design condition.
        cooling_load_1 (Climate_PeakLoadValueSet): Primary cooling design condition.
        cooling_load_2 (Climate_PeakLoadValueSet): Secondary cooling design condition.
    """

    def __init__(
        self,
        _heat_load_1=None,
        _heat_load_2=None,
        _cooling_load_1=None,
        _cooling_load_2=None,
    ):
        # type: (Optional[Climate_PeakLoadValueSet], Optional[Climate_PeakLoadValueSet], Optional[Climate_PeakLoadValueSet], Optional[Climate_PeakLoadValueSet]) -> None
        super(Climate_PeakLoadCollection, self).__init__()
        self.heat_load_1 = _heat_load_1 if _heat_load_1 is not None else Climate_PeakLoadValueSet()
        self.heat_load_2 = _heat_load_2 if _heat_load_2 is not None else Climate_PeakLoadValueSet()
        self.cooling_load_1 = _cooling_load_1 if _cooling_load_1 is not None else Climate_PeakLoadValueSet()
        self.cooling_load_2 = _cooling_load_2 if _cooling_load_2 is not None else Climate_PeakLoadValueSet()

    def __copy__(self):
        # type: () -> Climate_PeakLoadCollection
        obj = Climate_PeakLoadCollection(
            self.heat_load_1.duplicate(),
            self.heat_load_2.duplicate(),
            self.cooling_load_1.duplicate(),
            self.cooling_load_2.duplicate(),
        )
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Climate_PeakLoadCollection
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[Dict[str, float], str]]
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["heat_load_1"] = self.heat_load_1.to_dict()
        d["heat_load_2"] = self.heat_load_2.to_dict()
        d["cooling_load_1"] = self.cooling_load_1.to_dict()
        d["cooling_load_2"] = self.cooling_load_2.to_dict()
        d["display_name"] = self.display_name

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate_PeakLoadCollection
        obj = cls(
            Climate_PeakLoadValueSet.from_dict(_input_dict["heat_load_1"]),
            Climate_PeakLoadValueSet.from_dict(_input_dict["heat_load_2"]),
            Climate_PeakLoadValueSet.from_dict(_input_dict["cooling_load_1"]),
            Climate_PeakLoadValueSet.from_dict(_input_dict["cooling_load_2"]),
        )
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        return obj


class Climate_Ground(_base._Base):
    """Ground thermal properties for foundation heat loss calculations.

    Attributes:
        ground_thermal_conductivity (float): Thermal conductivity in W/(mK).
            Default: 2.
        ground_heat_capacity (float): Specific heat capacity in J/(kgK).
            Default: 1000.
        ground_density (float): Density in kg/m3. Default: 2000.
        depth_groundwater (float): Depth to groundwater table in meters.
            Default: 3.
        flow_rate_groundwater (float): Groundwater flow rate in m/day.
            Default: 0.05.
    """

    def __init__(self):
        # type: () -> None
        super(Climate_Ground, self).__init__()
        self.ground_thermal_conductivity = 2
        self.ground_heat_capacity = 1000
        self.ground_density = 2000
        self.depth_groundwater = 3
        self.flow_rate_groundwater = 0.05

    def __copy__(self):
        # type: () -> Climate_Ground
        obj = Climate_Ground()
        obj.set_base_attrs_from_source(self)
        obj.ground_thermal_conductivity = self.ground_thermal_conductivity
        obj.ground_heat_capacity = self.ground_heat_capacity
        obj.ground_density = self.ground_density
        obj.depth_groundwater = self.depth_groundwater
        obj.flow_rate_groundwater = self.flow_rate_groundwater
        modeled_attributes = {
            "_identifier",
            "_display_name",
            "user_data",
            "ground_thermal_conductivity",
            "ground_heat_capacity",
            "ground_density",
            "depth_groundwater",
            "flow_rate_groundwater",
        }
        for attr_name, attr_value in vars(self).items():
            if attr_name not in modeled_attributes:
                setattr(obj, attr_name, attr_value)

        return obj

    def duplicate(self):
        # type: () -> Climate_Ground
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["ground_thermal_conductivity"] = self.ground_thermal_conductivity
        d["ground_heat_capacity"] = self.ground_heat_capacity
        d["ground_density"] = self.ground_density
        d["depth_groundwater"] = self.depth_groundwater
        d["flow_rate_groundwater"] = self.flow_rate_groundwater

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate_Ground
        obj = cls()
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        obj.ground_thermal_conductivity = _input_dict.get(
            "ground_thermal_conductivity", obj.ground_thermal_conductivity
        )
        obj.ground_heat_capacity = _input_dict.get("ground_heat_capacity", obj.ground_heat_capacity)
        obj.ground_density = _input_dict.get("ground_density", obj.ground_density)
        obj.depth_groundwater = _input_dict.get("depth_groundwater", obj.depth_groundwater)
        obj.flow_rate_groundwater = _input_dict.get("flow_rate_groundwater", obj.flow_rate_groundwater)

        return obj


class ClimateProvenance(_base._Base):
    """Source identity, conversion method, and availability for climate data.

    Availability flags describe whether source data is present; they do not
    infer completeness from numeric values, since zero is a valid climate value.

    Attributes:
        source_type (str): Source category. One of ``legacy_unknown``,
            ``phi_approved``, ``phius_approved``, ``epw_derived``, or
            ``user_defined``.
        source_name (Optional[str]): Human-readable source name.
        source_uri (Optional[str]): Source file path or URI.
        source_version (Optional[str]): Version of the source data.
        source_checksum (Optional[str]): SHA-256 checksum for a file source.
        conversion_method (Optional[str]): Algorithm used to convert the source.
        conversion_method_version (Optional[str]): Version of the conversion method.
        is_certification_approved (Optional[bool]): Whether the source is approved
            for certification; ``None`` means unknown.
        monthly_data_available (Optional[bool]): Whether monthly-demand data is available.
        peak_load_data_available (Optional[bool]): Whether peak-load data is available.
        assumptions (Dict): JSON-safe conversion assumptions.
    """

    SOURCE_TYPES = (
        "legacy_unknown",
        "phi_approved",
        "phius_approved",
        "epw_derived",
        "user_defined",
    )

    def __init__(
        self,
        source_type="legacy_unknown",
        source_name=None,
        source_uri=None,
        source_version=None,
        source_checksum=None,
        conversion_method=None,
        conversion_method_version=None,
        is_certification_approved=None,
        monthly_data_available=None,
        peak_load_data_available=None,
        assumptions=None,
    ):
        # type: (str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[bool], Optional[bool], Optional[bool], Optional[Dict]) -> None
        super(ClimateProvenance, self).__init__()
        if source_type not in self.SOURCE_TYPES:
            raise ValueError(
                "source_type must be one of {}. Got: {!r}.".format(", ".join(self.SOURCE_TYPES), source_type)
            )
        for field_name, value in (
            ("is_certification_approved", is_certification_approved),
            ("monthly_data_available", monthly_data_available),
            ("peak_load_data_available", peak_load_data_available),
        ):
            if value is not None and not isinstance(value, bool):
                raise ValueError("{} must be True, False, or None. Got: {!r}.".format(field_name, value))
        if assumptions is not None and not isinstance(assumptions, dict):
            raise ValueError("assumptions must be a dict or None. Got: {!r}.".format(assumptions))

        self.source_type = source_type
        self.source_name = source_name
        self.source_uri = source_uri
        self.source_version = source_version
        self.source_checksum = source_checksum
        self.conversion_method = conversion_method
        self.conversion_method_version = conversion_method_version
        self.is_certification_approved = is_certification_approved
        self.monthly_data_available = monthly_data_available
        self.peak_load_data_available = peak_load_data_available
        self.assumptions = assumptions if assumptions is not None else {}

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return {
            "display_name": self.display_name,
            "identifier": self.identifier,
            "user_data": copy(self.user_data),
            "source_type": self.source_type,
            "source_name": self.source_name,
            "source_uri": self.source_uri,
            "source_version": self.source_version,
            "source_checksum": self.source_checksum,
            "conversion_method": self.conversion_method,
            "conversion_method_version": self.conversion_method_version,
            "is_certification_approved": self.is_certification_approved,
            "monthly_data_available": self.monthly_data_available,
            "peak_load_data_available": self.peak_load_data_available,
            "assumptions": deepcopy(self.assumptions),
        }

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> ClimateProvenance
        obj = cls(
            source_type=_input_dict.get("source_type", "legacy_unknown"),
            source_name=_input_dict.get("source_name"),
            source_uri=_input_dict.get("source_uri"),
            source_version=_input_dict.get("source_version"),
            source_checksum=_input_dict.get("source_checksum"),
            conversion_method=_input_dict.get("conversion_method"),
            conversion_method_version=_input_dict.get("conversion_method_version"),
            is_certification_approved=_input_dict.get("is_certification_approved"),
            monthly_data_available=_input_dict.get("monthly_data_available"),
            peak_load_data_available=_input_dict.get("peak_load_data_available"),
            assumptions=deepcopy(_input_dict.get("assumptions", {})),
        )
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = copy(_input_dict.get("user_data", {}))
        return obj

    def __copy__(self):
        # type: () -> ClimateProvenance
        obj = ClimateProvenance(
            source_type=self.source_type,
            source_name=self.source_name,
            source_uri=self.source_uri,
            source_version=self.source_version,
            source_checksum=self.source_checksum,
            conversion_method=self.conversion_method,
            conversion_method_version=self.conversion_method_version,
            is_certification_approved=self.is_certification_approved,
            monthly_data_available=self.monthly_data_available,
            peak_load_data_available=self.peak_load_data_available,
            assumptions=deepcopy(self.assumptions),
        )
        obj.set_base_attrs_from_source(self)
        return obj

    def duplicate(self):
        # type: () -> ClimateProvenance
        return self.__copy__()


class Climate(_base._Base):
    """Complete climate dataset for PH energy modeling.

    Contains monthly temperatures, monthly radiation, peak load conditions,
    and ground thermal properties. Default construction creates a fresh nested
    graph; explicitly supplied collections are retained by identity.

    Attributes:
        station_elevation (float): Weather station elevation in meters.
        summer_daily_temperature_swing (float): Daily temperature swing in K.
            Default: 8.0.
        average_wind_speed (float): Average wind speed in m/s. Default: 4.0.
        ground (Climate_Ground): Ground thermal properties.
        monthly_temps (Climate_MonthlyTempCollection): Monthly temperature data.
        monthly_radiation (Climate_MonthlyRadiationCollection): Monthly radiation data.
        peak_loads (Optional[Climate_PeakLoadCollection]): Peak load design conditions.
        provenance (Optional[ClimateProvenance]): Source and availability metadata.
    """

    def __init__(
        self,
        _display_name="New York",
        _station_elevation=0.0,
        _daily_temp_swing=8.0,
        _average_wind_speed=4.0,
        _monthly_temps=None,
        _monthly_radiation=None,
        _peak_loads=None,
        _provenance=None,
    ):
        # type: (str, float, float, float, Optional[Climate_MonthlyTempCollection], Optional[Climate_MonthlyRadiationCollection], Optional[Climate_PeakLoadCollection], Optional[ClimateProvenance]) -> None
        super(Climate, self).__init__()
        self.display_name = _display_name
        self.station_elevation = _station_elevation  # m
        self.summer_daily_temperature_swing = _daily_temp_swing  # Deg-K
        self.average_wind_speed = _average_wind_speed  # m/s

        self.ground = Climate_Ground()
        self.monthly_temps = _monthly_temps if _monthly_temps is not None else Climate_MonthlyTempCollection()
        self.monthly_radiation = (
            _monthly_radiation if _monthly_radiation is not None else Climate_MonthlyRadiationCollection()
        )
        self.provenance = _provenance
        peak_loads_unavailable = self.provenance is not None and self.provenance.peak_load_data_available is False
        if _peak_loads is not None:
            self.peak_loads = _peak_loads
        elif peak_loads_unavailable:
            self.peak_loads = None
        else:
            self.peak_loads = Climate_PeakLoadCollection()

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["station_elevation"] = self.station_elevation
        d["summer_daily_temperature_swing"] = self.summer_daily_temperature_swing
        d["average_wind_speed"] = self.average_wind_speed
        d["ground"] = self.ground.to_dict()
        d["monthly_temps"] = self.monthly_temps.to_dict()
        d["monthly_radiation"] = self.monthly_radiation.to_dict()
        d["peak_loads"] = self.peak_loads.to_dict() if self.peak_loads is not None else None
        if self.provenance is not None:
            d["provenance"] = self.provenance.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate
        peak_loads_dict = _input_dict.get("peak_loads")
        peak_loads = Climate_PeakLoadCollection.from_dict(peak_loads_dict) if peak_loads_dict is not None else None
        peak_loads_is_explicit_null = "peak_loads" in _input_dict and peak_loads_dict is None
        provenance_dict = _input_dict.get("provenance")
        obj = cls(
            _display_name=_input_dict.get("display_name", "New York"),
            _station_elevation=_input_dict["station_elevation"],
            _daily_temp_swing=_input_dict["summer_daily_temperature_swing"],
            _average_wind_speed=_input_dict["average_wind_speed"],
            _monthly_temps=Climate_MonthlyTempCollection.from_dict(_input_dict.get("monthly_temps", {})),
            _monthly_radiation=Climate_MonthlyRadiationCollection.from_dict(_input_dict.get("monthly_radiation", {})),
            _peak_loads=peak_loads,
            _provenance=ClimateProvenance.from_dict(provenance_dict) if provenance_dict is not None else None,
        )
        if peak_loads_is_explicit_null:
            obj.peak_loads = None
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = copy(_input_dict.get("user_data", {}))
        obj.ground = Climate_Ground.from_dict(_input_dict.get("ground", {}))

        return obj

    def __copy__(self):
        # type: () -> Climate
        obj = Climate(
            self.display_name,
            self.station_elevation,
            self.summer_daily_temperature_swing,
            self.average_wind_speed,
            self.monthly_temps.duplicate(),
            self.monthly_radiation.duplicate(),
            self.peak_loads.duplicate() if self.peak_loads is not None else None,
            self.provenance.duplicate() if self.provenance is not None else None,
        )
        if self.peak_loads is None:
            obj.peak_loads = None
        obj.set_base_attrs_from_source(self)
        obj.ground = self.ground.duplicate()
        modeled_attributes = {
            "_identifier",
            "_display_name",
            "user_data",
            "station_elevation",
            "summer_daily_temperature_swing",
            "average_wind_speed",
            "ground",
            "monthly_temps",
            "monthly_radiation",
            "peak_loads",
            "provenance",
        }
        for attr_name, attr_value in vars(self).items():
            if attr_name not in modeled_attributes:
                setattr(obj, attr_name, attr_value)

        return obj

    def duplicate(self):
        # type: () -> Climate
        return self.__copy__()

    def monthly_demand_readiness_issues(self):
        # type: () -> List[str]
        """Return deterministic issues preventing monthly-demand use."""
        if self.provenance is None:
            return ["provenance: monthly climate data availability is unknown for this legacy climate."]
        if self.provenance.monthly_data_available is False:
            return ["provenance.monthly_data_available: monthly climate data is explicitly unavailable."]
        if self.provenance.monthly_data_available is None:
            return ["provenance.monthly_data_available: monthly climate data availability is unknown."]

        issues = []
        scalar_fields = (
            ("station_elevation", self.station_elevation),
            ("summer_daily_temperature_swing", self.summer_daily_temperature_swing),
            ("average_wind_speed", self.average_wind_speed),
        )
        monthly_fields = (
            ("monthly_temps.air_temps", self.monthly_temps.air_temps),
            ("monthly_temps.dewpoints", self.monthly_temps.dewpoints),
            ("monthly_temps.sky_temps", self.monthly_temps.sky_temps),
            ("monthly_temps.ground_temps", self.monthly_temps.ground_temps),
            ("monthly_radiation.north", self.monthly_radiation.north),
            ("monthly_radiation.east", self.monthly_radiation.east),
            ("monthly_radiation.south", self.monthly_radiation.south),
            ("monthly_radiation.west", self.monthly_radiation.west),
            ("monthly_radiation.glob", self.monthly_radiation.glob),
        )
        for field_name, value in scalar_fields:
            issue = _finite_value_issue(field_name, value)
            if issue:
                issues.append(issue)
        for field_name, value_set in monthly_fields:
            for month_name, value in zip(value_set.months, value_set.values):
                issue = _finite_value_issue("{}.{}".format(field_name, month_name), value)
                if issue:
                    issues.append(issue)
        return issues

    @property
    def is_monthly_demand_ready(self):
        # type: () -> bool
        """Whether all explicitly available monthly-demand fields are finite."""
        return not self.monthly_demand_readiness_issues()

    def peak_load_readiness_issues(self):
        # type: () -> List[str]
        """Return deterministic issues preventing peak-load use."""
        if self.provenance is None:
            return ["provenance: peak-load climate data availability is unknown for this legacy climate."]
        if self.provenance.peak_load_data_available is False:
            return [
                "provenance.peak_load_data_available: approved or specialized peak-load climate data must be supplied separately."
            ]
        if self.provenance.peak_load_data_available is None:
            return ["provenance.peak_load_data_available: peak-load climate data availability is unknown."]
        if self.peak_loads is None:
            return ["peak_loads: data is marked available but no peak-load collection is present."]

        issues = []
        load_sets = (
            ("peak_loads.heat_load_1", self.peak_loads.heat_load_1),
            ("peak_loads.heat_load_2", self.peak_loads.heat_load_2),
            ("peak_loads.cooling_load_1", self.peak_loads.cooling_load_1),
            ("peak_loads.cooling_load_2", self.peak_loads.cooling_load_2),
        )
        value_names = ("temp", "rad_north", "rad_east", "rad_south", "rad_west", "rad_global")
        for field_name, value_set in load_sets:
            for value_name in value_names:
                issue = _finite_value_issue("{}.{}".format(field_name, value_name), getattr(value_set, value_name))
                if issue:
                    issues.append(issue)
        return issues

    @property
    def is_peak_load_ready(self):
        # type: () -> bool
        """Whether all explicitly available peak-load fields are finite."""
        return not self.peak_load_readiness_issues()


class Location(_base._Base):
    """Geographic location data for the building site.

    Attributes:
        latitude (float): Site latitude in decimal degrees. Default: 40.6.
        longitude (float): Site longitude in decimal degrees. Default: -73.8.
        site_elevation (Optional[float]): Site elevation in meters above sea level.
        climate_zone (Optional[int]): ASHRAE climate zone number, or None when
            the source does not supply one. Default: 1.
        hours_from_UTC (int): Time zone offset from UTC in hours. Default: -4.
    """

    def __init__(
        self,
        latitude=40.6,
        longitude=-73.8,
        site_elevation=None,
        climate_zone=1,
        hours_from_UTC=-4,
    ):
        # type: (float, float, Optional[float], Optional[int], int) -> None
        super(Location, self).__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.site_elevation = site_elevation
        self.climate_zone = climate_zone
        self.hours_from_UTC = hours_from_UTC

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        d["latitude"] = self.latitude
        d["longitude"] = self.longitude
        d["site_elevation"] = self.site_elevation
        d["climate_zone"] = self.climate_zone
        d["hours_from_UTC"] = self.hours_from_UTC

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> Location
        obj = cls(
            _input_dict["latitude"],
            _input_dict["longitude"],
            _input_dict["site_elevation"],
            _input_dict["climate_zone"],
            _input_dict["hours_from_UTC"],
        )
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        return obj

    def __copy__(self):
        # type: () -> Location
        obj = Location(
            self.latitude,
            self.longitude,
            self.site_elevation,
            self.climate_zone,
            self.hours_from_UTC,
        )
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Location
        return self.__copy__()


class PHPPCodes(_base._Base):
    """PHPP climate library reference codes.

    Identifies a specific climate dataset in the PHPP library by country,
    region, and dataset name.

    Attributes:
        country_code (str): PHPP country code string.
            Default: "US-United States of America".
        region_code (str): PHPP region code string. Default: "New York".
        dataset_name (str): PHPP dataset identifier. Default: "US0055c-New York".
    """

    def __init__(
        self,
        _country_code="US-United States of America",
        _region_code="New York",
        _dataset_name="US0055c-New York",
    ):
        # type: (str, str, str) -> None
        super(PHPPCodes, self).__init__()
        self.country_code = _country_code
        self.region_code = _region_code
        self.dataset_name = _dataset_name

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["country_code"] = self.country_code
        d["region_code"] = self.region_code
        d["dataset_name"] = self.dataset_name
        d["display_name"] = self.dataset_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        return d

    @classmethod
    def blank(cls):
        # type: () -> PHPPCodes
        """Create a record with no PHPP climate-library identity."""
        return cls("", "", "")

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PHPPCodes
        obj = cls(
            _input_dict["country_code"],
            _input_dict["region_code"],
            _input_dict["dataset_name"],
        )
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        return obj

    def __copy__(self):
        # type: () -> PHPPCodes
        obj = PHPPCodes(
            self.country_code,
            self.region_code,
            self.dataset_name,
        )
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> PHPPCodes
        return self.__copy__()


class Site(_base._Base):
    """Complete site data combining location, climate, and PHPP library codes.

    Default construction creates a fresh location, climate graph, and PHPP code
    object. Explicitly supplied child objects are retained by identity.

    Attributes:
        location (Location): Geographic location data.
        climate (Climate): Climate dataset for energy modeling.
        phpp_library_codes (PHPPCodes): PHPP climate library reference codes.
    """

    def __init__(
        self,
        _location=None,
        _climate=None,
        _phpp_library_codes=None,
    ):
        # type: (Optional[Location], Optional[Climate], Optional[PHPPCodes]) -> None
        super(Site, self).__init__()
        self.location = _location if _location is not None else Location()
        self.climate = _climate if _climate is not None else Climate()
        self.phpp_library_codes = _phpp_library_codes if _phpp_library_codes is not None else PHPPCodes()

    @classmethod
    def from_epw(cls, file_path, ground_temperature_depth=None, ground_reflectance=0.2, diffuse_model="isotropic"):
        # type: (str, Optional[float], float, str) -> Site
        """Create a preliminary monthly-demand Site from a caller-supplied EPW.

        EPW-derived values are not PHI/Phius certification climate data. The
        returned Site has blank PHPP library codes and no peak-load climate.

        Arguments:
        ----------
            * file_path (str): Path to a local annual EPW file.
            * ground_temperature_depth (Optional[float]): EPW ground-series
                depth in meters. May be omitted only when exactly one series
                is available.
            * ground_reflectance (float): Finite directional-radiation ground
                reflectance from 0 through 1. Default: 0.2.
            * diffuse_model (str): ``"isotropic"`` or ``"anisotropic"``.

        Returns:
        --------
            * Site: A fresh, monthly-demand-ready preliminary Site.

        Raises:
        -------
            * ValueError: If options or required EPW source data are invalid.
                All independently detected conversion issues are included.
        """
        from honeybee_ph._epw import convert_epw

        result = convert_epw(
            file_path,
            ground_temperature_depth=ground_temperature_depth,
            ground_reflectance=ground_reflectance,
            diffuse_model=diffuse_model,
        )
        if result.issues:
            raise ValueError("EPW conversion failed:\n- {}".format("\n- ".join(result.issues)))

        location = Location(
            latitude=result.latitude,
            longitude=result.longitude,
            site_elevation=result.elevation,
            climate_zone=None,
            hours_from_UTC=result.utc_offset,
        )
        location.display_name = result.location_name

        monthly_temps = Climate_MonthlyTempCollection(
            Climate_MonthlyValueSet(result.monthly_air_temperatures),
            Climate_MonthlyValueSet(result.monthly_dewpoint_temperatures),
            Climate_MonthlyValueSet(result.monthly_sky_temperatures),
            Climate_MonthlyValueSet(result.monthly_ground_temperatures),
        )
        monthly_radiation = Climate_MonthlyRadiationCollection(
            Climate_MonthlyValueSet(result.monthly_north_radiation),
            Climate_MonthlyValueSet(result.monthly_east_radiation),
            Climate_MonthlyValueSet(result.monthly_south_radiation),
            Climate_MonthlyValueSet(result.monthly_west_radiation),
            Climate_MonthlyValueSet(result.monthly_global_radiation),
        )
        climate = Climate(
            _display_name=result.location_name,
            _station_elevation=result.elevation,
            _daily_temp_swing=result.summer_daily_temperature_swing,
            _average_wind_speed=result.average_wind_speed,
            _monthly_temps=monthly_temps,
            _monthly_radiation=monthly_radiation,
            _peak_loads=None,
            _provenance=result.provenance,
        )
        obj = cls(location, climate, PHPPCodes.blank())
        obj.display_name = result.location_name
        return obj

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["location"] = self.location.to_dict()
        d["climate"] = self.climate.to_dict()
        d["phpp_library_codes"] = self.phpp_library_codes.to_dict()
        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> Site
        obj = cls(
            Location.from_dict(_input_dict["location"]),
            Climate.from_dict(_input_dict["climate"]),
            PHPPCodes.from_dict(_input_dict["phpp_library_codes"]),
        )
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = copy(_input_dict.get("user_data", {}))

        return obj

    def __copy__(self):
        # type: () -> Site
        obj = Site(self.location.duplicate(), self.climate.duplicate(), self.phpp_library_codes.duplicate())
        obj.set_base_attrs_from_source(self)

        return obj

    def duplicate(self):
        # type: () -> Site
        return self.__copy__()
