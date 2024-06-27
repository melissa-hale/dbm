import os
import logging.config


class Settings:
    def __init__(self):
        self.ATLAS_URI = os.getenv("ATLAS_URI")
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
        self.MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
        self.MINIO_ADDR = os.getenv("MINIO_ADDR")
        self.MINIO_BUCKET = os.getenv("MINIO_BUCKET")
        self.API_KEY = os.getenv("API_KEY")

settings = None

def get_settings():
    global settings
    if settings is None:
        settings = Settings()
    return settings

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
