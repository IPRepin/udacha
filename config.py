from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    TELEGRAM_TOKEN: str
    LOGS_PATH: str

    ADMINS: int

    DB_URL: str

    class Config:
        env_file: str = ".env"


settings = Settings()
