from pydantic import BaseModel


class WeatherDay(BaseModel):
	time: str
	weather_code: int
	temp_max: float
	temp_min: float
	sunshine_duration: float
	generated_energy: float


class WeatherForecast(BaseModel):
	latitude: float
	longitude: float
	time_unit: str
	weather_code_unit: str
	temp_max_unit: str
	temp_min_unit: str
	sunshine_duration_unit: str
	generated_energy_unit: str
	installation_power_unit: str
	installation_power: float
	installation_efficiency: float
	days: list[WeatherDay]
