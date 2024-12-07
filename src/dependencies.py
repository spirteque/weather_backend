from src.models import WeatherForecastService
from src.open_meteo.services import OpenMeteoForecastService
from src.settings import settings


def get_forecast_service() -> WeatherForecastService:
	return OpenMeteoForecastService(
		base_url=settings.open_meteo_base_url,
		installation_power_kw=settings.installation_power_kw,
		installation_efficiency=settings.installation_efficiency
	)
