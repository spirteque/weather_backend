from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.dependencies import get_forecast_service, get_week_summary_service
from src.main import app
from src.models import WeatherForecastNotAvailableError, WeatherWeekSummaryNotAvailableError


class TestGetForecast:
    def test_get_forecast_success(self, client: TestClient, mock_forecast_service: MagicMock) -> None:
        app.dependency_overrides[get_forecast_service] = lambda: mock_forecast_service

        response = client.get('/api/v1/week_forecast', params={'latitude': 52.52, 'longitude': 13.419998})

        assert response.status_code == 200

        data = response.json()
        assert data['latitude'] == 52.52
        assert data['longitude'] == 13.419998

        app.dependency_overrides.clear()

    def test_get_forecast_invalid_latitude_error(self, client: TestClient, mock_forecast_service: MagicMock) -> None:
        app.dependency_overrides[get_forecast_service] = lambda: mock_forecast_service

        response = client.get('/api/v1/week_forecast', params={'latitude': 100, 'longitude': 13.419998})

        assert response.status_code == 422

        error = response.json()
        assert 'detail' in error
        assert 'type' in error['detail'][0]
        assert error['detail'][0]['loc'] == ['query', 'latitude']

        app.dependency_overrides.clear()

    def test_get_forecast_invalid_longitude_error(self, client: TestClient, mock_forecast_service: MagicMock) -> None:
        app.dependency_overrides[get_forecast_service] = lambda: mock_forecast_service

        response = client.get('/api/v1/week_forecast', params={'latitude': 52.52, 'longitude': 200})

        assert response.status_code == 422

        error = response.json()
        assert 'detail' in error
        assert 'type' in error['detail'][0]
        assert error['detail'][0]['loc'] == ['query', 'longitude']

        app.dependency_overrides.clear()

    def test_get_forecast_missing_parameters_error(self, client: TestClient, mock_forecast_service: MagicMock) -> None:
        app.dependency_overrides[get_forecast_service] = lambda: mock_forecast_service

        response = client.get('/api/v1/week_forecast/')

        assert response.status_code == 422

        error = response.json()

        assert len(error['detail']) == 2

        missing_params = [err['loc'][-1] for err in error['detail']]
        assert 'latitude' in missing_params
        assert 'longitude' in missing_params

        app.dependency_overrides.clear()


class TestGetWeekSummary:
    def test_get_week_summary_success(self, client: TestClient, mock_week_summary_service: MagicMock) -> None:
        app.dependency_overrides[get_week_summary_service] = lambda: mock_week_summary_service

        response = client.get('/api/v1/week_forecast', params={'latitude': 52.52, 'longitude': 13.419998})

        assert response.status_code == 200
        data = response.json()
        assert data['latitude'] == 52.52
        assert data['longitude'] == 13.419998

        app.dependency_overrides.clear()

    def test_get_week_summary_invalid_latitude_error(
            self, client: TestClient, mock_week_summary_service: MagicMock
    ) -> None:
        app.dependency_overrides[get_week_summary_service] = lambda: mock_week_summary_service

        response = client.get('/api/v1/week_forecast', params={'latitude': -91, 'longitude': 13.419998})

        assert response.status_code == 422

        error = response.json()
        assert 'detail' in error
        assert 'type' in error['detail'][0]
        assert error['detail'][0]['loc'] == ['query', 'latitude']

        app.dependency_overrides.clear()

    def test_get_week_summary_invalid_longitude_error(
            self, client: TestClient, mock_week_summary_service: MagicMock
    ) -> None:
        app.dependency_overrides[get_week_summary_service] = lambda: mock_week_summary_service

        response = client.get('/api/v1/week_forecast', params={'latitude': 52.52, 'longitude': -180.1})

        assert response.status_code == 422

        error = response.json()
        assert 'detail' in error
        assert 'type' in error['detail'][0]
        assert error['detail'][0]['loc'] == ['query', 'longitude']

        app.dependency_overrides.clear()

    def test_get_week_summary_missing_parameters_error(
            self, client: TestClient, mock_week_summary_service: MagicMock
    ) -> None:
        app.dependency_overrides[get_week_summary_service] = lambda: mock_week_summary_service

        response = client.get('/api/v1/week_summary')

        assert response.status_code == 422

        error = response.json()

        assert len(error['detail']) == 2

        missing_params = [err['loc'][-1] for err in error['detail']]
        assert 'latitude' in missing_params
        assert 'longitude' in missing_params

        app.dependency_overrides.clear()


class TestExceptionHandel:
    def test_weather_forecast_not_available_error_handler(
            self, client: TestClient, mock_forecast_service: MagicMock
    ) -> None:
        def raise_error(*args, **kwargs) -> None:
            raise WeatherForecastNotAvailableError()

        app.dependency_overrides[get_forecast_service] = lambda: mock_forecast_service
        mock_forecast_service.get_weather_forecast.side_effect = raise_error

        response = client.get('/api/v1/week_forecast', params={'latitude': 52.52, 'longitude': 13.419998})

        assert response.status_code == 500
        error = response.json()
        assert error['id'] == 'WeatherForecastNotAvailableError'

        app.dependency_overrides.clear()

    def test_week_summary_not_available_error_handler(
            self, client: TestClient, mock_week_summary_service: MagicMock
    ) -> None:
        def raise_error(*args, **kwargs) -> None:
            raise WeatherWeekSummaryNotAvailableError()

        app.dependency_overrides[get_week_summary_service] = lambda: mock_week_summary_service
        mock_week_summary_service.get_week_summary.side_effect = raise_error

        response = client.get('/api/v1/week_summary', params={'latitude': 52.52, 'longitude': 13.419998})

        assert response.status_code == 500
        error = response.json()
        assert error['id'] == 'WeatherWeekSummaryNotAvailableError'

        app.dependency_overrides.clear()
