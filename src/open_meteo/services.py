from collections import Counter
from statistics import mean

import requests

from ..constants import (
	GENERATED_ENERGY_DECIMAL_PART_LENGTH,
	HOUR_IN_SECONDS,
	MEAN_PRESSURE_DECIMAL_PART_LENGTH,
	MEAN_SUNSHINE_DURATION_DECIMAL_PART_LENGTH,
)
from ..models import (
	WeatherDay,
	WeatherForecast,
	WeatherForecastNotAvailableError,
	WeatherForecastService,
	WeatherTypeEnum,
	WeatherWeekSummary,
	WeatherWeekSummaryNotAvailableError,
	WeatherWeekSummaryService, CacheService,
)
from ..utils import create_logger
from .models import (
	OpenMeteoDaily,
	OpenMeteoGroupedWeatherCodeEnum,
	OpenMeteoWeatherCodeEnum,
	OpenMeteoWeatherForecast,
	OpenMeteoWeatherWeekSummary,
)

logger = create_logger('OpenMeteoForecastService')


class OpenMeteoForecastService(WeatherForecastService):
	base_url: str
	installation_power_kw: float
	installation_efficiency: float
	cache_service: CacheService

	def __init__(
			self,
			base_url: str,
			installation_power_kw: float,
			installation_efficiency: float,
			cache_service: CacheService
	) -> None:
		self.base_url = base_url
		self.installation_power_kw = installation_power_kw
		self.installation_efficiency = installation_efficiency
		self.cache_service = cache_service

	@staticmethod
	def _create_cash_key(latitude: float, longitude: float) -> str:
		return f'forecast_{latitude}_{longitude}'

	def get_weather_forecast(self, latitude: float, longitude: float) -> WeatherForecast:
		url = f'{self.base_url}/v1/forecast'
		params = {
			'latitude': latitude,
			'longitude': longitude,
			'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
		}

		try:
			cache_key = OpenMeteoForecastService._create_cash_key(latitude, longitude)

			if cached_forecast := self.cache_service.get_cache(cache_key=cache_key):
				return cached_forecast

			logger.info(f'Fetching {url} {params}')

			response = requests.get(url, params=params)

			logger.info('Fetched forecast.')

			open_meteo_forecast = OpenMeteoWeatherForecast(**response.json())

			forecast = WeatherForecast(
				latitude=open_meteo_forecast.latitude,
				longitude=open_meteo_forecast.longitude,
				time_unit=open_meteo_forecast.daily_units.time,
				weather_code_unit=open_meteo_forecast.daily_units.weather_code,
				temp_max_unit=open_meteo_forecast.daily_units.temperature_2m_max,
				temp_min_unit=open_meteo_forecast.daily_units.temperature_2m_min,
				sunshine_duration_unit=open_meteo_forecast.daily_units.sunshine_duration,
				generated_energy_unit='kWh',
				installation_power_unit='kW',
				installation_power=self.installation_power_kw,
				installation_efficiency=self.installation_efficiency,
				days=self._get_days(open_meteo_forecast.daily)
			)

			self.cache_service.add_cache(cache_key=cache_key, cache_value=forecast)

			return forecast

		except Exception as e:
			raise WeatherForecastNotAvailableError(e)

	def _get_days(self, daily: OpenMeteoDaily) -> list[WeatherDay]:
		grouped_days = zip(
			daily.time,
			daily.weather_code,
			daily.temperature_2m_max,
			daily.temperature_2m_min,
			daily.sunshine_duration
		)

		return [
			WeatherDay(
				time=time,
				weather_code=code,
				weather_type=OpenMeteoGroupedWeatherCodeEnum.create_from_weather_code(code).to_weather_type(),
				temp_max=t_max,
				temp_min=t_min,
				sunshine_duration=sunshine,
				generated_energy=self._calculate_energy(sunshine)
			)
			for (time, code, t_max, t_min, sunshine) in grouped_days
		]

	def _calculate_energy(self, sunshine_duration: float) -> float:
		return round(
			self.installation_power_kw * (sunshine_duration / HOUR_IN_SECONDS) * self.installation_efficiency,
			GENERATED_ENERGY_DECIMAL_PART_LENGTH
		)


class OpenMeteoWeekSummaryService(WeatherWeekSummaryService):
	base_url: str
	cache_service: CacheService

	def __init__(self, base_url: str, cache_service: CacheService) -> None:
		self.base_url = base_url
		self.cache_service = cache_service

	@staticmethod
	def _create_cash_key(latitude: float, longitude: float) -> str:
		return f'summary_{latitude}_{longitude}'

	def get_week_summary(self, latitude: float, longitude: float) -> WeatherWeekSummary:
		url = f'{self.base_url}/v1/forecast'
		params = {
			'latitude': latitude,
			'longitude': longitude,
			'hourly': 'pressure_msl',
			'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
		}

		try:
			cache_key = OpenMeteoWeekSummaryService._create_cash_key(latitude, longitude)

			if cached_summary := self.cache_service.get_cache(cache_key=cache_key):
				return cached_summary

			logger.info(f'Fetching {url} {params}')

			response = requests.get(url, params=params)
			logger.info('Fetched week summary.')

			open_meteo_summary = OpenMeteoWeatherWeekSummary(**response.json())

			summary = WeatherWeekSummary(
				latitude=open_meteo_summary.latitude,
				longitude=open_meteo_summary.longitude,
				hourly_time_unit=open_meteo_summary.hourly_units.time,
				pressure_msl_unit=open_meteo_summary.hourly_units.pressure_msl,
				daily_time_unit=open_meteo_summary.daily_units.time,
				weather_code_unit=open_meteo_summary.daily_units.weather_code,
				temp_max_unit=open_meteo_summary.daily_units.temperature_2m_max,
				temp_min_unit=open_meteo_summary.daily_units.temperature_2m_min,
				sunshine_duration_unit=open_meteo_summary.daily_units.sunshine_duration,
				mean_pressure=OpenMeteoWeekSummaryService._get_mean_pressure(open_meteo_summary.hourly.pressure_msl),
				mean_sunshine_duration=OpenMeteoWeekSummaryService._get_mean_sunshine_duration(
					open_meteo_summary.daily.sunshine_duration
				),
				temp_max_week=OpenMeteoWeekSummaryService._get_max_temp(open_meteo_summary.daily.temperature_2m_max),
				temp_min_week=OpenMeteoWeekSummaryService._get_min_temp(open_meteo_summary.daily.temperature_2m_min),
				weather_types=OpenMeteoWeekSummaryService._get_weather_types(open_meteo_summary.daily.weather_code)
			)

			self.cache_service.add_cache(cache_key=cache_key, cache_value=summary)

			return summary

		except Exception as e:
			raise WeatherWeekSummaryNotAvailableError(e)

	@staticmethod
	def _get_mean_pressure(pressures: list[float]) -> float:
		return round(mean(pressures), MEAN_PRESSURE_DECIMAL_PART_LENGTH)

	@staticmethod
	def _get_mean_sunshine_duration(sunshine_durations: list[float]) -> float:
		return round(mean(sunshine_durations), MEAN_SUNSHINE_DURATION_DECIMAL_PART_LENGTH)

	@staticmethod
	def _get_max_temp(max_temps: list[float]) -> float:
		return max(max_temps)

	@staticmethod
	def _get_min_temp(min_temps: list[float]) -> float:
		return max(min_temps)

	@staticmethod
	def _get_weather_types(weather_codes: list[OpenMeteoWeatherCodeEnum]) -> list[WeatherTypeEnum]:
		grouped = []

		for code in weather_codes:
			grouped.append(OpenMeteoGroupedWeatherCodeEnum.create_from_weather_code(code))

		counter = Counter(grouped)
		max_count = max(counter.values())

		return [k.to_weather_type() for k, c in counter.items() if c == max_count]
