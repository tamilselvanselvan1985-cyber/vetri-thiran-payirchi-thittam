from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


APP_NAME = os.getenv(
    "APP_NAME",
    "PocketSmart AI"
)

APP_ENV = os.getenv(
    "APP_ENV",
    "development"
)


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-change-me"
)


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(BASE_DIR / "data" / "pocketsmart.db")
)


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-1.5-flash"
).strip()


AI_ENABLED = os.getenv(
    "AI_ENABLED",
    "true"
).lower() in {
    "1",
    "true",
    "yes",
    "on"
}


ALLOWED_ORIGINS = [
    item.strip()
    for item in os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000"
    ).split(",")
    if item.strip()
]


UPLOAD_DIR = (
    BASE_DIR
    / "app"
    / "static"
    / "uploads"
)


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


Path(DATABASE_PATH).parent.mkdir(
    parents=True,
    exist_ok=True
)