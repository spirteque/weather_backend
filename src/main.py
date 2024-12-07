from typing import Annotated

from fastapi import FastAPI, Query
import requests
from .open_meteo.models import OpenMeteoWeatherForecast
from .models import WeatherForecast, WeatherDay

from .settings import settings

app = FastAPI()

base_url = settings.open_meteo_base_url


@app.get('/')
def get_forecast(
		latitude: Annotated[float, Query(ge=settings.min_latitude, le=settings.max_latitude)],
		longitude: Annotated[float, Query(ge=settings.min_longitude, le=settings.max_longitude)]
):
	response_from_api = requests.get(
		f'{base_url}/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,sunshine_duration'
	)
	data = response_from_api.json()
	open_meteo_forecast = OpenMeteoWeatherForecast(**data)

	daily = open_meteo_forecast.daily

	zip_daily = zip(
		daily.time, daily.weather_code, daily.temperature_2m_max, daily.temperature_2m_min, daily.sunshine_duration
	)

	days = []
	for (time, code, t_max, t_min, sunshine) in zip_daily:
		days.append(WeatherDay(
			time=time,
			weather_code=code,
			temp_max=t_max,
			temp_min=t_min,
			sunshine_duration=sunshine,
			generated_energy=round(
				settings.installation_power_kw * (sunshine / 3600) * settings.installation_efficiency, 4
			)
		))

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
		installation_power=settings.installation_power_kw,
		installation_efficiency=settings.installation_efficiency,
		days=days
	)

	return forecast
