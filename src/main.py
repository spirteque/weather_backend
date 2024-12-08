from typing import Annotated, Callable

from fastapi import Depends, FastAPI, Query, Request, Response, status
from fastapi.responses import JSONResponse

from .dependencies import get_forecast_service, get_week_summary_service
from .models import (
	WeatherForecast,
	WeatherForecastNotAvailableError,
	WeatherForecastService,
	WeatherWeekSummary,
	WeatherWeekSummaryNotAvailableError,
	WeatherWeekSummaryService,
)
from .settings import settings
from .utils import create_logger

app = FastAPI()
logger = create_logger(name='App')


@app.exception_handler(WeatherForecastNotAvailableError)
async def weather_forecast_not_available_error_handler(
		request: Request, error: WeatherForecastNotAvailableError
) -> JSONResponse:
	logger.error(error)
	status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

	return JSONResponse(status_code=status_code, content={"id": error.__class__.__name__})


@app.exception_handler(WeatherWeekSummaryNotAvailableError)
async def week_summary_not_available_error_handler(
		request: Request, error: WeatherWeekSummaryNotAvailableError
) -> JSONResponse:
	logger.error(error)
	status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

	return JSONResponse(status_code=status_code, content={"id": error.__class__.__name__})


@app.middleware("http")
async def log_request(request: Request, call_next: Callable) -> Response:
	logger.info(f"Request: {request.method} {request.url} {request.headers}")

	return await call_next(request)


@app.get('/api/v1/week_forecast')
def get_forecast(
		latitude: Annotated[float, Query(ge=settings.min_latitude, le=settings.max_latitude)],
		longitude: Annotated[float, Query(ge=settings.min_longitude, le=settings.max_longitude)],
		forecast_service: WeatherForecastService = Depends(get_forecast_service)
) -> WeatherForecast:
	return forecast_service.get_weather_forecast(latitude, longitude)


@app.get('/api/v1/week_summary')
def get_week_summary(
		latitude: Annotated[float, Query(ge=settings.min_latitude, le=settings.max_latitude)],
		longitude: Annotated[float, Query(ge=settings.min_longitude, le=settings.max_longitude)],
		week_summary_service: WeatherWeekSummaryService = Depends(get_week_summary_service)
) -> WeatherWeekSummary:
	return week_summary_service.get_week_summary(latitude, longitude)
