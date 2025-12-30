from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    # Database Settings
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Seed Settings
    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str
    DEFAULT_VET_EMAIL: str
    DEFAULT_VET_PASSWORD: str

    # Email / SendGrid
    SENDGRID_API_KEY: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str = "LeishAI"
    FRONTEND_BASE_URL: str = "http://localhost:5173"
    BACKEND_BASE_URL: str = "http://127.0.0.1:8000"
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_NOTIFICATION_EMAIL: str | None = None

    TESTING: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    @property
    def DATABASE_URL(self) -> str:
        password_encoded = quote_plus(self.postgres_password)
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{password_encoded}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
