"""Run 夜鹿集 locally for review: temporary SQLite, real catalog, no password.

    .venv/bin/python scripts/local_preview.py            # http://127.0.0.1:61705
    STUDIO_URL=... PORT=... .venv/bin/python scripts/local_preview.py

The database is rebuilt from catalog_data.py on every start and lives in a
temporary folder, so nothing touches the server or real favourites. When the
local visual studio is running (default http://127.0.0.1:8765), song pages
show the frames kept there.
"""

import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYTHON_DOTENV_DISABLED", "1")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app  # noqa: E402
from catalog_service import sync_catalog  # noqa: E402
from models import db  # noqa: E402


def main():
    workdir = Path(tempfile.mkdtemp(prefix="yeluji-preview-"))
    app = create_app(
        {
            "SECRET_KEY": "local-preview-only",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{workdir / 'preview.sqlite3'}",
            "STUDIO_URL": os.getenv("STUDIO_URL", "http://127.0.0.1:8765"),
            # Only answer to this machine's own addresses (blocks DNS rebinding).
            "TRUSTED_HOSTS": ["127.0.0.1", "localhost"],
        }
    )
    with app.app_context():
        db.create_all()
        sync_catalog()
    port = int(os.getenv("PORT", "61705"))
    print(f"夜鹿集本机预览：http://127.0.0.1:{port}/  （数据库在 {workdir}）")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
