from src.models import WeatherForecastService, WeatherWeekSummaryService
from src.open_meteo.services import OpenMeteoForecastService, OpenMeteoWeekSummaryService
from src.settings import settings


def get_forecast_service() -> WeatherForecastService:
	return OpenMeteoForecastService(
		base_url=settings.open_meteo_base_url,
		installation_power_kw=settings.installation_power_kw,
		installation_efficiency=settings.installation_efficiency
	)


def get_week_summary_service() -> WeatherWeekSummaryService:
	return OpenMeteoWeekSummaryService(
		base_url=settings.open_meteo_base_url
	)
