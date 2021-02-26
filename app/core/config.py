from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
