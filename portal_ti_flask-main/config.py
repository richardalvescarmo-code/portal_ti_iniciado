import os

from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy.engine import URL


load_dotenv(override=True)


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "A variável SECRET_KEY não foi definida no arquivo .env."
        )

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookies de sessão
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Em produção deve ficar True, pois exige HTTPS.
    # Localmente pode ser False.
    SESSION_COOKIE_SECURE = (
        os.getenv(
            "SESSION_COOKIE_SECURE",
            "false"
        ).lower()
        == "true"
    )

    # Tempo máximo da sessão
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=30
    )

    # Limite máximo para uploads: 100 MB
    MAX_CONTENT_LENGTH = (
        100 * 1024 * 1024
    )

    # Evita propagação desnecessária de exceções
    TESTING = False

    TOPDESK_URL = os.getenv(
        "TOPDESK_URL"
    )

    PLANNER_URL = os.getenv(
        "PLANNER_URL"
    )