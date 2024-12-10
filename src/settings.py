import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import PROJECT_NAME


def create_dotenv_file_path() -> str:
	path = str(pathlib.Path().resolve())

	if not path.endswith(PROJECT_NAME):
		separate_path = path.split(PROJECT_NAME, 1)
		path = separate_path[0] + PROJECT_NAME

	return path + '/.env'


# Settings model allows using environment variables defined in .env file (for non-production environments)
# or standard environment variables depending on the "PRODUCTION" environment variable
# (0 = production disabled, 1 = production enabled).
class Settings(BaseSettings):
	open_meteo_base_url: str
	min_latitude: float
	max_latitude: float
	min_longitude: float
	max_longitude: float
	installation_power_kw: float
	installation_efficiency: float

	model_config = SettingsConfigDict(
		env_file=create_dotenv_file_path() if not bool(os.getenv("PRODUCTION", 0)) else None
	)


settings = Settings()
