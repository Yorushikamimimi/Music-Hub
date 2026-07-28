"""Catalog synchronization helpers used by deployment and tests."""

from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import or_

from catalog_data import CATALOG_TRACKS
from models import MusicYorushika, db


def _clean_external_url(url: str | None) -> str | None:
    if not url:
        return None
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in {
        "yorushika.com",
        "www.yorushika.com",
    }:
        return None
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _clean_bilibili_url(url: str | None) -> str | None:
    if not url:
        return None
    parts = urlsplit(url)
    if (
        parts.scheme != "https"
        or parts.hostname not in {"bilibili.com", "www.bilibili.com"}
        or not parts.path.startswith("/video/BV")
    ):
        return None
    return urlunsplit(("https", "www.bilibili.com", parts.path, "", ""))


def sync_catalog(commit: bool = True) -> dict:
    """Upsert curated catalog rows without deleting unknown records."""
    created = 0
    updated = 0

    for display_order, track in enumerate(CATALOG_TRACKS, start=1):
        song = MusicYorushika.query.filter_by(slug=track["slug"]).first()
        unclaimed_legacy_row = or_(
            MusicYorushika.slug.is_(None),
            MusicYorushika.slug == "",
        )
        if song is None:
            song = MusicYorushika.query.filter(
                unclaimed_legacy_row,
                MusicYorushika.cover_path
                == track["cover_path"].replace(".webp", ".jpg"),
            ).first()
        if song is None and track["title_en"]:
            song = MusicYorushika.query.filter(
                unclaimed_legacy_row,
                MusicYorushika.title.contains(track["title_en"])
            ).first()

        if song is None:
            song = MusicYorushika()
            db.session.add(song)
            created += 1
        else:
            updated += 1

        song.slug = track["slug"]
        song.title = track["title"]
        song.title_ja = track["title_ja"]
        song.title_en = track["title_en"]
        song.album_title = track["album_title"]
        song.release_type = track["release_type"]
        song.release_year = track["release_year"]
        song.release_date = track["release_date"]
        song.track_number = track["track_number"]
        song.cover_path = track["cover_path"]
        song.link = _clean_bilibili_url(track.get("mv_url"))
        song.story_summary = track["story_summary"]
        song.source_url = _clean_external_url(track["source_url"])
        song.source_checked_at = track["source_checked_at"]
        song.display_order = display_order
        song.is_featured = True

    if commit:
        db.session.commit()
    else:
        db.session.flush()

    return {"created": created, "updated": updated, "total": len(CATALOG_TRACKS)}
