import logging
import logging.config
from dotenv import load_dotenv
import os
import colorlog

load_dotenv()

custom_dict = {
    "version": 1,
    "formatters": {
        "default": {
            "()": colorlog.ColoredFormatter,
            "format": "[%(asctime)s] [%(log_color)s%(levelname)-4s%(reset)s] [%(module)s] [%(funcName)s] >> %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL", "INFO"),
        }
    },
}

logging.config.dictConfig(custom_dict)

logger = logging.getLogger(__name__)
