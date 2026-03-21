from flask import Flask, jsonify
import config
from models import db
from routes.main import main_bp

app = Flask(__name__)

# ── 安全配置 ────────────────────────────────────────────────
app.secret_key = config.SECRET_KEY

# ── 数据库配置 ──────────────────────────────────────────────
app.config['SQLALCHEMY_DATABASE_URI']        = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# ── 上传配置 ─────────────────────────────────────────────────
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# ── 初始化扩展 ───────────────────────────────────────────────
db.init_app(app)

# ── 注册蓝图 ─────────────────────────────────────────────────
app.register_blueprint(main_bp)

# ── 自动建表（Gunicorn 等 WSGI 服务器也能执行）───────────────
with app.app_context():
    db.create_all()

# ── 错误处理 ─────────────────────────────────────────────────
@app.errorhandler(413)
def request_entity_too_large(e):
    """上传文件超过 2 MB 限制时返回友好的 JSON 错误。"""
    return jsonify(error="上传文件太大，请控制在 2 MB 以内"), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
