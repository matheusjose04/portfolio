from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    access_token_expire_minutes: int = 720
    admin_user: str = "admin"
    admin_password: str = "admin123"
    origins: str = "http://localhost:4321"
    database_url: str = "sqlite:///./data/portfolio.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
