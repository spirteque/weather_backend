import pytest

from src.models import DayEnum


class TestDayEnum:
	def test_get_by_index_success(self) -> None:
		for i, expected_day in enumerate(DayEnum):
			day = DayEnum.get_by_index(i)
			assert isinstance(day, str)
			assert day == expected_day.name

	def test_get_by_index_invalid_index_error(self) -> None:
		invalid_indices = [-1, 7, 100]
		for invalid_index in invalid_indices:
			with pytest.raises(Exception, match="Couldn't resolve day!"):
				DayEnum.get_by_index(invalid_index)
