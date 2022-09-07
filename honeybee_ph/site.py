# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive-House Style Monthly Climate Data"""

try:
    from itertools import izip as zip  # type: ignore
except ImportError:
    pass  # Python3

try:
    from typing import Dict, List, Collection, Any, Union, Optional
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import _base


class Climate_MonthlyValueSet(_base._Base):
    """A set of 12 monthly values (temp, radiation, etc)."""

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

    def __init__(self, _values=[0.0]*12):
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
            msg = "Error: Monthly data should be a collection of 12 numeric items.\n"\
                  "Got a {} of length: {}?".format(type(_in), len(_in))
            raise Exception(msg)

        for val, month_name in zip(_in, self.months):
            setattr(self, month_name, val)

    def to_dict(self):
        # type: () -> Dict[str, float]
        d = {}

        for month in self.months:
            d[month] = getattr(self, month)

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, float]) -> Climate_MonthlyValueSet
        obj = cls()

        for month in cls.months:
            setattr(obj, month, _input_dict.get(month))

        return obj


class Climate_MonthlyTempCollection(_base._Base):
    """Collection class to organize monthly temperature values"""

    def __init__(self,
                 _air=Climate_MonthlyValueSet(),
                 _dewpoint=Climate_MonthlyValueSet(),
                 _sky=Climate_MonthlyValueSet(),
                 _ground=Climate_MonthlyValueSet()
                 ):
        # type: (Climate_MonthlyValueSet, Climate_MonthlyValueSet, Climate_MonthlyValueSet, Climate_MonthlyValueSet) -> None
        super(Climate_MonthlyTempCollection, self).__init__()
        self.air_temps = _air
        self.dewpoints = _dewpoint
        self.sky_temps = _sky
        self.ground_temps = _ground

    def to_dict(self):
        # type: () -> Dict[str, Dict[str, float]]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["air_temps"] = self.air_temps.to_dict()
        d["dewpoints"] = self.dewpoints.to_dict()
        d["sky_temps"] = self.sky_temps.to_dict()
        d["ground_temps"] = self.ground_temps.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Dict[str, float]]) -> Climate_MonthlyTempCollection
        new_obj = cls(
            _air=Climate_MonthlyValueSet.from_dict(_input_dict["air_temps"]),
            _dewpoint=Climate_MonthlyValueSet.from_dict(_input_dict["dewpoints"]),
            _sky=Climate_MonthlyValueSet.from_dict(_input_dict["sky_temps"]),
            _ground=Climate_MonthlyValueSet.from_dict(_input_dict["ground_temps"]),
        )
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]

        return new_obj


class Climate_MonthlyRadiationCollection(_base._Base):

    def __init__(self,
                 _north=Climate_MonthlyValueSet(),
                 _east=Climate_MonthlyValueSet(),
                 _south=Climate_MonthlyValueSet(),
                 _west=Climate_MonthlyValueSet(),
                 _glob=Climate_MonthlyValueSet()):
        super(Climate_MonthlyRadiationCollection, self).__init__()
        self.north = _north
        self.east = _east
        self.south = _south
        self.west = _west
        self.glob = _glob

    def to_dict(self):
        # type: () -> Dict[str, Dict[str, float]]
        d = {}

        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["north"] = self.north.to_dict()
        d["east"] = self.east.to_dict()
        d["south"] = self.south.to_dict()
        d["west"] = self.west.to_dict()
        d["glob"] = self.glob.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Dict[str, float]]) -> Climate_MonthlyRadiationCollection
        new_obj = cls(
            _north=Climate_MonthlyValueSet.from_dict(_input_dict["north"]),
            _east=Climate_MonthlyValueSet.from_dict(_input_dict["east"]),
            _south=Climate_MonthlyValueSet.from_dict(_input_dict["south"]),
            _west=Climate_MonthlyValueSet.from_dict(_input_dict["west"]),
            _glob=Climate_MonthlyValueSet.from_dict(_input_dict["glob"]),
        )
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]

        return new_obj


class Climate_PeakLoadValueSet(_base._Base):
    """A set of Peak Load data."""

    def __init__(self,
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

    def to_dict(self):
        # type: () -> Dict[str, float]
        d = {}

        d['temp'] = self.temp
        d['rad_north'] = self.rad_north
        d['rad_east'] = self.rad_east
        d['rad_south'] = self.rad_south
        d['rad_west'] = self.rad_west
        d['rad_global'] = self.rad_global
        d["dewpoint"] = self.dewpoint
        d["sky_temp"] = self.sky_temp
        d["ground_temp"] = self.ground_temp

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, float]) -> Climate_PeakLoadValueSet
        new_obj = cls()

        new_obj.temp = _input_dict["temp"]
        new_obj.rad_north = _input_dict["rad_north"]
        new_obj.rad_east = _input_dict["rad_east"]
        new_obj.rad_south = _input_dict["rad_south"]
        new_obj.rad_west = _input_dict["rad_west"]
        new_obj.rad_global = _input_dict["rad_global"]
        new_obj.rad_global = _input_dict["dewpoint"]
        new_obj.rad_global = _input_dict["sky_temp"]
        new_obj.rad_global = _input_dict["ground_temp"]

        return new_obj


class Climate_PeakLoadCollection(_base._Base):
    """A Collection of Peak Loads (Heating and Cooling)."""

    def __init__(self,
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

    def to_dict(self):
        # type: () -> Dict[str, Union[Dict[str, float], str]]
        d = {}

        d["heat_load_1"] = self.heat_load_1.to_dict()
        d["heat_load_2"] = self.heat_load_2.to_dict()
        d["cooling_load_1"] = self.cooling_load_1.to_dict()
        d["cooling_load_2"] = self.cooling_load_2.to_dict()
        d["display_name"] = self.display_name
        d["identifier"] = self.identifier

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate_PeakLoadCollection
        new_obj = cls(
            Climate_PeakLoadValueSet.from_dict(_input_dict["heat_load_1"]),
            Climate_PeakLoadValueSet.from_dict(_input_dict["heat_load_2"]),
            Climate_PeakLoadValueSet.from_dict(_input_dict["cooling_load_1"]),
            Climate_PeakLoadValueSet.from_dict(_input_dict["cooling_load_2"]),
        )
        new_obj.display_name = _input_dict["display_name"]
        new_obj.identifier = _input_dict["identifier"]

        return new_obj


class Climate_Ground(_base._Base):
    def __init__(self):
        super(Climate_Ground, self).__init__()
        self.ground_thermal_conductivity = 2
        self.ground_heat_capacity = 1000
        self.ground_density = 2000
        self.depth_groundwater = 3
        self.flow_rate_groundwater = 0.05

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["ground_thermal_conductivity"] = self.ground_thermal_conductivity
        d["ground_heat_capacity"] = self.ground_heat_capacity
        d["ground_density"] = self.ground_density
        d["depth_groundwater"] = self.depth_groundwater
        d["flow_rate_groundwater"] = self.flow_rate_groundwater

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate_Ground
        new_obj = cls()

        new_obj.ground_thermal_conductivity = _input_dict.get(
            "ground_thermal_conductivity")
        new_obj.ground_heat_capacity = _input_dict.get(
            "ground_heat_capacity")
        new_obj.ground_density = _input_dict.get("ground_density")
        new_obj.depth_groundwater = _input_dict.get("depth_groundwater")
        new_obj.flow_rate_groundwater = _input_dict.get(
            "flow_rate_groundwater")

        return new_obj


class Climate(_base._Base):
    def __init__(self,
                 _display_name="New York",
                 _station_elevation=0.0,
                 _daily_temp_swing=8.0,
                 _average_wind_speed=4.0,
                 _monthly_temps=Climate_MonthlyTempCollection(),
                 _monthly_radiation=Climate_MonthlyRadiationCollection(),
                 _peak_loads=Climate_PeakLoadCollection()
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
        new_obj = cls()

        new_obj.display_name = _input_dict["display_name"]
        new_obj.identifier = _input_dict["identifier"]
        new_obj.station_elevation = _input_dict["station_elevation"]
        new_obj.summer_daily_temperature_swing = _input_dict["summer_daily_temperature_swing"]
        new_obj.average_wind_speed = _input_dict["average_wind_speed"]

        new_obj.ground = Climate_Ground.from_dict(
            _input_dict.get("ground", {}))
        new_obj.monthly_temps = Climate_MonthlyTempCollection.from_dict(
            _input_dict.get("monthly_temps", {}))
        new_obj.monthly_radiation = Climate_MonthlyRadiationCollection.from_dict(
            _input_dict.get("monthly_radiation", {}))
        new_obj.peak_loads = Climate_PeakLoadCollection.from_dict(
            _input_dict.get("peak_loads", {}))

        return new_obj

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
    """Geographic Location Information."""

    def __init__(self,
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

        d["latitude"] = self.latitude
        d["longitude"] = self.longitude
        d["site_elevation"] = self.site_elevation
        d["climate_zone"] = self.climate_zone
        d["hours_from_UTC"] = self.hours_from_UTC
        d["display_name"] = self.display_name
        d["identifier"] = self.identifier

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> Location
        new_obj = cls(
            _input_dict["latitude"],
            _input_dict["longitude"],
            _input_dict["site_elevation"],
            _input_dict["climate_zone"],
            _input_dict["hours_from_UTC"],
        )
        new_obj.display_name = _input_dict["display_name"]
        new_obj.identifier = _input_dict["identifier"]

        return new_obj

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
    """Settings / names if using Pre-loaded PHPP Library Data"""

    def __init__(self,
                 _country_code="US-United States of America",
                 _region_code="New York",
                 _dataset_name="US0055b-New York",
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

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PHPPCodes
        obj = cls(
            _input_dict["country_code"],
            _input_dict["region_code"],
            _input_dict["dataset_name"],
        )
        obj.display_name = _input_dict["display_name"]
        obj.identifier = _input_dict["identifier"]
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
    """Location and Climate data for the building site."""

    def __init__(self,
                 _location=Location(),
                 _climate=Climate(),
                 _phpp_library_codes=PHPPCodes(),
                 ):
        super(Site, self).__init__()
        self.location = _location
        self.climate = _climate
        self.phpp_library_codes = _phpp_library_codes

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d['location'] = self.location.to_dict()
        d['climate'] = self.climate.to_dict()
        d['phpp_library_codes'] = self.phpp_library_codes.to_dict()
        d['display_name'] = self.display_name
        d['identifier'] = self.identifier

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> Site
        obj = cls(
            Location.from_dict(_input_dict['location']),
            Climate.from_dict(_input_dict['climate']),
            PHPPCodes.from_dict(_input_dict['phpp_library_codes']),
        )
        obj.display_name = _input_dict["display_name"]
        obj.identifier = _input_dict["identifier"]

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
