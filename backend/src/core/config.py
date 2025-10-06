from pydantic_settings import BaseSettings

from urllib.parse import quote_plus

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        password_encoded = quote_plus(self.postgres_password)
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{password_encoded}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
