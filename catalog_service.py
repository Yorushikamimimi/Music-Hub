"""Catalog synchronization helpers used by deployment and tests."""

from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import or_

from catalog_data import (
    CATALOG_REVIEWED_ON,
    CATALOG_RELEASES,
    CATALOG_RELEASE_TRACKS,
    CATALOG_TRACKS,
    LEGACY_TRACK_SLUG_ALIASES,
)
from models import (
    MusicYorushika,
    YorushikaRelease,
    YorushikaReleaseTrack,
    db,
)


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
    release_created = 0
    release_updated = 0
    canonical_aliases = {}
    for legacy_slug, canonical_slug in LEGACY_TRACK_SLUG_ALIASES.items():
        canonical_aliases.setdefault(canonical_slug, []).append(legacy_slug)

    for display_order, track in enumerate(CATALOG_TRACKS, start=1):
        song = MusicYorushika.query.filter_by(slug=track["slug"]).first()
        if song is None:
            for legacy_slug in canonical_aliases.get(track["slug"], ()):
                song = MusicYorushika.query.filter_by(slug=legacy_slug).first()
                if song is not None:
                    break
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

    canonical_slugs = {track["slug"] for track in CATALOG_TRACKS}
    for legacy_slug, canonical_slug in LEGACY_TRACK_SLUG_ALIASES.items():
        if canonical_slug not in canonical_slugs:
            continue
        legacy_song = MusicYorushika.query.filter_by(slug=legacy_slug).first()
        if legacy_song is not None:
            legacy_song.is_featured = False

    releases_by_slug = {}
    for display_order, release_data in enumerate(CATALOG_RELEASES, start=1):
        release = YorushikaRelease.query.filter_by(
            slug=release_data["slug"],
        ).first()
        if release is None:
            release = YorushikaRelease()
            db.session.add(release)
            release_created += 1
        else:
            release_updated += 1

        release.slug = release_data["slug"]
        release.title = release_data["title"]
        release.release_type = release_data["release_type"]
        release.release_date = release_data["release_date"]
        release.cover_path = release_data["cover_path"]
        release.source_url = _clean_external_url(release_data["source_url"])
        release.source_checked_at = CATALOG_REVIEWED_ON
        release.display_order = display_order
        release.is_featured = True
        releases_by_slug[release.slug] = release

    db.session.flush()
    tracks_by_slug = {
        song.slug: song
        for song in MusicYorushika.query.filter(
            MusicYorushika.slug.in_(canonical_slugs)
        ).all()
    }
    for release in releases_by_slug.values():
        release.track_links.clear()
    db.session.flush()

    for membership in CATALOG_RELEASE_TRACKS:
        db.session.add(
            YorushikaReleaseTrack(
                release=releases_by_slug[membership["release_slug"]],
                track=tracks_by_slug[membership["track_slug"]],
                track_number=membership["track_number"],
            )
        )

    if commit:
        db.session.commit()
    else:
        db.session.flush()

    return {
        "created": created,
        "updated": updated,
        "total": len(CATALOG_TRACKS),
        "releases_created": release_created,
        "releases_updated": release_updated,
        "releases_total": len(CATALOG_RELEASES),
        "placements_total": len(CATALOG_RELEASE_TRACKS),
    }
