from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These variables MUST be provided in the .env file or environment variables.
    BASE_URL: str
    TIMEOUT: int

    # This tells pydantic to load variables from a .env file if it exists
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
