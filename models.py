from datetime import datetime, timedelta, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Beijing time (UTC+8) is used for human-facing timestamps.
BEIJING_TZ = timezone(timedelta(hours=8))


def beijing_now():
    """Return the current naive Beijing time for database compatibility."""
    return datetime.now(BEIJING_TZ).replace(tzinfo=None)


class MusicYorushika(db.Model):
    __tablename__ = 'music_yorushika'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(120), unique=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    title_ja = db.Column(db.String(255))
    title_en = db.Column(db.String(255))
    album_title = db.Column(db.String(255))
    release_type = db.Column(db.String(80))
    release_year = db.Column(db.Integer, index=True)
    cover_path = db.Column(db.String(255))
    link = db.Column(db.String(500))
    story_summary = db.Column(db.Text)
    source_url = db.Column(db.String(500))
    display_order = db.Column(db.Integer, nullable=False, default=0, index=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=beijing_now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=beijing_now,
        onupdate=beijing_now,
    )

    def __repr__(self):
        return f'<Song {self.title}>'
