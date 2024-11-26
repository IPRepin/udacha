from pydantic.v1 import BaseSettings


class TestSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    LOGS_PATH: str = "logs/test.log"
    ADMINS: int = 123456789
    DB_URL: str = "sqlite+aiosqlite:///:memory:"

    class Config:
        env_file: str = ".env.test"


test_settings = TestSettings()
