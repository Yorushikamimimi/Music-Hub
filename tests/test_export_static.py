import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_exporter():
    spec = importlib.util.spec_from_file_location("export_static", ROOT / "scripts" / "export_static.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_export_writes_pages_without_search_radio_or_forms(tmp_path):
    out = tmp_path / "site"
    pages = load_exporter().export(out)
    assert "/" in pages and "/discography" in pages and "/lyrics" in pages
    assert any(p.startswith("/songs/") for p in pages) and any(p.startswith("/releases/") for p in pages)
    assert not any(p.startswith(("/search", "/radio", "/local/")) for p in pages)
    assert (out / "404.html").exists() and (out / "robots.txt").exists()
    assert not (out / "static" / "radio.js").exists()
    for html in out.rglob("index.html"):
        text = html.read_text(encoding="utf-8")
        assert "<form" not in text, html
        assert 'href="/search' not in text and 'href="/radio' not in text, html
        assert "data-studio" not in text, html
