from enum import Enum

from pydantic import BaseModel, Extra

from src.models import WeatherTypeEnum


# Open Meteo weather codes mapping.
class OpenMeteoWeatherCodeEnum(Enum):
    CLEAR_SKY = 0
    MAINLY_CLEAR = 1
    PARTLY_CLOUDY = 2
    OVERCAST = 3
    FOG = 45
    DEPOSITING_RIME_FOG = 48
    DRIZZLE_LIGHT = 51
    DRIZZLE_MODERATE = 53
    DRIZZLE_DENSE = 55
    FREEZING_DRIZZLE_LIGHT = 56
    FREEZING_DRIZZLE_DENSE = 57
    RAIN_SLIGHT = 61
    RAIN_MODERATE = 63
    RAIN_HEAVY = 65
    FREEZING_RAIN_LIGHT = 66
    FREEZING_RAIN_HEAVY = 67
    SNOW_SLIGHT = 71
    SNOW_MODERATE = 73
    SNOW_HEAVY = 75
    SNOW_GRAINS = 77
    RAIN_SHOWERS_SLIGHT = 80
    RAIN_SHOWERS_MODERATE = 81
    RAIN_SHOWERS_VIOLENT = 82
    SNOW_SHOWERS_SLIGHT = 85
    SNOW_SHOWERS_HEAVY = 86
    THUNDERSTORM_SLIGHT_MODERATE = 95
    THUNDERSTORM_WITH_SLIGHT_HAIL = 96
    THUNDERSTORM_WITH_HEAVY_HAIL = 99


# Mapping weather codes to more general weather groups.
class OpenMeteoGroupedWeatherCodeEnum(Enum):
    CLEAR_SKY = (OpenMeteoWeatherCodeEnum.CLEAR_SKY,)
    CLOUDY = (
        OpenMeteoWeatherCodeEnum.MAINLY_CLEAR,
        OpenMeteoWeatherCodeEnum.PARTLY_CLOUDY,
        OpenMeteoWeatherCodeEnum.OVERCAST
    )
    FOG = (
        OpenMeteoWeatherCodeEnum.FOG,
        OpenMeteoWeatherCodeEnum.DEPOSITING_RIME_FOG
    )
    DRIZZLE = (
        OpenMeteoWeatherCodeEnum.DRIZZLE_LIGHT,
        OpenMeteoWeatherCodeEnum.DRIZZLE_MODERATE,
        OpenMeteoWeatherCodeEnum.DRIZZLE_DENSE
    )
    FREEZING_DRIZZLE = (
        OpenMeteoWeatherCodeEnum.FREEZING_DRIZZLE_LIGHT,
        OpenMeteoWeatherCodeEnum.FREEZING_DRIZZLE_DENSE
    )
    RAIN = (
        OpenMeteoWeatherCodeEnum.RAIN_SLIGHT,
        OpenMeteoWeatherCodeEnum.RAIN_MODERATE,
        OpenMeteoWeatherCodeEnum.RAIN_HEAVY
    )
    FREEZING_RAIN = (
        OpenMeteoWeatherCodeEnum.FREEZING_RAIN_LIGHT,
        OpenMeteoWeatherCodeEnum.FREEZING_RAIN_HEAVY
    )
    SNOW = (
        OpenMeteoWeatherCodeEnum.SNOW_SLIGHT,
        OpenMeteoWeatherCodeEnum.SNOW_MODERATE,
        OpenMeteoWeatherCodeEnum.SNOW_HEAVY
    )
    SNOW_GRAINS = (OpenMeteoWeatherCodeEnum.SNOW_GRAINS,)
    RAIN_SHOWERS = (
        OpenMeteoWeatherCodeEnum.RAIN_SHOWERS_SLIGHT,
        OpenMeteoWeatherCodeEnum.RAIN_SHOWERS_MODERATE,
        OpenMeteoWeatherCodeEnum.RAIN_SHOWERS_VIOLENT
    )
    SNOW_SHOWERS = (
        OpenMeteoWeatherCodeEnum.SNOW_SHOWERS_SLIGHT,
        OpenMeteoWeatherCodeEnum.SNOW_SHOWERS_HEAVY
    )
    THUNDERSTORM = (OpenMeteoWeatherCodeEnum.THUNDERSTORM_SLIGHT_MODERATE,)
    THUNDERSTORM_WITH_HAIL = (
        OpenMeteoWeatherCodeEnum.THUNDERSTORM_WITH_SLIGHT_HAIL,
        OpenMeteoWeatherCodeEnum.THUNDERSTORM_WITH_HEAVY_HAIL
    )

    @staticmethod
    def create_from_weather_code(code: OpenMeteoWeatherCodeEnum) -> 'OpenMeteoGroupedWeatherCodeEnum':
        # Iterate through weather groups values to match given weather code to its group.
        for member in OpenMeteoGroupedWeatherCodeEnum.__members__.values():
            if code in member.value:
                return member

        raise Exception(f'Given code is not supported: {code}')

    def to_weather_type(self) -> WeatherTypeEnum:
        # Convert weather group to weather type.
        match self.name:
            case 'CLEAR_SKY':
                return WeatherTypeEnum.CLEAR_SKY
            case 'CLOUDY':
                return WeatherTypeEnum.CLOUDY
            case 'FOG':
                return WeatherTypeEnum.FOG
            case 'DRIZZLE':
                return WeatherTypeEnum.DRIZZLE
            case 'FREEZING_DRIZZLE':
                return WeatherTypeEnum.FREEZING_DRIZZLE
            case 'RAIN':
                return WeatherTypeEnum.RAIN
            case 'FREEZING_RAIN':
                return WeatherTypeEnum.FREEZING_RAIN
            case 'SNOW':
                return WeatherTypeEnum.SNOW
            case 'SNOW_GRAINS':
                return WeatherTypeEnum.SNOW_GRAINS
            case 'RAIN_SHOWERS':
                return WeatherTypeEnum.RAIN_SHOWERS
            case 'SNOW_SHOWERS':
                return WeatherTypeEnum.SNOW_SHOWERS
            case 'THUNDERSTORM':
                return WeatherTypeEnum.THUNDERSTORM
            case 'THUNDERSTORM_WITH_HAIL':
                return WeatherTypeEnum.THUNDERSTORM_WITH_HAIL
            case _:
                raise ValueError(f'Unexpected group name: {self.name}')


# Models representing Open Meteo API responses:
class OpenMeteoHourlyUnits(BaseModel):
    time: str
    pressure_msl: str


class OpenMeteoHourly(BaseModel):
    time: list[str]
    pressure_msl: list[float]


class OpenMeteoDailyUnits(BaseModel):
    time: str
    weather_code: str
    temperature_2m_max: str
    temperature_2m_min: str
    sunshine_duration: str


class OpenMeteoDaily(BaseModel):
    time: list[str]
    weather_code: list[OpenMeteoWeatherCodeEnum]
    temperature_2m_max: list[float]
    temperature_2m_min: list[float]
    sunshine_duration: list[float]


class OpenMeteoWeatherForecast(BaseModel):
    latitude: float
    longitude: float
    daily_units: OpenMeteoDailyUnits
    daily: OpenMeteoDaily

    # Ignores additional keys in Open Meteo response,
    # that are not part of the model representation.
    class Config:
        extra = Extra.ignore


class OpenMeteoWeatherWeekSummary(BaseModel):
    latitude: float
    longitude: float
    hourly_units: OpenMeteoHourlyUnits
    hourly: OpenMeteoHourly
    daily_units: OpenMeteoDailyUnits
    daily: OpenMeteoDaily

    # Ignores additional keys in Open Meteo response,
    # that are not part of the model representation.
    class Config:
        extra = Extra.ignore
