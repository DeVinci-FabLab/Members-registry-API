from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str =""
    POSTGRES_PASSWORD: str =""
    POSTGRES_DB: str =""

    # Tell Pydantic to load environment variables from .env
    model_config = SettingsConfigDict(env_file="./docker/.env")

settings = Settings()