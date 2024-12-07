from typing import Annotated

from fastapi import Depends, FastAPI, Query

from .dependencies import get_forecast_service
from .models import WeatherForecast, WeatherForecastService
from .settings import settings

app = FastAPI()

base_url = settings.open_meteo_base_url


@app.get('/')
def get_forecast(
		latitude: Annotated[float, Query(ge=settings.min_latitude, le=settings.max_latitude)],
		longitude: Annotated[float, Query(ge=settings.min_longitude, le=settings.max_longitude)],
		forecast_service: WeatherForecastService = Depends(get_forecast_service)
) -> WeatherForecast:

	forecast = forecast_service.get_weather_forecast(latitude, longitude)
	return forecast
