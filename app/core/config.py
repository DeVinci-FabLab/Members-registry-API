from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    # Tell Pydantic to load environment variables from .env
    model_config = SettingsConfigDict(env_file="./docker/.env")

settings = Settings()