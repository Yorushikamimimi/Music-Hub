from flask import Flask, jsonify, request
import config
from models import db
from routes.main import main_bp

app = Flask(__name__)


@app.after_request
def set_security_headers(response):
    """Add baseline security headers for HTTPS deployment."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")

    csp = (
        "default-src 'self' https: data: blob:; "
        "img-src 'self' https: data: blob:; "
        "style-src 'self' 'unsafe-inline' https:; "
        "script-src 'self' 'unsafe-inline' https:; "
        "font-src 'self' data: https:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'self'; "
        "upgrade-insecure-requests; "
        "block-all-mixed-content"
    )
    response.headers.setdefault("Content-Security-Policy", csp)

    if request.is_secure or request.headers.get("X-Forwarded-Proto", "").lower() == "https":
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains; preload",
        )

    return response


app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

db.init_app(app)
app.register_blueprint(main_bp)

with app.app_context():
    db.create_all()


@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify(error="Upload is too large. Maximum allowed size is 2 MB."), 413


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)