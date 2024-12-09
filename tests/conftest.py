from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.models import WeatherForecast, WeatherWeekSummary


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_forecast_service() -> MagicMock:
    service = MagicMock()
    service.get_weather_forecast.return_value = WeatherForecast(
        latitude=52.52,
        longitude=13.419998,
        time_unit="iso8601",
        weather_code_unit="wmo code",
        temp_max_unit="°C",
        temp_min_unit="°C",
        sunshine_duration_unit="s",
        generated_energy_unit="kWh",
        installation_power_unit="kW",
        installation_power=2.5,
        installation_efficiency=0.85,
        days=[]
    )
    return service


@pytest.fixture
def mock_week_summary_service() -> MagicMock:
    service = MagicMock()
    service.get_week_summary.return_value = WeatherWeekSummary(
        latitude=52.52,
        longitude=13.419998,
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
        weather_types=[]
    )
    return service
