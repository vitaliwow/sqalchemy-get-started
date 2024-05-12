from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self) -> str:
        return self._database_url("postgresql+asyncpg")

    @property
    def database_url_psycopg(self) -> str:
        return self._database_url("postgresql+psycopg")

    def _database_url(self, driver: str) -> str:
        return f"{driver}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
