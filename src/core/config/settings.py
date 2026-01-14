from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения"""
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/techpark"
    database_echo: bool = False
    
    app_name: str = "Сервис расчёта стоимости изделия"
    debug: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


app_settings = Settings()

