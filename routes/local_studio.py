"""Local-only link to the owner's visual studio (Yorushika-Lyric-Card-Bot).

Enabled only when ``STUDIO_URL`` is configured (the local preview runner sets
it; production never does). The browser talks to this app only, so the page
CSP stays ``'self'``; this app reads the studio's read-only showcase API and
forwards thumbnails. Nothing is stored, and the studio's frames never leave
the machine.
"""

import json
import re
import time
import unicodedata
import urllib.error
import urllib.request

from flask import Blueprint, Response, abort, current_app, jsonify, redirect, request, url_for

from models import MusicYorushika

local_studio_bp = Blueprint("local_studio", __name__)

_MEDIA_ID = re.compile(r"^[0-9a-f]{16,64}$")
_TIMEOUT = 8
_CACHE_SECONDS = 60
_cache = {}


def _studio_url():
    url = (current_app.config.get("STUDIO_URL") or "").rstrip("/")
    if not url:
        abort(404)
    return url


def normalize_title(value):
    """Compare titles loosely: full/half width, case and spaces.

    Studio scene labels such as "盗作 · 舞台剪影" name a concert set, not the
    song, so they are deliberately left unmatched.
    """
    text = unicodedata.normalize("NFKC", str(value or ""))
    return re.sub(r"\s+", "", text).casefold()


def _showcase(base):
    """The studio's showcase list, kept for a minute (it takes ~3 s to build)."""
    hit = _cache.get(base)
    if hit and time.monotonic() - hit[0] < _CACHE_SECONDS:
        return hit[1]
    try:
        with urllib.request.urlopen(f"{base}/api/showcase", timeout=_TIMEOUT) as resp:
            items = json.load(resp).get("items") or []
    except (OSError, ValueError, urllib.error.URLError):
        _cache.pop(base, None)
        return None
    _cache[base] = (time.monotonic(), items)
    return items


@local_studio_bp.route("/local/studio/frames/<slug>")
def frames(slug):
    base = _studio_url()
    song = MusicYorushika.query.filter_by(slug=slug, is_featured=True).first()
    if song is None:
        abort(404)
    items = _showcase(base)
    if items is None:
        return jsonify({"online": False, "frames": []})
    want = normalize_title(song.title_ja)
    public = (current_app.config.get("STUDIO_PUBLIC_URL") or base).rstrip("/")
    picked = []
    for item in items:
        if normalize_title(item.get("title")) != want:
            continue
        thumb = str(item.get("thumbnail") or "")
        media = thumb.rsplit("/", 1)[-1]
        if not thumb.startswith("/media/") or not _MEDIA_ID.match(media):
            continue
        cid = str(item.get("id") or "")
        lyric = item.get("lyric")
        picked.append(
            {
                "id": cid,
                "source": str(item.get("source_label") or ""),
                "timecode": str(item.get("timecode") or ""),
                "lyric": lyric.strip()[:160] if isinstance(lyric, str) and lyric.strip() else None,
                "image": url_for("local_studio.media", media_id=media),
                "href": f"{public}/#c={cid}&v={cid}",
            }
        )
    return jsonify({"online": True, "frames": picked})


def _frame_count(items, title):
    want = normalize_title(title)
    return sum(
        1
        for item in items
        if normalize_title(item.get("title")) == want
        and _MEDIA_ID.match(str(item.get("thumbnail") or "").removeprefix("/media/"))
        and str(item.get("thumbnail") or "").startswith("/media/")
    )


@local_studio_bp.route("/local/studio/songs")
def songs_with_frames():
    """Which songs have frames in the studio, so lists can mark them."""
    base = _studio_url()
    items = _showcase(base)
    if items is None:
        return jsonify({"online": False, "counts": {}})
    counts = {}
    for song in MusicYorushika.query.filter_by(is_featured=True).all():
        n = _frame_count(items, song.title_ja)
        if n:
            counts[song.slug] = n
    return jsonify({"online": True, "counts": counts})


@local_studio_bp.route("/local/studio/media/<media_id>")
def media(media_id):
    base = _studio_url()
    if not _MEDIA_ID.match(media_id):
        abort(404)
    try:
        with urllib.request.urlopen(f"{base}/media/{media_id}", timeout=_TIMEOUT) as resp:
            kind = resp.headers.get_content_type()
            if not kind.startswith("image/"):
                abort(404)
            body = resp.read(8 * 1024 * 1024)
    except (OSError, urllib.error.URLError):
        abort(404)
    return Response(body, mimetype=kind, headers={"Cache-Control": "private, max-age=3600"})


@local_studio_bp.route("/songs/by-title")
def song_by_title():
    """Let the console link a frame's title to the matching song page."""
    want = normalize_title(request.args.get("t", ""))
    if want:
        for song in MusicYorushika.query.filter_by(is_featured=True).all():
            if normalize_title(song.title_ja) == want:
                return redirect(url_for("main.song_detail", slug=song.slug))
    return redirect(url_for("main.search", q=request.args.get("t", "")))
