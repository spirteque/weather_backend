from datetime import datetime
from typing import Any

from pydantic import BaseModel

from src.models import CacheService
from src.utils import create_logger

logger = create_logger('DailyCacheService')


class DailyCacheService(CacheService):
	cache: dict[str, dict[str, Any]] = {}

	def add_cache(self, cache_key: str, cache_value: BaseModel) -> None:
		today_date = datetime.now().date()
		self._delete_old_cache(today_date)

		if self.cache.get(str(today_date)) is None:
			self.cache[str(today_date)] = {}

		self.cache[str(today_date)][cache_key] = cache_value
		logger.info(f'Added new cache for {today_date} with key {cache_key}.')

	def get_cache(self, cache_key: str) -> BaseModel | None:
		today_date = datetime.now().date()

		if date_cache := self.cache.get(str(today_date)):
			logger.info(f'Found cache for {today_date} with key {cache_key}.')

			return date_cache.get(cache_key)

		logger.info(f'Cache for {today_date} with key {cache_key} not found.')

		return None

	def _delete_old_cache(self, today_date: datetime.date) -> None:
		dates = self.cache.keys()
		keys_to_remove = []

		for date in dates:
			formatted_date = datetime.strptime(date, '%Y-%m-%d').date()

			if formatted_date < today_date:
				keys_to_remove.append(date)

		for key_to_remove in keys_to_remove:
			del self.cache[key_to_remove]
			logger.info(f'Deleted old cache from {key_to_remove}.')




