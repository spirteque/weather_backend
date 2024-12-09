import pytest

from src.models import WeatherTypeEnum
from src.open_meteo.models import OpenMeteoGroupedWeatherCodeEnum, OpenMeteoWeatherCodeEnum


class TestOpenMeteoWeatherCodeEnum:
	def test_create_from_weather_code_success(self) -> None:
		codes = [v for v in OpenMeteoWeatherCodeEnum]

		for code in codes:
			group = OpenMeteoGroupedWeatherCodeEnum.create_from_weather_code(code)
			assert isinstance(group, OpenMeteoGroupedWeatherCodeEnum)

	def test_create_from_weather_code_invalid_code_error(self) -> None:
		with pytest.raises(Exception):
			OpenMeteoGroupedWeatherCodeEnum.create_from_weather_code(999)

	def test_to_weather_type_success(self) -> None:
		for group in OpenMeteoGroupedWeatherCodeEnum:
			assert isinstance(group.to_weather_type(), WeatherTypeEnum)

