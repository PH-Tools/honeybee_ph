# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Create Site | Climate Interface"""
try:
    from typing import List, Optional
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import site
from honeybee_ph_utils import units
from honeybee_ph_rhino.gh_compo_io import ghio_validators


class IClimateMonthlyTemps(object):
    """Interface for Climate Monthly Temperature Component."""

    def __init__(self, _air_temps, _dewpoints, _sky_temps, _ground_temps):
        # type: (List[float], List[float], List[float], List[float]) -> None
        self.air_temps = _air_temps
        self.dewpoints = _dewpoints
        self.sky_temps = _sky_temps
        self.ground_temps = _ground_temps

    def _validate(self, _input_list):
        # type: (List[float]) -> List[float]
        """Validate that the input data is the right shape."""
        if not _input_list:
            return [0.0]*12

        if len(_input_list) != 12:
            msg = "Error: Monthly data should be a collection of 12 numeric items.\n"\
                  "Got a {} of length: {}?".format(type(_input_list), len(_input_list))
            raise Exception(msg)

        return _input_list

    def _build_data(self, _input_list):
        # type: (List[float]) -> List[float]
        """Clean and convert the input data (if needed)."""
        _ = []
        for t in self._validate(_input_list):
            input_value, input_units = units.parse_input(str(t))
            result = units.convert(input_value, input_units or "C", "C")
            _.append(result)
        return _

    @property
    def air_temps(self):
        # type: () -> List[float]
        return self._air_temps

    @air_temps.setter
    def air_temps(self, _air_temps):
        # type: (List[float]) -> None
        self._air_temps = self._build_data(_air_temps)

    @property
    def dewpoints(self):
        return self._dewpoints

    @dewpoints.setter
    def dewpoints(self, _dewpoints):
        # type: (List[float]) -> None
        self._dewpoints = self._build_data(_dewpoints)

    @property
    def sky_temps(self):
        return self._sky_temps

    @sky_temps.setter
    def sky_temps(self, _sky_temps):
        # type: (List[float]) -> None
        self._sky_temps = self._build_data(_sky_temps)

    @property
    def ground_temps(self):
        return self._ground_temps

    @ground_temps.setter
    def ground_temps(self, _ground_temps):
        # type: (List[float]) -> None
        self._ground_temps = self._build_data(_ground_temps)

    def create_hbph_obj(self):
        # type: () -> site.Climate_MonthlyTempCollection
        return site.Climate_MonthlyTempCollection(
            _air=site.Climate_MonthlyValueSet(self.air_temps),
            _dewpoint=site.Climate_MonthlyValueSet(self.dewpoints),
            _sky=site.Climate_MonthlyValueSet(self.sky_temps),
            _ground=site.Climate_MonthlyValueSet(self.ground_temps),
        )


class IClimateMonthlyRadiation(object):
    """Interface for Climate Monthly Radiation Component."""

    def __init__(self, _north, _east, _south, _west, _glob):
        # type: (List[float], List[float], List[float], List[float], List[float]) -> None
        self.north = _north
        self.east = _east
        self.south = _south
        self.west = _west
        self.glob = _glob

    def _validate(self, _input_list):
        # type: (List[float]) -> List[float]
        """Validate that the input data is the right shape."""
        if not _input_list:
            return [0.0]*12

        if len(_input_list) != 12:
            msg = "Error: Monthly data should be a collection of 12 numeric items.\n"\
                  "Got a {} of length: {}?".format(type(_input_list), len(_input_list))
            raise Exception(msg)

        return _input_list

    def _build_data(self, _input_list):
        # type: (List[float]) -> List[float]
        """Clean and convert the input data (if needed)."""
        _ = []
        for t in self._validate(_input_list):
            input_value, input_units = units.parse_input(str(t))
            result = units.convert(input_value, input_units or "KWH/M2", "KWH/M2")
            _.append(result)
        return _

    @property
    def north(self):
        return self._north

    @north.setter
    def north(self, _north):
        # type: (List[float]) -> None
        self._north = self._build_data(_north)

    @property
    def east(self):
        return self._east

    @east.setter
    def east(self, _east):
        # type: (List[float]) -> None
        self._east = self._build_data(_east)

    @property
    def south(self):
        return self._south

    @south.setter
    def south(self, _south):
        # type: (List[float]) -> None
        self._south = self._build_data(_south)

    @property
    def west(self):
        return self._west

    @west.setter
    def west(self, _west):
        # type: (List[float]) -> None
        self._west = self._build_data(_west)

    @property
    def glob(self):
        return self._glob

    @glob.setter
    def glob(self, _glob):
        # type: (List[float]) -> None
        self._glob = self._build_data(_glob)

    def create_hbph_obj(self):
        # type: () -> site.Climate_MonthlyRadiationCollection
        return site.Climate_MonthlyRadiationCollection(
            _north=site.Climate_MonthlyValueSet(self.north),
            _east=site.Climate_MonthlyValueSet(self.east),
            _south=site.Climate_MonthlyValueSet(self.south),
            _west=site.Climate_MonthlyValueSet(self.west),
            _glob=site.Climate_MonthlyValueSet(self.glob),
        )


class IClimate_PeakLoad(object):
    """Interface for a single Peak Load data Component."""

    display_name = ghio_validators.HBName("display_name")
    temp = ghio_validators.UnitDegreeC("temp", default=0.0)
    rad_north = ghio_validators.UnitKWH_M2("rad_north", default=0.0)
    rad_east = ghio_validators.UnitKWH_M2("rad_east", default=0.0)
    rad_south = ghio_validators.UnitKWH_M2("rad_south", default=0.0)
    rad_west = ghio_validators.UnitKWH_M2("rad_west", default=0.0)
    rad_global = ghio_validators.UnitKWH_M2("rad_global", default=0.0)
    dewpoint_temp = ghio_validators.UnitDegreeC("dewpoint_temp")
    ground_temp = ghio_validators.UnitDegreeC("ground_temp")
    sky_temp = ghio_validators.UnitDegreeC("sky_temp")

    def __init__(self,
                 _display_name,
                 _temp,
                 _rad_north,
                 _rad_east,
                 _rad_south,
                 _rad_west,
                 _rad_global,
                 _dewpoint_temp,
                 _ground_temp,
                 _sky_temp,):
        # type: (str, float, float, float, float, float, float, Optional[float], Optional[float], Optional[float]) -> None
        self.display_name = _display_name
        self.temp = _temp
        self.rad_north = _rad_north
        self.rad_east = _rad_east
        self.rad_south = _rad_south
        self.rad_west = _rad_west
        self.rad_global = _rad_global
        self.dewpoint = _dewpoint_temp
        self.ground_temp = _ground_temp
        self.sky_temp = _sky_temp

    def create_hbph_obj(self):
        # type: () -> site.Climate_PeakLoadValueSet
        hbph_obj = site.Climate_PeakLoadValueSet(
            self.temp,
            self.rad_north,
            self.rad_east,
            self.rad_south,
            self.rad_west,
            self.rad_global,
            self.dewpoint,
            self.ground_temp,
            self.sky_temp,
        )
        hbph_obj.display_name = self.display_name

        return hbph_obj


class IClimate_PeakLoads(object):
    """Interface for the Peak Loads Collection."""

    def __init__(self, _peak_heat_load_1, _peak_heat_load_2, _peak_cooling_load_1, _peak_cooling_load_2):
        # type: (site.Climate_PeakLoadValueSet, site.Climate_PeakLoadValueSet, site.Climate_PeakLoadValueSet, site.Climate_PeakLoadValueSet) -> None
        self.heat_load_1 = _peak_heat_load_1 or site.Climate_PeakLoadValueSet()
        self.heat_load_2 = _peak_heat_load_2 or site.Climate_PeakLoadValueSet()
        self.cooling_load_1 = _peak_cooling_load_1 or site.Climate_PeakLoadValueSet()
        self.cooling_load_2 = _peak_cooling_load_2 or site.Climate_PeakLoadValueSet()

    def create_hbph_obj(self):
        # type: () -> site.Climate_PeakLoadCollection
        hbph_obj = site.Climate_PeakLoadCollection(
            self.heat_load_1,
            self.heat_load_2,
            self.cooling_load_1,
            self.cooling_load_2
        )

        return hbph_obj


class IClimate(object):
    """Interface for Climate Component."""

    display_name = ghio_validators.HBName("display_name", default="New York")
    station_elevation = ghio_validators.UnitM("station_elevation", default=0.0)
    daily_temp_swing = ghio_validators.UnitDeltaC("daily_temp_swing", default=8.0)
    average_wind_speed = ghio_validators.UnitMeterPerSecond(
        "average_wind_speed", default=4.0)

    def __init__(self,
                 _display_name,
                 _station_elevation,
                 _daily_temp_swing,
                 _average_wind_speed,
                 _monthly_temps=site.Climate_MonthlyTempCollection(),
                 _monthly_radiation=site.Climate_MonthlyRadiationCollection(),
                 _peak_loads=site.Climate_PeakLoadCollection(),
                 ):
        # type: (str, float, float, float, site.Climate_MonthlyTempCollection, site.Climate_MonthlyRadiationCollection, site.Climate_PeakLoadCollection) -> None
        self.display_name = _display_name
        self.station_elevation = _station_elevation
        self.daily_temp_swing = _daily_temp_swing
        self.average_wind_speed = _average_wind_speed
        self.monthly_temps = _monthly_temps or site.Climate_MonthlyTempCollection()
        self.monthly_radiation = _monthly_radiation or site.Climate_MonthlyRadiationCollection()
        self.peak_loads = _peak_loads or site.Climate_PeakLoadCollection()

    def create_hbph_obj(self):
        # type: () -> site.Climate

        hbph_climate = site.Climate(
            _display_name=self.display_name,
            _station_elevation=self.station_elevation,
            _daily_temp_swing=self.daily_temp_swing,
            _average_wind_speed=self.average_wind_speed,
            _monthly_temps=self.monthly_temps,
            _monthly_radiation=self.monthly_radiation,
            _peak_loads=self.peak_loads,
        )

        return hbph_climate


class ILocation(object):
    """Interface for the Location Component."""
    display_name = ghio_validators.HBName("display_name", default="New York")
    site_elevation = ghio_validators.UnitM("site_elevation", default=0.0)

    def __init__(self,
                 _display_name,
                 _latitude,
                 _longitude,
                 _site_elevation,
                 _climate_zone,
                 _hours_from_UTC,
                 ):
        # type: (str, float, float, Optional[float], int, int) -> None
        self.display_name = _display_name or "New York"
        self.latitude = _latitude or 40.6
        self.longitude = _longitude or -73.8
        self.site_elevation = _site_elevation or None
        self.climate_zone = _climate_zone or 1
        self.hours_from_UTC = _hours_from_UTC or -4

    def create_hbph_obj(self):
        hbph_obj = site.Location(
            self.latitude,
            self.longitude,
            self.site_elevation,
            self.climate_zone,
            self.hours_from_UTC,
        )
        hbph_obj.display_name = self.display_name

        return hbph_obj


class ISite(object):

    def __init__(self):
        raise NotImplementedError("TODO")
