import os
import random
import datetime

from flask import Blueprint, Response, current_app, render_template, request, url_for
from sqlalchemy import or_

from models import db, MusicYorushika

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    songs = (
        MusicYorushika.query
        .filter_by(is_featured=True)
        .order_by(MusicYorushika.display_order.asc(), MusicYorushika.id.asc())
        .all()
    )

    if len(songs) > 10:
        yorushika_left = songs[:10]
        yorushika_right = songs[10:]
    else:
        yorushika_left = songs
        yorushika_right = []

    daily_song = None
    daily_note = ''
    if songs:
        seed = datetime.date.today().isoformat()
        rng = random.Random(seed)
        daily_song = rng.choice(songs)
        daily_note = f"收录于《{daily_song.album_title}》"

    return render_template(
        'index.html',
        yorushika=yorushika_left,
        yorushika_right=yorushika_right,
        daily_song=daily_song,
        daily_note=daily_note,
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
    avatar_url = url_for('static', filename='images/avatar-placeholder.svg')

    skills = [
        {'name': 'Python / Flask', 'progress': 90, 'color': 'success'},
        {'name': 'Linux / Ops', 'progress': 75, 'color': 'info'},
        {'name': 'MySQL / Database', 'progress': 80, 'color': 'warning'},
        {'name': 'Java / Backend', 'progress': 60, 'color': 'danger'},
    ]

    return render_template('about.html', skills=skills, avatar_url=avatar_url)


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
