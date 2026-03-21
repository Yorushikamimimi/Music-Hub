from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

db = SQLAlchemy()

# 鍖椾含鏃堕棿 UTC+8
BEIJING_TZ = timezone(timedelta(hours=8))

def beijing_now():
    """杩斿洖褰撳墠鍖椾含鏃堕棿"""
    return datetime.now(BEIJING_TZ).replace(tzinfo=None)

class MusicYorushika(db.Model):
    __tablename__ = 'music_yorushika'

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title        = db.Column(db.String(255), nullable=False)
    album        = db.Column(db.String(255))
    rating       = db.Column(db.String(255))
    link         = db.Column(db.String(255))
    release_year = db.Column(db.Integer)
    cover_path   = db.Column(db.String(255))

    def __repr__(self):
        return f'<Song {self.title}>'


