import os
import urllib.parse

from dotenv import load_dotenv


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f'Missing required environment variable: {name}')
    return value.strip()


def _require_strong_secret() -> str:
    secret = _require_env('SECRET_KEY')
    blocked = {
        'dev-fallback-key-change-in-production',
        'please-change-this-to-a-long-random-string-in-production',
    }
    if secret in blocked or len(secret) < 16:
        raise RuntimeError('SECRET_KEY is too weak. Use a random string with length >= 16.')
    return secret


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_CONTENT_LENGTH = 2 * 1024 * 1024


def load_runtime_config() -> dict:
    """Load production configuration without exposing secret values."""
    load_dotenv()

    db_host = _require_env('DB_HOST')
    db_user = _require_env('DB_USER')
    db_password = urllib.parse.quote_plus(_require_env('DB_PASSWORD'))
    db_name = _require_env('DB_NAME')

    return {
        'SECRET_KEY': _require_strong_secret(),
        'SQLALCHEMY_DATABASE_URI': (
            f'mysql+pymysql://{db_user}:{db_password}'
            f'@{db_host}/{db_name}?charset=utf8mb4'
        ),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 280,
        },
        'MAX_CONTENT_LENGTH': MAX_CONTENT_LENGTH,
        'SEND_FILE_MAX_AGE_DEFAULT': 86400,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'TRUSTED_HOSTS': ['81.68.72.245', 'localhost', '127.0.0.1'],
    }
