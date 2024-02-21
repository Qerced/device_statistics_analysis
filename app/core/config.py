from pydantic_settings import BaseSettings


ENV_FILE = '.env'
DATABASE_URL = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'
REDIS_URL = 'redis://{host}:{port}'


class Settings(BaseSettings):
    DEBUG: bool
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    APP_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_url(self) -> str:
        return REDIS_URL.format(host=self.REDIS_HOST, port=self.REDIS_PORT)

    @property
    def database_url(self) -> str:
        return DATABASE_URL.format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST if not self.DEBUG else 'localhost',
            port=self.DB_PORT,
            db_name=self.POSTGRES_DB
        )

    class Config:
        env_file = ENV_FILE


settings = Settings()
