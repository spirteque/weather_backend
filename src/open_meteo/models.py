from pydantic import BaseModel, Extra


class OpenMeteoDailyUnits(BaseModel):
    time: str
    weather_code: str
    temperature_2m_max: str
    temperature_2m_min: str
    sunshine_duration: str


class OpenMeteoDaily(BaseModel):
    time: list[str]
    weather_code: list[int]
    temperature_2m_max: list[float]
    temperature_2m_min: list[float]
    sunshine_duration: list[float]


class OpenMeteoWeatherForecast(BaseModel):
    latitude: float
    longitude: float
    daily_units: OpenMeteoDailyUnits
    daily: OpenMeteoDaily

    class Config:
        extra = Extra.ignore
