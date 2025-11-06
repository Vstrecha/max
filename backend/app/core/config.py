"""
App Config
Settings and environment configuration for the application.
"""

# --------------------------------------------------------------------------------

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# --------------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

# Перебор возможных путей для .env
ENV_PATHS = [
    Path(".env"),
    ROOT_DIR / ".env",
    ROOT_DIR / "app" / ".env",
    ROOT_DIR / "app" / "api" / ".env",
    ROOT_DIR / "app" / "core" / ".env",
]
ENV_FILE = None
for path in ENV_PATHS:
    if path.exists():
        ENV_FILE = path
        break
if ENV_FILE is None:
    ENV_FILE = ENV_PATHS[0]  # fallback, даже если не найден

load_dotenv(ENV_FILE)


# --------------------------------------------------------------------------------


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.

    Attributes:
        PROJECT_NAME (str): Application name.
        VERSION (str): Version of the application.
        API_VERSION (str): Base API path prefix.
    """

    PROJECT_NAME: str = "Встреча service"
    VERSION: str = "1.0.0"
    API_VERSION: str = "/v1"

    # Database
    DB_HOST: str = "test"
    DB_NAME: str = "test"
    DB_USER: str = "test"
    DB_PASSWORD: str = "test"

    @property
    def DATABASE_URL(self) -> str:
        """
        Construct database URL from individual components.

        Returns:
            str: Database connection URL.
        """

        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:5432/{self.DB_NAME}"

    # DOCS
    DOCS_USERNAME: str = "admin"
    DOCS_PASSWORD: str = "<PASSWORD>"
    BASE_API_URL: str = "http://localhost:8000"

    # TELEGRAM
    BOT_TOKEN: str = "<TOKEN>"

    # S3 Configuration
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = ""
    S3_ENDPOINT_URL: str = ""
    S3_PUBLIC_URL: str = ""
    S3_REGION: str = ""

    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "allow",
    }


# --------------------------------------------------------------------------------

settings = Settings()

# Event tags configuration
ALL_TAGS = ["Лекция", "Музей", "Спорт", "Музыка", "Природа"]
