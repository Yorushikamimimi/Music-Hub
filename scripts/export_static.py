"""Export 夜鹿集 as plain files for nginx: no database, login, search or radio.

    .venv/bin/python scripts/export_static.py            # -> build/static-site/
    .venv/bin/python scripts/export_static.py OUT_DIR

Pages are rendered from catalog_data.py through the real app (STATIC_SITE on,
so search, filters and the radio are left out), found by following the site's
own links from the home page. Each page is written as <path>/index.html; nginx
serves them with ``try_files $uri $uri/index.html =404``.
"""

import os
import re
import shutil
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

os.environ.setdefault("PYTHON_DOTENV_DISABLED", "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from catalog_service import sync_catalog  # noqa: E402
from models import db  # noqa: E402

# Server-only pages that stay out of the static site.
SKIP = re.compile(r"^/(search|radio|local/|songs/by-title|health|static/)")
# Scripts only the dynamic site needs.
SKIP_STATIC = {"radio.js"}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = set()

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href") or ""
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or not parts.path.startswith("/"):
            return
        self.found.add(parts.path)


def page_file(out, path):
    if path.endswith((".txt", ".xml", ".ico")):
        return out / path.lstrip("/")
    return out / path.strip("/") / "index.html" if path != "/" else out / "index.html"


def export(out):
    out = Path(out)
    workdir = Path(tempfile.mkdtemp(prefix="yeluji-export-"))
    app = create_app(
        {
            "SECRET_KEY": "static-export-only",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{workdir / 'export.sqlite3'}",
            "STATIC_SITE": True,
            "RADIO_STREAM_URL": "",
            "STUDIO_URL": "",
        }
    )
    with app.app_context():
        db.create_all()
        sync_catalog()
    client = app.test_client()

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    seen, queue, written = set(), ["/", "/robots.txt"], []
    while queue:
        path = queue.pop()
        if path in seen or SKIP.match(path):
            continue
        seen.add(path)
        resp = client.get(path)
        if resp.status_code != 200:
            print(f"跳过 {path}（{resp.status_code}）")
            continue
        target = page_file(out, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(resp.data)
        written.append(path)
        if resp.mimetype == "text/html":
            parser = Links()
            parser.feed(resp.get_data(as_text=True))
            queue.extend(sorted(parser.found - seen))

    missing = client.get("/__not-a-page__")
    (out / "404.html").write_bytes(missing.data)
    shutil.copytree(ROOT / "static", out / "static",
                    ignore=lambda d, names: [n for n in names if n in SKIP_STATIC or n == "uploads"])
    shutil.rmtree(workdir, ignore_errors=True)
    return sorted(written)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else ROOT / "build" / "static-site"
    pages = export(target)
    print(f"已导出 {len(pages)} 个页面到 {target}")
