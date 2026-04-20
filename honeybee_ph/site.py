# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive-House Style Monthly Climate Data"""

from copy import copy

try:
    from itertools import izip as zip  # type: ignore
except ImportError:
    pass  # Python3

try:
    from typing import Any, Collection, Dict, List, Optional, Union
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import _base


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

    def __init__(self, _values=[0.0] * 12):
        # type: (Collection[float]) -> None
        super(Climate_MonthlyValueSet, self).__init__()
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
        obj = Climate_MonthlyValueSet(copy(self.values))
        obj.set_base_attrs_from_source(self)
        for month in self.months:
            setattr(obj, month, getattr(self, month))

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
        obj.user_data = _input_dict.get("user_data", {})

        for month in cls.months:
            setattr(obj, month, _input_dict.get(month))

        return obj


class Climate_MonthlyTempCollection(_base._Base):
    """Collection of monthly temperature data sets.

    Attributes:
        air_temps (Climate_MonthlyValueSet): Monthly air temperatures in degrees C.
        dewpoints (Climate_MonthlyValueSet): Monthly dewpoint temperatures in degrees C.
        sky_temps (Climate_MonthlyValueSet): Monthly sky temperatures in degrees C.
        ground_temps (Climate_MonthlyValueSet): Monthly ground temperatures in degrees C.
    """

    def __init__(
        self,
        _air=Climate_MonthlyValueSet(),
        _dewpoint=Climate_MonthlyValueSet(),
        _sky=Climate_MonthlyValueSet(),
        _ground=Climate_MonthlyValueSet(),
    ):
        # type: (Climate_MonthlyValueSet, Climate_MonthlyValueSet, Climate_MonthlyValueSet, Climate_MonthlyValueSet) -> None
        super(Climate_MonthlyTempCollection, self).__init__()
        self.air_temps = _air
        self.dewpoints = _dewpoint
        self.sky_temps = _sky
        self.ground_temps = _ground

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
        obj.user_data = _input_dict.get("user_data", {})

        return obj


class Climate_MonthlyRadiationCollection(_base._Base):
    """Collection of monthly solar radiation data by orientation.

    Attributes:
        north (Climate_MonthlyValueSet): Monthly north-facing radiation in kWh/m2.
        east (Climate_MonthlyValueSet): Monthly east-facing radiation in kWh/m2.
        south (Climate_MonthlyValueSet): Monthly south-facing radiation in kWh/m2.
        west (Climate_MonthlyValueSet): Monthly west-facing radiation in kWh/m2.
        glob (Climate_MonthlyValueSet): Monthly global horizontal radiation in kWh/m2.
    """

    def __init__(
        self,
        _north=Climate_MonthlyValueSet(),
        _east=Climate_MonthlyValueSet(),
        _south=Climate_MonthlyValueSet(),
        _west=Climate_MonthlyValueSet(),
        _glob=Climate_MonthlyValueSet(),
    ):
        super(Climate_MonthlyRadiationCollection, self).__init__()
        # type: (Climate_MonthlyValueSet, Climate_MonthlyValueSet, Climate_MonthlyValueSet, Climate_MonthlyValueSet) -> None
        self.north = _north
        self.east = _east
        self.south = _south
        self.west = _west
        self.glob = _glob

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
        obj.user_data = _input_dict.get("user_data", {})

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
        obj.user_data = _input_dict.get("user_data", {})

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

    Attributes:
        heat_load_1 (Climate_PeakLoadValueSet): Primary heating design condition.
        heat_load_2 (Climate_PeakLoadValueSet): Secondary heating design condition.
        cooling_load_1 (Climate_PeakLoadValueSet): Primary cooling design condition.
        cooling_load_2 (Climate_PeakLoadValueSet): Secondary cooling design condition.
    """

    def __init__(
        self,
        _heat_load_1=Climate_PeakLoadValueSet(),
        _heat_load_2=Climate_PeakLoadValueSet(),
        _cooling_load_1=Climate_PeakLoadValueSet(),
        _cooling_load_2=Climate_PeakLoadValueSet(),
    ):
        # type: (Climate_PeakLoadValueSet, Climate_PeakLoadValueSet, Climate_PeakLoadValueSet, Climate_PeakLoadValueSet) -> None
        super(Climate_PeakLoadCollection, self).__init__()
        self.heat_load_1 = _heat_load_1
        self.heat_load_2 = _heat_load_2
        self.cooling_load_1 = _cooling_load_1
        self.cooling_load_2 = _cooling_load_2

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
        obj.user_data = _input_dict.get("user_data", {})

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
        for attr_nm, attr_val in vars(self).items():
            setattr(obj, attr_nm, attr_val)

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
        obj.user_data = _input_dict.get("user_data", {})

        obj.ground_thermal_conductivity = _input_dict.get(
            "ground_thermal_conductivity", obj.ground_thermal_conductivity
        )
        obj.ground_heat_capacity = _input_dict.get("ground_heat_capacity", obj.ground_heat_capacity)
        obj.ground_density = _input_dict.get("ground_density", obj.ground_density)
        obj.depth_groundwater = _input_dict.get("depth_groundwater", obj.depth_groundwater)
        obj.flow_rate_groundwater = _input_dict.get("flow_rate_groundwater", obj.flow_rate_groundwater)

        return obj


class Climate(_base._Base):
    """Complete climate dataset for PH energy modeling.

    Contains monthly temperatures, monthly radiation, peak load conditions,
    and ground thermal properties.

    Attributes:
        station_elevation (float): Weather station elevation in meters.
        summer_daily_temperature_swing (float): Daily temperature swing in K.
            Default: 8.0.
        average_wind_speed (float): Average wind speed in m/s. Default: 4.0.
        ground (Climate_Ground): Ground thermal properties.
        monthly_temps (Climate_MonthlyTempCollection): Monthly temperature data.
        monthly_radiation (Climate_MonthlyRadiationCollection): Monthly radiation data.
        peak_loads (Climate_PeakLoadCollection): Peak load design conditions.
    """

    def __init__(
        self,
        _display_name="New York",
        _station_elevation=0.0,
        _daily_temp_swing=8.0,
        _average_wind_speed=4.0,
        _monthly_temps=Climate_MonthlyTempCollection(),
        _monthly_radiation=Climate_MonthlyRadiationCollection(),
        _peak_loads=Climate_PeakLoadCollection(),
    ):
        # type: (str, float, float, float, Climate_MonthlyTempCollection, Climate_MonthlyRadiationCollection, Climate_PeakLoadCollection) -> None
        super(Climate, self).__init__()
        self.display_name = _display_name
        self.station_elevation = _station_elevation  # m
        self.summer_daily_temperature_swing = _daily_temp_swing  # Deg-K
        self.average_wind_speed = _average_wind_speed  # m/s

        self.ground = Climate_Ground()
        self.monthly_temps = _monthly_temps
        self.monthly_radiation = _monthly_radiation
        self.peak_loads = _peak_loads

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
        d["peak_loads"] = self.peak_loads.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate
        obj = cls()

        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = _input_dict.get("user_data", {})

        obj.station_elevation = _input_dict["station_elevation"]
        obj.summer_daily_temperature_swing = _input_dict["summer_daily_temperature_swing"]
        obj.average_wind_speed = _input_dict["average_wind_speed"]

        obj.ground = Climate_Ground.from_dict(_input_dict.get("ground", {}))
        obj.monthly_temps = Climate_MonthlyTempCollection.from_dict(_input_dict.get("monthly_temps", {}))
        obj.monthly_radiation = Climate_MonthlyRadiationCollection.from_dict(_input_dict.get("monthly_radiation", {}))
        obj.peak_loads = Climate_PeakLoadCollection.from_dict(_input_dict.get("peak_loads", {}))

        return obj

    def __copy__(self):
        # type: () -> Climate
        obj = Climate()
        obj.set_base_attrs_from_source(self)
        for attr_nm, attr_val in vars(self).items():
            setattr(obj, attr_nm, attr_val)

        return obj

    def duplicate(self):
        # type: () -> Climate
        return self.__copy__()


class Location(_base._Base):
    """Geographic location data for the building site.

    Attributes:
        latitude (float): Site latitude in decimal degrees. Default: 40.6.
        longitude (float): Site longitude in decimal degrees. Default: -73.8.
        site_elevation (Optional[float]): Site elevation in meters above sea level.
        climate_zone (int): ASHRAE climate zone number. Default: 1.
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
        # type: (float, float, Optional[float], int, int) -> None
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
        obj.user_data = _input_dict.get("user_data", {})

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
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PHPPCodes
        obj = cls(
            _input_dict["country_code"],
            _input_dict["region_code"],
            _input_dict["dataset_name"],
        )
        obj.display_name = _input_dict.get("display_name", obj.display_name)
        obj.identifier = _input_dict.get("identifier", obj.identifier)
        obj.user_data = _input_dict.get("user_data", {})

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

    Attributes:
        location (Location): Geographic location data.
        climate (Climate): Climate dataset for energy modeling.
        phpp_library_codes (PHPPCodes): PHPP climate library reference codes.
    """

    def __init__(
        self,
        _location=Location(),
        _climate=Climate(),
        _phpp_library_codes=PHPPCodes(),
    ):
        # type: (Location, Climate, PHPPCodes) -> None
        super(Site, self).__init__()
        self.location = _location
        self.climate = _climate
        self.phpp_library_codes = _phpp_library_codes

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
        obj.user_data = _input_dict.get("user_data", {})

        return obj

    def __copy__(self):
        # type: () -> Site
        obj = Site()

        obj.set_base_attrs_from_source(self)
        obj.location = self.location.duplicate()
        obj.climate = self.climate.duplicate()
        obj.phpp_library_codes = self.phpp_library_codes.duplicate()

        return obj

    def duplicate(self):
        # type: () -> Site
        return self.__copy__()
