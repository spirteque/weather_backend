import json
import logging


# Logs are created in JSON format to easily integrate them with
# some external tools used to collect and display logs (e.g. Graylog).
class JSONFormatter(logging.Formatter):
	def format(self, record: logging.LogRecord) -> str:
		log_record = {
			"time": self.formatTime(record, self.datefmt),
			"level": record.levelname,
			"name": record.name,
			"message": record.getMessage()
		}

		return json.dumps(log_record)


def create_logger(name: str) -> logging.Logger:
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	handler = logging.StreamHandler()
	handler.setFormatter(JSONFormatter())
	logger.addHandler(handler)

	return logger
