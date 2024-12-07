from pydantic import BaseModel


class WeatherDay(BaseModel):
	time: str
	weather_code: int
	temp_max: float
	temp_min: float
	sunshine_duration: float


class WeatherForecast(BaseModel):
	latitude: float
	longitude: float
	time_unit: str
	weather_code_unit: str
	temp_max_unit: str
	temp_min_unit: str
	sunshine_duration_unit: str
	days: list[WeatherDay]
