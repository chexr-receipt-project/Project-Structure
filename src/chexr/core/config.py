from pydantic import BaseSettings
import logging


class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGO_URL: str
    MONGO_DATABASE: str
    MATCHING_QUEUE_URL: str
    AWS_REGION: str
    LOG_LEVEL: int = logging.INFO

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(settings.LOG_LEVEL)
else:
    logging.basicConfig(level=settings.LOG_LEVEL)

logging.info("Settings loaded and logging configured")
