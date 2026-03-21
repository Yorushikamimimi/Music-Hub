import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


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


DB_HOST = _require_env('DB_HOST')
DB_USER = _require_env('DB_USER')
DB_PASSWORD = _require_env('DB_PASSWORD')
DB_NAME = _require_env('DB_NAME')

encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{DB_USER}:{encoded_password}'
    f'@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = _require_strong_secret()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024
AVATAR_PERSISTENCE_FILE = os.path.join(BASE_DIR, 'current_avatar.txt')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
