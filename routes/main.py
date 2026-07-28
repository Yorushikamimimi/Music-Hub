import os
import random
import datetime

from flask import Blueprint, Response, abort, current_app, render_template, request
from sqlalchemy import or_

from models import db, MusicYorushika
from release_data import RELEASE_SLUGS_BY_TITLE, RELEASE_STORIES

main_bp = Blueprint('main', __name__)


def _featured_songs():
    return (
        MusicYorushika.query
        .filter_by(is_featured=True)
        .order_by(MusicYorushika.display_order.asc(), MusicYorushika.id.asc())
        .all()
    )


def _album_index(songs):
    albums = {}
    for song in songs:
        key = song.album_title or "未整理作品"
        if key not in albums:
            albums[key] = {
                "title": key,
                "release_year": song.release_year,
                "release_date": song.release_date,
                "release_type": song.release_type,
                "cover_path": song.cover_path,
                "source_url": song.source_url,
                "source_checked_at": song.source_checked_at,
                "detail_slug": RELEASE_SLUGS_BY_TITLE.get(key),
                "songs": [],
                "first_order": song.display_order,
            }
        albums[key]["songs"].append(song)
        if song.release_year and (
            albums[key]["release_year"] is None
            or song.release_year > albums[key]["release_year"]
        ):
            albums[key]["release_year"] = song.release_year
        if song.release_date and (
            albums[key]["release_date"] is None
            or song.release_date > albums[key]["release_date"]
        ):
            albums[key]["release_date"] = song.release_date

    return sorted(
        albums.values(),
        key=lambda album: (
            album["release_date"] is None,
            -(album["release_date"].toordinal() if album["release_date"] else 0),
            album["first_order"],
        ),
    )


@main_bp.route('/')
def index():
    songs = _featured_songs()

    daily_song = None
    daily_note = ''
    if songs:
        seed = datetime.date.today().isoformat()
        rng = random.Random(seed)
        daily_song = rng.choice(songs)
        daily_note = f"收录于《{daily_song.album_title}》"

    song_by_slug = {song.slug: song for song in songs}
    listening_paths = [
        {
            "eyebrow": "夜に歩く",
            "title": "沿着夜色行走",
            "description": "从《夜行》开始，进入行走、回望与无声告别的作品路径。",
            "song": song_by_slug.get("night-journey"),
        },
        {
            "eyebrow": "春を待つ",
            "title": "等待春天抵达",
            "description": "把春日的明亮和短暂放在一起听，感受季节流动的痕迹。",
            "song": song_by_slug.get("spring-thief"),
        },
        {
            "eyebrow": "雨の日記",
            "title": "雨天与日记",
            "description": "从雨、城市与书写出发，回到《エルマ》的叙事线索。",
            "song": song_by_slug.get("rain-with-cappuccino"),
        },
    ]

    albums = _album_index(songs)
    album_spotlights = sorted(
        albums,
        key=lambda album: (-len(album["songs"]), -(album["release_year"] or 0)),
    )[:4]

    return render_template(
        'index.html',
        daily_song=daily_song,
        daily_note=daily_note,
        featured_songs=songs[:6],
        total_song_count=len(songs),
        listening_paths=listening_paths,
        album_spotlights=album_spotlights,
    )


@main_bp.route('/discography')
def discography():
    songs = _featured_songs()
    selected_year = request.args.get('year', '').strip()
    selected_type = request.args.get('type', '').strip()

    years = sorted(
        {song.release_year for song in songs if song.release_year is not None},
        reverse=True,
    )
    release_types = sorted(
        {song.release_type for song in songs if song.release_type}
    )

    filtered_songs = [
        song for song in songs
        if (not selected_year or str(song.release_year) == selected_year)
        and (not selected_type or song.release_type == selected_type)
    ]

    return render_template(
        'discography.html',
        albums=_album_index(filtered_songs),
        years=years,
        release_types=release_types,
        selected_year=selected_year,
        selected_type=selected_type,
        result_count=len(filtered_songs),
    )


@main_bp.route('/songs/<slug>')
def song_detail(slug):
    songs = _featured_songs()
    song = next((item for item in songs if item.slug == slug), None)
    if song is None:
        abort(404)

    album_songs = [
        item for item in songs
        if item.album_title == song.album_title
    ]
    current_index = album_songs.index(song)
    previous_song = album_songs[current_index - 1] if current_index > 0 else None
    next_song = (
        album_songs[current_index + 1]
        if current_index + 1 < len(album_songs)
        else None
    )
    related_songs = [item for item in album_songs if item.id != song.id][:4]

    return render_template(
        'song_detail.html',
        song=song,
        previous_song=previous_song,
        next_song=next_song,
        related_songs=related_songs,
        release_detail_slug=RELEASE_SLUGS_BY_TITLE.get(song.album_title),
    )


@main_bp.route('/releases/<slug>')
def release_detail(slug):
    release = RELEASE_STORIES.get(slug)
    if release is None:
        abort(404)

    songs = [
        song for song in _featured_songs()
        if song.album_title == release["album_title"]
    ]
    if not songs:
        abort(404)

    songs_by_slug = {song.slug: song for song in songs}
    chapters = [
        {
            **chapter,
            "songs": [
                songs_by_slug[track_slug]
                for track_slug in chapter["track_slugs"]
                if track_slug in songs_by_slug
            ],
        }
        for chapter in release["chapters"]
    ]

    return render_template(
        'release_detail.html',
        release=release,
        songs=songs,
        chapters=chapters,
        track_badges=release["track_badges"],
        video_count=sum(bool(song.link) for song in songs),
    )


@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    year = request.args.get('year')
    sort_by = request.args.get('sort', 'editorial')

    sql_query = MusicYorushika.query.filter_by(is_featured=True)

    if query:
        sql_query = sql_query.filter(
            or_(
                MusicYorushika.title.contains(query),
                MusicYorushika.title_ja.contains(query),
                MusicYorushika.title_en.contains(query),
                MusicYorushika.album_title.contains(query),
            )
        )

    if year and year.isdigit():
        sql_query = sql_query.filter_by(release_year=int(year))

    if sort_by == 'date_desc':
        sql_query = sql_query.order_by(
            MusicYorushika.release_year.desc(),
            MusicYorushika.display_order.asc(),
        )
    elif sort_by == 'title_asc':
        sql_query = sql_query.order_by(MusicYorushika.title_ja.asc())
    else:
        sql_query = sql_query.order_by(
            MusicYorushika.display_order.asc(),
            MusicYorushika.id.asc(),
        )

    songs = sql_query.all()
    all_dates = (
        db.session.query(MusicYorushika.release_year)
        .distinct()
        .order_by(MusicYorushika.release_year.desc())
        .all()
    )
    years = [r[0] for r in all_dates if r[0] is not None]

    return render_template('search.html', songs=songs, years=years)


@main_bp.route('/about')
def about():
    songs = _featured_songs()
    albums = _album_index(songs)
    source_checked_dates = [
        song.source_checked_at
        for song in songs
        if song.source_checked_at is not None
    ]

    return render_template(
        'about.html',
        release_count=len(albums),
        song_count=len(songs),
        video_count=sum(bool(song.link) for song in songs),
        source_checked_at=max(source_checked_dates) if source_checked_dates else None,
    )


@main_bp.route('/lyrics')
def lyrics():
    keyword = request.args.get('q', '').strip()
    sql_query = MusicYorushika.query.filter_by(is_featured=True)

    if keyword:
        sql_query = sql_query.filter(
            or_(
                MusicYorushika.title.contains(keyword),
                MusicYorushika.title_ja.contains(keyword),
                MusicYorushika.title_en.contains(keyword),
                MusicYorushika.album_title.contains(keyword),
            )
        )

    songs = sql_query.order_by(
        MusicYorushika.release_year.desc(),
        MusicYorushika.display_order.asc(),
    ).all()
    stories = []
    for song in songs:
        stories.append({
            'title': song.title,
            'album_title': song.album_title,
            'release_type': song.release_type,
            'release_year': song.release_year,
            'link': song.link,
            'story': song.story_summary,
            'source_url': song.source_url,
        })

    return render_template('lyrics.html', stories=stories, keyword=keyword)


@main_bp.route('/radio')
def radio():
    station_name = os.getenv('RADIO_STATION_NAME', 'Yorushika Radio')
    stream_url = os.getenv('RADIO_STREAM_URL', '').strip()
    return render_template(
        'radio.html',
        station_name=station_name,
        stream_url=stream_url,
        private_mode=True,
    )


@main_bp.route('/robots.txt')
def robots():
    return Response(
        "User-agent: *\nDisallow: /\n",
        mimetype="text/plain",
    )


@main_bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('images/avatar-placeholder.svg')
