import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


def create_dotenv_file_path() -> str:
	path = str(pathlib.Path().resolve())
	project_name = 'backend_weather'

	if not path.endswith(project_name):
		separate_path = path.split(project_name, 1)
		path = separate_path[0] + project_name

	return path + '/.env'


class Settings(BaseSettings):
	open_meteo_base_url: str
	min_latitude: float
	max_latitude: float
	min_longitude: float
	max_longitude: float
	installation_power_kw: float
	installation_efficiency: float

	model_config = SettingsConfigDict(env_file=create_dotenv_file_path())


settings = Settings()
