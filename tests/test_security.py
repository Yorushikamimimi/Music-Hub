def _directive(csp, name):
    return next(part.strip() for part in csp.split(";") if part.strip().startswith(name))


def test_security_headers_restrict_embedding_and_inline_scripts(client):
    response = client.get("/")
    csp = response.headers["Content-Security-Policy"]

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Robots-Tag"] == "noindex, nofollow"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert _directive(csp, "script-src") == "script-src 'self'"
    assert _directive(csp, "frame-ancestors") == "frame-ancestors 'none'"
    assert "'unsafe-inline'" not in _directive(csp, "script-src")


def test_runtime_templates_do_not_emit_inline_scripts(client):
    for path in ("/", "/search", "/lyrics", "/radio", "/about"):
        page = client.get(path).get_data(as_text=True)
        assert "<script>" not in page
        assert "javascript:" not in page.lower()


def test_test_app_uses_safe_cookie_defaults(app):
    assert app.config.get("SESSION_COOKIE_HTTPONLY", True) is True
    assert app.config.get("SESSION_COOKIE_SAMESITE", "Lax") == "Lax"
