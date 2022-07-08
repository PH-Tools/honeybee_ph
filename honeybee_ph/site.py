# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive-House Style Monthly Climate Data"""

try:
    from itertools import izip as zip
except ImportError:
    pass  # Python3

try:
    from typing import Dict, List, Collection
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import _base


class Climate_MonthlyValueCollection(_base._Base):
    """Collection class to organize monthly climate values"""

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

    def __init__(self):
        super(Climate_MonthlyValueCollection, self).__init__()
        for month_name in self.months:
            setattr(self, month_name, 0)

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
        # type: () -> Dict
        d = {}

        for month in self.months:
            d[month] = getattr(self, month)

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> Climate_MonthlyValueCollection
        obj = cls()

        for month in cls.months:
            setattr(obj, month, _input_dict.get(month))

        return obj


class Climate_PeakLoadCollection(_base._Base):
    """Collection class to organize peak load weather data"""

    def __init__(self):
        super(Climate_PeakLoadCollection, self).__init__()
        self.temp = 0
        self.rad_north = 0
        self.rad_east = 0
        self.rad_south = 0
        self.rad_west = 0
        self.rad_global = 0

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d['temp'] = self.temp
        d['rad_north'] = self.rad_north
        d['rad_east'] = self.rad_east
        d['rad_south'] = self.rad_south
        d['rad_west'] = self.rad_west
        d['rad_global'] = self.rad_global

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate_PeakLoadCollection
        new_obj = cls()

        new_obj.temp = _input_dict.get("temp")
        new_obj.rad_north = _input_dict.get("rad_north")
        new_obj.rad_east = _input_dict.get("rad_east")
        new_obj.rad_south = _input_dict.get("rad_south")
        new_obj.rad_west = _input_dict.get("rad_west")
        new_obj.rad_global = _input_dict.get("rad_global")

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
    def __init__(self):
        super(Climate, self).__init__()
        self.display_name = "New York"
        self.station_elevation = 0.0  # m
        self.summer_daily_temperature_swing = 8  # Deg K
        self.average_wind_speed = 4  # m/s

        self.ground = Climate_Ground()

        self.monthly_temperature_air = Climate_MonthlyValueCollection()
        self.monthly_temperature_dewpoint = Climate_MonthlyValueCollection()
        self.monthly_temperature_sky = Climate_MonthlyValueCollection()
        self.monthly_temperature_ground = Climate_MonthlyValueCollection()

        self.monthly_radiation_north = Climate_MonthlyValueCollection()
        self.monthly_radiation_east = Climate_MonthlyValueCollection()
        self.monthly_radiation_south = Climate_MonthlyValueCollection()
        self.monthly_radiation_west = Climate_MonthlyValueCollection()
        self.monthly_radiation_global = Climate_MonthlyValueCollection()

        self.peak_heating_1 = Climate_PeakLoadCollection()
        self.peak_heating_2 = Climate_PeakLoadCollection()
        self.peak_cooling_1 = Climate_PeakLoadCollection()
        self.peak_cooling_2 = Climate_PeakLoadCollection()

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["display_name"] = self.display_name
        d["station_elevation"] = self.station_elevation
        d["summer_daily_temperature_swing"] = self.summer_daily_temperature_swing
        d["average_wind_speed"] = self.average_wind_speed

        d["ground"] = self.ground.to_dict()

        d["monthly_temperature_air"] = self.monthly_temperature_air.to_dict()
        d["monthly_temperature_dewpoint"] = self.monthly_temperature_dewpoint.to_dict()
        d["monthly_temperature_sky"] = self.monthly_temperature_sky.to_dict()
        d["monthly_temperature_ground"] = self.monthly_temperature_ground.to_dict()

        d["monthly_radiation_north"] = self.monthly_radiation_north.to_dict()
        d["monthly_radiation_east"] = self.monthly_radiation_east.to_dict()
        d["monthly_radiation_south"] = self.monthly_radiation_south.to_dict()
        d["monthly_radiation_west"] = self.monthly_radiation_west.to_dict()
        d["monthly_radiation_global"] = self.monthly_radiation_global.to_dict()

        d["peak_heating_1"] = self.peak_heating_1.to_dict()
        d["peak_heating_2"] = self.peak_heating_2.to_dict()
        d["peak_cooling_1"] = self.peak_cooling_1.to_dict()
        d["peak_cooling_2"] = self.peak_cooling_2.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Climate
        new_obj = cls()

        new_obj.display_name = _input_dict.get("display_name")
        new_obj.station_elevation = _input_dict.get("station_elevation")
        new_obj.summer_daily_temperature_swing = _input_dict.get(
            "summer_daily_temperature_swing")
        new_obj.average_wind_speed = _input_dict.get("average_wind_speed")

        new_obj.ground = Climate_Ground.from_dict(
            _input_dict.get("ground", {}))

        new_obj.monthly_temperature_air = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_temperature_air", {})
        )
        new_obj.monthly_temperature_dewpoint = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_temperature_dewpoint", {})
        )
        new_obj.monthly_temperature_sky = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_temperature_sky", {})
        )
        new_obj.monthly_temperature_ground = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_temperature_ground", {})
        )

        new_obj.monthly_radiation_north = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_radiation_north", {})
        )
        new_obj.monthly_radiation_east = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_radiation_east", {})
        )
        new_obj.monthly_radiation_south = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_radiation_south", {})
        )
        new_obj.monthly_radiation_west = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_radiation_west", {})
        )
        new_obj.monthly_radiation_global = Climate_MonthlyValueCollection.from_dict(
            _input_dict.get("monthly_radiation_global", {})
        )

        new_obj.peak_heating_1 = Climate_PeakLoadCollection.from_dict(
            _input_dict.get("peak_heating_1", {}))
        new_obj.peak_heating_2 = Climate_PeakLoadCollection.from_dict(
            _input_dict.get("peak_heating_2", {}))
        new_obj.peak_cooling_1 = Climate_PeakLoadCollection.from_dict(
            _input_dict.get("peak_cooling_1", {}))
        new_obj.peak_cooling_2 = Climate_PeakLoadCollection.from_dict(
            _input_dict.get("peak_cooling_2", {}))

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

    def __init__(self):
        super(Location, self).__init__()
        # NYC Default
        self.latitude = 40.6
        self.longitude = -73.8
        self.site_elevation = None
        self.climate_zone = 1
        self.hours_from_UTC = -4

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["latitude"] = self.latitude
        d["longitude"] = self.longitude
        d["site_elevation"] = self.site_elevation
        d["climate_zone"] = self.climate_zone
        d["hours_from_UTC"] = self.hours_from_UTC

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> Location
        new_obj = cls()

        new_obj.latitude = _input_dict["latitude"]
        new_obj.longitude = _input_dict["longitude"]
        new_obj.site_elevation = _input_dict["site_elevation"]
        new_obj.climate_zone = _input_dict["climate_zone"]
        new_obj.hours_from_UTC = _input_dict["hours_from_UTC"]

        return new_obj

    def __copy__(self):
        # type: () -> Location
        obj = Location()

        obj.set_base_attrs_from_source(self)
        obj.latitude = self.latitude
        obj.longitude = self.longitude
        obj.site_elevation = self.site_elevation
        obj.climate_zone = self.climate_zone
        obj.hours_from_UTC = self.hours_from_UTC

        return obj

    def duplicate(self):
        # type: () -> Location
        return self.__copy__()


class PHPPCodes(_base._Base):
    """Settings / names if using Pre-loaded PHPP Library Data"""

    def __init__(self):
        super(PHPPCodes, self).__init__()
        # PHPP Specific settings
        self.country_code = "US-United States of America"
        self.region_code = "New York"
        self._dataset_name = "US0055b-New York"

    @property
    def dataset_name(self):
        return self._dataset_name

    @dataset_name.setter
    def dataset_name(self, _in):
        if _in is None:
            return

        vals = _in.split("-")
        if len(vals) != 2:
            raise Exception(
                "Error: PHPP Dataset name format should be "
                "'xx01234-xxxx'. Got: {}".format(self._dataset_name))
        self._dataset_name = _in
        self.display_name = vals[1]

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d["phpp_country_code"] = self.country_code
        d["phpp_region_code"] = self.region_code
        d["phpp_dataset_name"] = self.dataset_name

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PHPPCodes
        obj = cls()

        obj.country_code = _input_dict["phpp_country_code"]
        obj.region_code = _input_dict["phpp_region_code"]
        obj.dataset_name = _input_dict["phpp_dataset_name"]

        return obj

    def __copy__(self):
        # type: () -> PHPPCodes
        obj = PHPPCodes()

        obj.set_base_attrs_from_source(self)
        obj.country_code = self.country_code
        obj.region_code = self.region_code
        obj._dataset_name = self._dataset_name

        return obj

    def duplicate(self):
        # type: () -> PHPPCodes
        return self.__copy__()


class Site(_base._Base):
    """Location and Climate data for the building site."""

    def __init__(self):
        super(Site, self).__init__()
        self.location = Location()
        self.climate = Climate()
        self.phpp_library_codes = PHPPCodes()

    def to_dict(self):
        # type: () -> Dict
        d = {}

        d['location'] = self.location.to_dict()
        d['climate'] = self.climate.to_dict()
        d['phpp_library_codes'] = self.phpp_library_codes.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> Site
        obj = cls()

        obj.location = Location.from_dict(_input_dict['location'])
        obj.climate = Climate.from_dict(_input_dict['climate'])
        obj.phpp_library_codes = PHPPCodes.from_dict(_input_dict['phpp_library_codes'])

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
