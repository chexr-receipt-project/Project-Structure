from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGO_URL: str
    MONGO_DATABASE: str
    MATCHING_QUEUE_URL: str
    AWS_REGION: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
