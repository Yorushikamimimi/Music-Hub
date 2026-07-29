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
    release_date = db.Column(db.Date)
    track_number = db.Column(db.Integer, nullable=False, default=0)
    cover_path = db.Column(db.String(255))
    link = db.Column(db.String(500))
    story_summary = db.Column(db.Text)
    source_url = db.Column(db.String(500))
    source_checked_at = db.Column(db.Date)
    display_order = db.Column(db.Integer, nullable=False, default=0, index=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=beijing_now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=beijing_now,
        onupdate=beijing_now,
    )
    release_links = db.relationship(
        'YorushikaReleaseTrack',
        back_populates='track',
        cascade='all, delete-orphan',
        order_by='YorushikaReleaseTrack.track_number',
    )

    def __repr__(self):
        return f'<Song {self.title}>'


class YorushikaRelease(db.Model):
    __tablename__ = 'yorushika_release'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    release_type = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.Date, nullable=False, index=True)
    cover_path = db.Column(db.String(255), nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    source_checked_at = db.Column(db.Date, nullable=False)
    display_order = db.Column(db.Integer, nullable=False, default=0, index=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=beijing_now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=beijing_now,
        onupdate=beijing_now,
    )
    track_links = db.relationship(
        'YorushikaReleaseTrack',
        back_populates='release',
        cascade='all, delete-orphan',
        order_by='YorushikaReleaseTrack.track_number',
    )

    @property
    def release_year(self):
        return self.release_date.year

    def __repr__(self):
        return f'<Release {self.title}>'


class YorushikaReleaseTrack(db.Model):
    __tablename__ = 'yorushika_release_track'
    __table_args__ = (
        db.UniqueConstraint(
            'release_id',
            'track_number',
            name='uq_yorushika_release_track_number',
        ),
    )

    release_id = db.Column(
        db.Integer,
        db.ForeignKey('yorushika_release.id', ondelete='CASCADE'),
        primary_key=True,
    )
    track_id = db.Column(
        db.Integer,
        db.ForeignKey('music_yorushika.id', ondelete='CASCADE'),
        primary_key=True,
    )
    track_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=beijing_now)

    release = db.relationship('YorushikaRelease', back_populates='track_links')
    track = db.relationship('MusicYorushika', back_populates='release_links')

    def __repr__(self):
        return (
            f'<ReleaseTrack release={self.release_id} '
            f'track={self.track_id} number={self.track_number}>'
        )
