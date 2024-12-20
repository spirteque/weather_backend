from src.models import CacheService
from src.services import DailyCacheService

from ..conftest import *


@pytest.fixture
def cache_service() -> CacheService:
	cache = DailyCacheService()
	yield cache
	cache.cache.clear()


@pytest.fixture
def open_meteo_forecast_response() -> dict:
	return {
		"latitude": 52.52,
		"longitude": 13.419998,
		"generationtime_ms": 0.10001659393310547,
		"utc_offset_seconds": 0,
		"timezone": "GMT",
		"timezone_abbreviation": "GMT",
		"elevation": 38,
		"daily_units": {
			"time": "iso8601",
			"weather_code": "wmo code",
			"temperature_2m_max": "°C",
			"temperature_2m_min": "°C",
			"sunshine_duration": "s"
		},
		"daily": {
			"time": [
				"2024-12-08",
				"2024-12-09",
				"2024-12-10",
				"2024-12-11",
				"2024-12-12",
				"2024-12-13",
				"2024-12-14"
			],
			"weather_code": [
				61,
				61,
				61,
				3,
				3,
				3,
				3
			],
			"temperature_2m_max": [
				4.8,
				4.9,
				3.7,
				2.5,
				2.6,
				1.4,
				0.2
			],
			"temperature_2m_min": [
				3.5,
				2,
				2.1,
				1.5,
				0,
				-0.4,
				-0.6
			],
			"sunshine_duration": [
				0,
				0,
				0,
				6231.31,
				183.85,
				19272.82,
				2867.29
			]
		}
	}


@pytest.fixture
def open_meteo_week_summary_response() -> dict:
	return {
		"latitude": 52.52,
		"longitude": 13.419998,
		"generationtime_ms": 0.10502338409423828,
		"utc_offset_seconds": 0,
		"timezone": "GMT",
		"timezone_abbreviation": "GMT",
		"elevation": 38,
		"hourly_units": {
			"time": "iso8601",
			"pressure_msl": "hPa"
		},
		"hourly": {
			"time": [
				"2024-12-09T00:00",
				"2024-12-09T01:00",
				"2024-12-09T02:00",
				"2024-12-09T03:00",
				"2024-12-09T04:00",
				"2024-12-09T05:00",
				"2024-12-09T06:00",
				"2024-12-09T07:00",
				"2024-12-09T08:00",
				"2024-12-09T09:00",
				"2024-12-09T10:00",
				"2024-12-09T11:00",
				"2024-12-09T12:00",
				"2024-12-09T13:00",
				"2024-12-09T14:00",
				"2024-12-09T15:00",
				"2024-12-09T16:00",
				"2024-12-09T17:00",
				"2024-12-09T18:00",
				"2024-12-09T19:00",
				"2024-12-09T20:00",
				"2024-12-09T21:00",
				"2024-12-09T22:00",
				"2024-12-09T23:00",
				"2024-12-10T00:00",
				"2024-12-10T01:00",
				"2024-12-10T02:00",
				"2024-12-10T03:00",
				"2024-12-10T04:00",
				"2024-12-10T05:00",
				"2024-12-10T06:00",
				"2024-12-10T07:00",
				"2024-12-10T08:00",
				"2024-12-10T09:00",
				"2024-12-10T10:00",
				"2024-12-10T11:00",
				"2024-12-10T12:00",
				"2024-12-10T13:00",
				"2024-12-10T14:00",
				"2024-12-10T15:00",
				"2024-12-10T16:00",
				"2024-12-10T17:00",
				"2024-12-10T18:00",
				"2024-12-10T19:00",
				"2024-12-10T20:00",
				"2024-12-10T21:00",
				"2024-12-10T22:00",
				"2024-12-10T23:00",
				"2024-12-11T00:00",
				"2024-12-11T01:00",
				"2024-12-11T02:00",
				"2024-12-11T03:00",
				"2024-12-11T04:00",
				"2024-12-11T05:00",
				"2024-12-11T06:00",
				"2024-12-11T07:00",
				"2024-12-11T08:00",
				"2024-12-11T09:00",
				"2024-12-11T10:00",
				"2024-12-11T11:00",
				"2024-12-11T12:00",
				"2024-12-11T13:00",
				"2024-12-11T14:00",
				"2024-12-11T15:00",
				"2024-12-11T16:00",
				"2024-12-11T17:00",
				"2024-12-11T18:00",
				"2024-12-11T19:00",
				"2024-12-11T20:00",
				"2024-12-11T21:00",
				"2024-12-11T22:00",
				"2024-12-11T23:00",
				"2024-12-12T00:00",
				"2024-12-12T01:00",
				"2024-12-12T02:00",
				"2024-12-12T03:00",
				"2024-12-12T04:00",
				"2024-12-12T05:00",
				"2024-12-12T06:00",
				"2024-12-12T07:00",
				"2024-12-12T08:00",
				"2024-12-12T09:00",
				"2024-12-12T10:00",
				"2024-12-12T11:00",
				"2024-12-12T12:00",
				"2024-12-12T13:00",
				"2024-12-12T14:00",
				"2024-12-12T15:00",
				"2024-12-12T16:00",
				"2024-12-12T17:00",
				"2024-12-12T18:00",
				"2024-12-12T19:00",
				"2024-12-12T20:00",
				"2024-12-12T21:00",
				"2024-12-12T22:00",
				"2024-12-12T23:00",
				"2024-12-13T00:00",
				"2024-12-13T01:00",
				"2024-12-13T02:00",
				"2024-12-13T03:00",
				"2024-12-13T04:00",
				"2024-12-13T05:00",
				"2024-12-13T06:00",
				"2024-12-13T07:00",
				"2024-12-13T08:00",
				"2024-12-13T09:00",
				"2024-12-13T10:00",
				"2024-12-13T11:00",
				"2024-12-13T12:00",
				"2024-12-13T13:00",
				"2024-12-13T14:00",
				"2024-12-13T15:00",
				"2024-12-13T16:00",
				"2024-12-13T17:00",
				"2024-12-13T18:00",
				"2024-12-13T19:00",
				"2024-12-13T20:00",
				"2024-12-13T21:00",
				"2024-12-13T22:00",
				"2024-12-13T23:00",
				"2024-12-14T00:00",
				"2024-12-14T01:00",
				"2024-12-14T02:00",
				"2024-12-14T03:00",
				"2024-12-14T04:00",
				"2024-12-14T05:00",
				"2024-12-14T06:00",
				"2024-12-14T07:00",
				"2024-12-14T08:00",
				"2024-12-14T09:00",
				"2024-12-14T10:00",
				"2024-12-14T11:00",
				"2024-12-14T12:00",
				"2024-12-14T13:00",
				"2024-12-14T14:00",
				"2024-12-14T15:00",
				"2024-12-14T16:00",
				"2024-12-14T17:00",
				"2024-12-14T18:00",
				"2024-12-14T19:00",
				"2024-12-14T20:00",
				"2024-12-14T21:00",
				"2024-12-14T22:00",
				"2024-12-14T23:00",
				"2024-12-15T00:00",
				"2024-12-15T01:00",
				"2024-12-15T02:00",
				"2024-12-15T03:00",
				"2024-12-15T04:00",
				"2024-12-15T05:00",
				"2024-12-15T06:00",
				"2024-12-15T07:00",
				"2024-12-15T08:00",
				"2024-12-15T09:00",
				"2024-12-15T10:00",
				"2024-12-15T11:00",
				"2024-12-15T12:00",
				"2024-12-15T13:00",
				"2024-12-15T14:00",
				"2024-12-15T15:00",
				"2024-12-15T16:00",
				"2024-12-15T17:00",
				"2024-12-15T18:00",
				"2024-12-15T19:00",
				"2024-12-15T20:00",
				"2024-12-15T21:00",
				"2024-12-15T22:00",
				"2024-12-15T23:00"
			],
			"pressure_msl": [
				1020,
				1019.9,
				1019.8,
				1019.9,
				1020.2,
				1020.2,
				1021.5,
				1022.4,
				1023.2,
				1023.8,
				1024.2,
				1024.4,
				1024.4,
				1024.6,
				1025.3,
				1025.5,
				1025.8,
				1026,
				1026.7,
				1027.3,
				1027.9,
				1028.2,
				1028.4,
				1028.6,
				1028.9,
				1029.4,
				1029.5,
				1029.5,
				1029.7,
				1029.8,
				1030,
				1030.3,
				1030.9,
				1031.1,
				1031,
				1030.7,
				1030.5,
				1030.5,
				1030.8,
				1031.1,
				1031.2,
				1031.2,
				1031,
				1030.9,
				1030.8,
				1030.7,
				1030.6,
				1030.4,
				1030.3,
				1030,
				1029.9,
				1029.8,
				1029.7,
				1029.6,
				1029.5,
				1029.7,
				1030,
				1030.4,
				1030.3,
				1030,
				1029.7,
				1029.7,
				1029.8,
				1029.9,
				1029.7,
				1030,
				1030.5,
				1030.8,
				1031.1,
				1031.1,
				1031.5,
				1031.4,
				1031.3,
				1031.4,
				1031.6,
				1031.7,
				1031.8,
				1031.9,
				1032.1,
				1032.4,
				1032.8,
				1033.2,
				1033.6,
				1033.4,
				1033.1,
				1033.1,
				1033.2,
				1033.4,
				1033.7,
				1034,
				1034.3,
				1034.5,
				1034.6,
				1034.8,
				1035,
				1035.2,
				1035.3,
				1035.4,
				1035.4,
				1035.4,
				1035.2,
				1035,
				1034.8,
				1034.8,
				1034.9,
				1034.8,
				1034.4,
				1033.8,
				1033.2,
				1032.5,
				1031.8,
				1031.1,
				1030.5,
				1029.8,
				1029.2,
				1028.6,
				1027.9,
				1027.2,
				1026.5,
				1025.7,
				1024.9,
				1024,
				1023.1,
				1022.3,
				1021.6,
				1021.1,
				1020.7,
				1017.9,
				1017.6,
				1017.2,
				1016.7,
				1016.1,
				1015.7,
				1015.5,
				1015.4,
				1015.2,
				1014.9,
				1014.5,
				1014.1,
				1013.9,
				1013.7,
				1013.5,
				1013.3,
				1013.2,
				1013.1,
				1013.1,
				1013.2,
				1013.5,
				1014,
				1014.8,
				1015.6,
				1016.6,
				1017.6,
				1018.5,
				1019.1,
				1019.4,
				1019.8,
				1020.2,
				1020.5,
				1020.8,
				1021.1,
				1021.3,
				1021.4,
				1021.3,
				1021.1,
				1020.9,
				1020.7,
				1020.4
			]
		},
		"daily_units": {
			"time": "iso8601",
			"weather_code": "wmo code",
			"temperature_2m_max": "°C",
			"temperature_2m_min": "°C",
			"sunshine_duration": "s"
		},
		"daily": {
			"time": [
				"2024-12-09",
				"2024-12-10",
				"2024-12-11",
				"2024-12-12",
				"2024-12-13",
				"2024-12-14",
				"2024-12-15"
			],
			"weather_code": [
				61,
				61,
				51,
				3,
				3,
				71,
				71
			],
			"temperature_2m_max": [
				4.7,
				3.4,
				2.9,
				2.4,
				-0.1,
				0.2,
				3.5
			],
			"temperature_2m_min": [
				1.4,
				1.8,
				1.3,
				0.2,
				-2.2,
				-2.4,
				0.2
			],
			"sunshine_duration": [
				0,
				0,
				421.61,
				9895.27,
				14395.65,
				0,
				2221.34
			]
		}
	}
