from fastapi import Depends

from src.models import CacheService, WeatherForecastService, WeatherWeekSummaryService
from src.open_meteo.services import OpenMeteoForecastService, OpenMeteoWeekSummaryService
from src.services import DailyCacheService
from src.settings import settings


def get_cache_service() -> CacheService:
	return DailyCacheService()


def get_forecast_service(
		cache_service: CacheService = Depends(get_cache_service)
) -> WeatherForecastService:
	return OpenMeteoForecastService(
		base_url=settings.open_meteo_base_url,
		installation_power_kw=settings.installation_power_kw,
		installation_efficiency=settings.installation_efficiency,
		cache_service=cache_service
	)


def get_week_summary_service(
		cache_service: CacheService = Depends(get_cache_service)
) -> WeatherWeekSummaryService:
	return OpenMeteoWeekSummaryService(
		base_url=settings.open_meteo_base_url,
		cache_service=cache_service
	)
