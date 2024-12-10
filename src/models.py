from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel


# WeatherTypeEnum provides weather code string representation (e.g. from Open Meteo API)
class WeatherTypeEnum(Enum):
	CLEAR_SKY = 'CLEAR_SKY'
	CLOUDY = 'CLOUDY'
	FOG = 'FOG'
	DRIZZLE = 'DRIZZLE'
	FREEZING_DRIZZLE = 'FREEZING_DRIZZLE'
	RAIN = 'RAIN'
	FREEZING_RAIN = 'FREEZING_RAIN'
	SNOW = 'SNOW'
	SNOW_GRAINS = 'SNOW_GRAINS'
	RAIN_SHOWERS = 'RAIN_SHOWERS'
	SNOW_SHOWERS = 'SNOW_SHOWERS'
	THUNDERSTORM = 'THUNDERSTORM'
	THUNDERSTORM_WITH_HAIL = 'THUNDERSTORM_WITH_HAIL'


# DayEnum is used to map value to string day representation.
class DayEnum(Enum):
	MONDAY = "MONDAY"
	TUESDAY = "TUESDAY"
	WEDNESDAY = "WEDNESDAY"
	THURSDAY = "THURSDAY"
	FRIDAY = "FRIDAY"
	SATURDAY = "SATURDAY"
	SUNDAY = "SUNDAY"

	@staticmethod
	def get_by_index(i: int) -> str:
		for (day_index, day) in enumerate(DayEnum.__members__.keys()):
			if day_index == i:
				return day

		raise Exception("Couldn't resolve day!")


# Models representing returned data:
class WeatherDay(BaseModel):
	time: str
	day: DayEnum
	weather_code: int
	weather_type: WeatherTypeEnum
	temp_max: float
	temp_min: float
	sunshine_duration: float
	generated_energy: float


class WeatherForecast(BaseModel):
	latitude: float
	longitude: float
	time_unit: str
	weather_code_unit: str
	temp_max_unit: str
	temp_min_unit: str
	sunshine_duration_unit: str
	generated_energy_unit: str
	installation_power_unit: str
	installation_power: float
	installation_efficiency: float
	days: list[WeatherDay]


class WeatherWeekSummary(BaseModel):
	latitude: float
	longitude: float
	hourly_time_unit: str
	pressure_msl_unit: str
	daily_time_unit: str
	weather_code_unit: str
	temp_max_unit: str
	temp_min_unit: str
	sunshine_duration_unit: str
	mean_pressure: float
	mean_sunshine_duration: float
	temp_max_week: float
	temp_min_week: float
	# Very often only one weather type will be returned, but it would be nice to support
	# cases when some weather types are equal to each other.
	weather_types: list[WeatherTypeEnum] | None


# Interface used for future forecast services. As long as services have same structure,
# they can be exchanged independently without destroying the logic (e.g. when Open-Meteo suddenly becomes not free).
class WeatherForecastService(ABC):
	@abstractmethod
	def get_weather_forecast(self, latitude: float, longitude: float) -> WeatherForecast:
		pass


class WeatherWeekSummaryService(ABC):
	@abstractmethod
	def get_week_summary(self, latitude: float, longitude: float) -> WeatherWeekSummary:
		pass


# Interface used for cache functionality, e.g. Redis can be introduced without destroying the logic.
class CacheService(ABC):
	@abstractmethod
	def add_cache(self, cache_key: str, cache_value: BaseModel) -> None:
		pass

	@abstractmethod
	def get_cache(self, cache_key: str) -> BaseModel | None:
		pass


# Exception classes:
class WeatherForecastNotAvailableError(Exception):
	pass


class WeatherWeekSummaryNotAvailableError(Exception):
	pass
