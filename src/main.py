from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request, status
from fastapi.responses import JSONResponse

from .dependencies import get_forecast_service
from .models import WeatherForecast, WeatherForecastNotAvailableError, WeatherForecastService
from .settings import settings

app = FastAPI()


@app.exception_handler(WeatherForecastNotAvailableError)
async def weather_forecast_not_available_error_handler(
		request: Request, error: WeatherForecastNotAvailableError
) -> JSONResponse:
	status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

	return JSONResponse(status_code=status_code, content={"id": error.__class__.__name__})


@app.get('/')
def get_forecast(
		latitude: Annotated[float, Query(ge=settings.min_latitude, le=settings.max_latitude)],
		longitude: Annotated[float, Query(ge=settings.min_longitude, le=settings.max_longitude)],
		forecast_service: WeatherForecastService = Depends(get_forecast_service)
) -> WeatherForecast:

	forecast = forecast_service.get_weather_forecast(latitude, longitude)
	return forecast
