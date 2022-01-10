# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive-House Style Monthly Climate Data"""

try:
    from itertools import izip as zip
except ImportError:
    pass  # Python3


class InvalidMonthlyDataError(Exception):
    def __init__(self, _in):
        self.message = "Error: Monthly data should be a collection of 12 numeric items.\n"\
            "Got {} of length: {}".format(_in, len(_in))
        super(InvalidMonthlyDataError, self).__init__(self.message)


class Climate_MonthlyValueCollection(object):
    """Collection class to organize monthly cliamte values"""

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
        for month_name in self.months:
            setattr(self, month_name, 0)

    @property
    def values(self):
        return [getattr(self, month) for month in self.months]

    @values.setter
    def values(self, _in):
        if (_in is None) or (len(_in) != 12):
            raise InvalidMonthlyDataError(_in)

        for val, month_name in zip(_in, self.months):
            setattr(self, month_name, val)

    def to_dict(self):
        # type: () -> dict
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

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Climate_PeakLoadCollection(object):
    """Collection class to orgaize peak load weather data"""

    def __init__(self):
        self.temp = 0
        self.rad_north = 0
        self.rad_east = 0
        self.rad_south = 0
        self.rad_west = 0
        self.rad_global = 0

    def to_dict(self):
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
        new_obj = cls()

        new_obj.temp = _input_dict.get("temp")
        new_obj.rad_north = _input_dict.get("rad_north")
        new_obj.rad_east = _input_dict.get("rad_east")
        new_obj.rad_south = _input_dict.get("rad_south")
        new_obj.rad_west = _input_dict.get("rad_west")
        new_obj.rad_global = _input_dict.get("rad_global")

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Climate_Location(object):
    def __init__(self):
        # NYC Default
        self.latitude = 40.6
        self.longitude = -73.8
        self.weather_station_elevation = 3.0
        self.climate_zone = 1
        self.hours_from_UTC = -4

    def to_dict(self):
        # type: () -> dict
        d = {}

        d["latitude"] = self.latitude
        d["longitude"] = self.longitude
        d["weather_station_elevation"] = self.weather_station_elevation
        d["climate_zone"] = self.climate_zone
        d["hours_from_UTC"] = self.hours_from_UTC

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> Climate_Location
        new_obj = cls()

        new_obj.latitude = _input_dict.get("latitude")
        new_obj.longitude = _input_dict.get("longitude")
        new_obj.weather_station_elevation = _input_dict.get("weather_station_elevation")
        new_obj.climate_zone = _input_dict.get("climate_zone")
        new_obj.hours_from_UTC = _input_dict.get("hours_from_UTC")

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Climate_Ground(object):
    def __init__(self):
        self.ground_thermal_conductivity = 2
        self.ground_heat_capacitiy = 1000
        self.ground_density = 2000
        self.depth_groundwater = 3
        self.flow_rate_groundwater = 0.05

    def to_dict(self):
        # type: () -> dict
        d = {}

        d["ground_thermal_conductivity"] = self.ground_thermal_conductivity
        d["ground_heat_capacitiy"] = self.ground_heat_capacitiy
        d["ground_density"] = self.ground_density
        d["depth_groundwater"] = self.depth_groundwater
        d["flow_rate_groundwater"] = self.flow_rate_groundwater

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.ground_thermal_conductivity = _input_dict.get(
            "ground_thermal_conductivity")
        new_obj.ground_heat_capacitiy = _input_dict.get("ground_heat_capacitiy")
        new_obj.ground_density = _input_dict.get("ground_density")
        new_obj.depth_groundwater = _input_dict.get("depth_groundwater")
        new_obj.flow_rate_groundwater = _input_dict.get("flow_rate_groundwater")

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Climate(object):
    def __init__(self):
        self.name = None
        self.summer_daily_temperature_swing = 8  # Deg K
        self.average_wind_speed = 4

        self.location = Climate_Location()
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
        self.peak_cooling = Climate_PeakLoadCollection()

    def to_dict(self):
        # type: () -> dict
        d = {}

        d["name"] = self.name
        d["summer_daily_temperature_swing"] = self.summer_daily_temperature_swing
        d["average_wind_speed"] = self.average_wind_speed

        d["location"] = self.location.to_dict()
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
        d["peak_cooling"] = self.peak_cooling.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.name = _input_dict.get("name")
        new_obj.summer_daily_temperature_swing = _input_dict.get(
            "summer_daily_temperature_swing")
        new_obj.average_wind_speed = _input_dict.get("average_wind_speed")

        new_obj.location = Climate_Location.from_dict(_input_dict.get("location", {}))
        new_obj.ground = Climate_Ground.from_dict(_input_dict.get("ground", {}))

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
        new_obj.peak_cooling = Climate_PeakLoadCollection.from_dict(
            _input_dict.get("peak_cooling", {}))

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
