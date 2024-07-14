from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASES: str

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASES}"


    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_HOST: str

    @property
    def TEST_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}"
            f"@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
        )


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()