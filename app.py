"""Flask application factory for Music Hub."""

import os

from flask import Flask, jsonify, request, url_for
from flask_migrate import Migrate
from sqlalchemy import text

from commands import register_commands
from catalog_data import CATALOG_TRACKS
from config import load_runtime_config
from models import db
from routes.main import main_bp

migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config is None:
        app.config.update(load_runtime_config())
    else:
        app.config.update(test_config)
        app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
        app.config.setdefault("MAX_CONTENT_LENGTH", 2 * 1024 * 1024)
        app.config.setdefault("SEND_FILE_MAX_AGE_DEFAULT", 0)
    app.config.setdefault(
        "RADIO_STATION_NAME",
        os.getenv("RADIO_STATION_NAME", "夜鹿电台"),
    )
    app.config.setdefault(
        "RADIO_STREAM_URL",
        os.getenv("RADIO_STREAM_URL", "").strip(),
    )

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main_bp)
    register_commands(app)

    @app.context_processor
    def inject_global_radio():
        """Expose one persistent private radio player to every page."""
        return {
            "global_radio_station_name": app.config["RADIO_STATION_NAME"],
            "global_radio_stream_url": app.config["RADIO_STREAM_URL"],
            "global_radio_private_mode": True,
            "global_radio_artwork_map": {
                track["title_ja"]: url_for(
                    "static",
                    filename=f"images/{track['cover_path']}",
                )
                for track in CATALOG_TRACKS
            },
        }

    @app.get("/healthz")
    def healthz():
        """Report whether the web process can reach its database."""
        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            app.logger.exception("Music Hub database health check failed")
            db.session.remove()
            return jsonify(status="unhealthy"), 503

        return jsonify(status="ok"), 200

    @app.after_request
    def set_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy",
            "geolocation=(), microphone=(), camera=()",
        )
        response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")

        csp = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "media-src 'self' blob:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers.setdefault("Content-Security-Policy", csp)

        if (
            request.is_secure
            or request.headers.get("X-Forwarded-Proto", "").lower() == "https"
        ):
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains; preload",
            )

        return response

    @app.errorhandler(413)
    def request_entity_too_large(_error):
        return jsonify(error="Request is too large. Maximum allowed size is 2 MB."), 413

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
