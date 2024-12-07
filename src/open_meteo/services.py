import requests

from ..constants import GENERATED_ENERGY_DECIMAL_PART_LENGTH, HOUR_IN_SECONDS
from ..models import WeatherDay, WeatherForecast, WeatherForecastNotAvailableError, WeatherForecastService
from .models import OpenMeteoDaily, OpenMeteoWeatherForecast


class OpenMeteoForecastService(WeatherForecastService):
	base_url: str

	def __init__(self, base_url: str, installation_power_kw: float, installation_efficiency: float) -> None:
		self.base_url = base_url
		self.installation_power_kw = installation_power_kw
		self.installation_efficiency = installation_efficiency

	def get_weather_forecast(self, latitude: float, longitude: float) -> WeatherForecast:
		try:
			response = requests.get(
				f'{self.base_url}/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
			)

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
