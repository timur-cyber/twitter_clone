dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(asctime)s | line: %(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
        },
        "debug": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "logs/log.txt",
            "mode": "a",
        },
        "errors": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "base",
            "filename": "logs/errors.txt",
            "mode": "a",
        },
    },
    "loggers": {
        "twitter log": {"level": "DEBUG", "handlers": ["console", "debug", "errors"]}
    },
}
