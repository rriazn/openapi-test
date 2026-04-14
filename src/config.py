from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    database_url: str = "sqlite:///./test.db"
    backend_url: str = "http://localhost:7000"
    workout_save_time_days: int = 60
    workout_stop_time_hours: int = 12

def get_settings() -> Settings:
    return Settings()