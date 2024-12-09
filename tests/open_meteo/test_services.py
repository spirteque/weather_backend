from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time

from src.models import (
	CacheService,
	DayEnum,
	WeatherDay,
	WeatherForecast,
	WeatherForecastNotAvailableError,
	WeatherTypeEnum,
	WeatherWeekSummary,
	WeatherWeekSummaryNotAvailableError,
)
from src.open_meteo.models import OpenMeteoDaily, OpenMeteoWeatherCodeEnum
from src.open_meteo.services import OpenMeteoForecastService, OpenMeteoWeekSummaryService


class TestOpenMeteoForecastService:
	base_url = 'http://example.com'
	installation_power_kw = 2.5
	installation_efficiency = 0.2
	latitude = 52.52
	longitude = 13.419998

	def create_service(self, cache_service: CacheService) -> OpenMeteoForecastService:
		return OpenMeteoForecastService(
			base_url=self.base_url,
			installation_power_kw=self.installation_power_kw,
			installation_efficiency=self.installation_efficiency,
			cache_service=cache_service
		)

	@freeze_time('2024-12-08')
	@patch('requests.get')
	def test_get_weather_forecast_success(
			self, mock_get: MagicMock, cache_service: CacheService, open_meteo_forecast_response: dict
	) -> None:
		open_meteo_forecast_service = self.create_service(cache_service)

		mock_get.return_value.status_code = 200
		mock_get.return_value.json.return_value = open_meteo_forecast_response

		actual = open_meteo_forecast_service.get_weather_forecast(self.latitude, self.longitude)

		mock_get.assert_called_once_with(
			f'{self.base_url}/v1/forecast',
			params={
				'latitude': self.latitude,
				'longitude': self.longitude,
				'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
			}
		)

		assert isinstance(actual, WeatherForecast)
		assert isinstance(actual.days[0], WeatherDay)
		assert actual.installation_power == self.installation_power_kw
		assert actual.installation_power_unit is not None
		assert actual.installation_efficiency == self.installation_efficiency
		assert len(actual.days) == len(open_meteo_forecast_response['daily']['time'])

		cache_key = f'forecast_{self.latitude}_{self.longitude}'
		date_key = str(datetime.now().date())
		assert cache_key in cache_service.cache[date_key]
		assert cache_service.cache[date_key][cache_key] == actual

	@pytest.mark.parametrize(
		'status_code, exception_message',
		[
			(500, 'Invalid response'),
			(400, 'Invalid response')
		]
	)
	@patch('requests.get')
	def test_get_weather_forecast_api_error(
			self, mock_get: MagicMock, cache_service: CacheService, status_code: int, exception_message: str
	) -> None:
		open_meteo_forecast_service = self.create_service(cache_service)

		mock_get.return_value.status_code = status_code
		mock_get.return_value.json.side_effect = ValueError(exception_message)

		with pytest.raises(WeatherForecastNotAvailableError) as exc_info:
			open_meteo_forecast_service.get_weather_forecast(self.latitude, self.longitude)

		assert "Invalid response" in str(exc_info.value)

	@freeze_time("2024-12-08")
	@patch('requests.get')
	def test_get_weather_forecast_from_cache(
			self, mock_get: MagicMock, cache_service: CacheService, open_meteo_forecast_response: dict
	) -> None:
		open_meteo_forecast_service = self.create_service(cache_service)
		cache_key = f"forecast_{self.latitude}_{self.longitude}"
		date_key = str(datetime.now().date())

		expected_forecast = WeatherForecast(
			latitude=self.latitude,
			longitude=self.longitude,
			time_unit="iso8601",
			weather_code_unit="wmo code",
			temp_max_unit="°C",
			temp_min_unit="°C",
			sunshine_duration_unit="s",
			generated_energy_unit="kWh",
			installation_power_unit="kW",
			installation_power=2.5,
			installation_efficiency=0.2,
			days=[]
		)

		cache_service.cache[date_key] = {cache_key: expected_forecast}

		actual = open_meteo_forecast_service.get_weather_forecast(self.latitude, self.longitude)

		mock_get.assert_not_called()
		assert actual == expected_forecast

	@patch('requests.get')
	def test_get_weather_forecast_connection_error(self, mock_get: MagicMock, cache_service: CacheService) -> None:
		open_meteo_forecast_service = self.create_service(cache_service)

		mock_get.side_effect = ConnectionError("API not reachable")

		with pytest.raises(WeatherForecastNotAvailableError) as exc_info:
			open_meteo_forecast_service.get_weather_forecast(self.latitude, self.longitude)

		assert "API not reachable" in str(exc_info.value)

	def test_get_days(self) -> None:
		service = self.create_service(None)
		daily = OpenMeteoDaily(
			time=["2024-12-08", "2024-12-09"],
			weather_code=[1, 2],
			temperature_2m_max=[10.0, 12.0],
			temperature_2m_min=[5.0, 6.0],
			sunshine_duration=[3600, 7200]
		)

		days = service._get_days(daily)

		assert len(days) == 2
		assert days[0].time == "2024-12-08"
		assert days[0].generated_energy > 0

	def test_get_day(self) -> None:
		assert OpenMeteoForecastService._get_day("2024-12-08") == DayEnum.SUNDAY.value
		assert OpenMeteoForecastService._get_day("2024-12-09") == DayEnum.MONDAY.value

	def test_calculate_energy(self) -> None:
		service = self.create_service(None)
		energy = service._calculate_energy(7200)
		expected_energy = round(
			service.installation_power_kw * (7200 / 3600) * service.installation_efficiency,
			2
		)

		assert energy == expected_energy


class TestOpenMeteoWeekSummaryService:
	base_url = 'http://example.com'
	latitude = 52.52
	longitude = 13.419998

	def create_service(self, cache_service: CacheService) -> OpenMeteoWeekSummaryService:
		return OpenMeteoWeekSummaryService(
			base_url=self.base_url,
			cache_service=cache_service
		)

	def create_expected_summary(self) -> WeatherWeekSummary:
		return WeatherWeekSummary(
			latitude=self.latitude,
			longitude=self.longitude,
			hourly_time_unit="iso8601",
			pressure_msl_unit="hPa",
			daily_time_unit="iso8601",
			weather_code_unit="wmo code",
			temp_max_unit="°C",
			temp_min_unit="°C",
			sunshine_duration_unit="s",
			mean_pressure=1020.5,
			mean_sunshine_duration=5.67,
			temp_max_week=4.7,
			temp_min_week=-2.4,
			weather_types=[WeatherTypeEnum.RAIN]
		)

	def setup_cache(self, cache_service: CacheService, expected_summary: WeatherWeekSummary) -> (str, str):
		cache_key = f'summary_{self.latitude}_{self.longitude}'
		date_key = str(datetime.now().date())
		cache_service.cache[date_key] = {cache_key: expected_summary}
		return cache_key, date_key

	@patch('requests.get')
	def test_get_week_summary_success(
			self, mock_get: MagicMock, cache_service: CacheService, open_meteo_week_summary_response: dict
	) -> None:
		open_meteo_week_summary_service = self.create_service(cache_service)

		mock_get.return_value.status_code = 200
		mock_get.return_value.json.return_value = open_meteo_week_summary_response

		summary = open_meteo_week_summary_service.get_week_summary(self.latitude, self.longitude)

		mock_get.assert_called_once_with(
			f'{self.base_url}/v1/forecast',
			params={
				'latitude': self.latitude,
				'longitude': self.longitude,
				'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration',
				'hourly': 'pressure_msl'
			}
		)

		assert isinstance(summary, WeatherWeekSummary)

		open_meteo_pressure_data = open_meteo_week_summary_response['hourly']['pressure_msl']
		expected_mean_pressure = round(sum(open_meteo_pressure_data) / len(open_meteo_pressure_data), 1)
		assert summary.mean_pressure == expected_mean_pressure

		open_meteo_sunshine_data = open_meteo_week_summary_response['daily']['sunshine_duration']
		expected_mean_sunshine_duration = round(sum(open_meteo_sunshine_data) / len(open_meteo_sunshine_data), 2)
		assert summary.mean_sunshine_duration == expected_mean_sunshine_duration

		assert summary.temp_max_week == max(open_meteo_week_summary_response['daily']['temperature_2m_max'])
		assert summary.temp_min_week == min(open_meteo_week_summary_response['daily']['temperature_2m_min'])

		expected_weather_types = {WeatherTypeEnum.RAIN, WeatherTypeEnum.CLOUDY, WeatherTypeEnum.SNOW}
		assert set(summary.weather_types) == expected_weather_types
		assert isinstance(summary.weather_types, list)

		cache_key, date_key = self.setup_cache(cache_service, summary)
		assert cache_key in cache_service.cache[date_key]
		assert cache_service.cache[date_key][cache_key] == summary

	@freeze_time("2024-12-09")
	@patch('requests.get')
	def test_get_week_summary_from_cache(
			self, mock_get: MagicMock, cache_service: CacheService, open_meteo_week_summary_response: dict
	) -> None:
		open_meteo_week_summary_service = self.create_service(cache_service)
		expected_summary = self.create_expected_summary()
		cache_key, date_key = self.setup_cache(cache_service, expected_summary)
		cache_service.cache[date_key] = {cache_key: expected_summary}

		summary = open_meteo_week_summary_service.get_week_summary(self.latitude, self.longitude)

		mock_get.assert_not_called()
		assert summary == expected_summary
		assert cache_service.cache[date_key][cache_key] == expected_summary

	@patch('requests.get')
	def test_get_week_summary_no_cache_and_api_unreachable(
			self, mock_get: MagicMock, cache_service: CacheService
	) -> None:
		open_meteo_week_summary_service = self.create_service(cache_service)

		mock_get.side_effect = ConnectionError("API not reachable")

		with pytest.raises(WeatherWeekSummaryNotAvailableError) as exc_info:
			open_meteo_week_summary_service.get_week_summary(self.latitude, self.longitude)

		assert "API not reachable" in str(exc_info.value)

	def test_get_weather_types_success(self) -> None:
		weather_codes = [
			OpenMeteoWeatherCodeEnum.SNOW_SLIGHT,
			OpenMeteoWeatherCodeEnum.RAIN_MODERATE,
			OpenMeteoWeatherCodeEnum.SNOW_MODERATE,
			OpenMeteoWeatherCodeEnum.SNOW_HEAVY
		]

		grouped_weather = OpenMeteoWeekSummaryService._get_weather_types(weather_codes)

		assert grouped_weather == [WeatherTypeEnum.SNOW]

	def test_get_weather_types_multiple_types(self) -> None:
		weather_codes = [
			OpenMeteoWeatherCodeEnum.RAIN_SLIGHT,
			OpenMeteoWeatherCodeEnum.RAIN_SLIGHT,
			OpenMeteoWeatherCodeEnum.SNOW_SLIGHT,
			OpenMeteoWeatherCodeEnum.SNOW_SLIGHT
		]

		grouped_weather = OpenMeteoWeekSummaryService._get_weather_types(weather_codes)

		assert set(grouped_weather) == {WeatherTypeEnum.RAIN, WeatherTypeEnum.SNOW}

	def test_get_weather_types_empty_list_error(self) -> None:
		with pytest.raises(ValueError):
			OpenMeteoWeekSummaryService._get_weather_types([])

	def test_get_weather_types_list_with_invalid_values_error(self) -> None:
		with pytest.raises(Exception):
			OpenMeteoWeekSummaryService._get_weather_types([1, 'a'])
