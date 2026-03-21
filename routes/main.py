from flask import Blueprint, render_template, url_for
import random
import datetime

from models import db, MusicYorushika
from utils import get_current_avatar

main_bp = Blueprint('main', __name__)

LYRIC_SNIPPETS = {
    'Sunny': 'Even if dawn comes, stay by my side.',
    'Spring Thief': 'Spring, come soon.',
    'Just a Sunny Day for You': 'If only the sky clears for you.',
    'Night Journey': 'I walk through the night thinking of you.',
    'Nautilus': 'Did you already forget?',
}


@main_bp.route('/')
def index():
    songs = MusicYorushika.query.all()

    if len(songs) > 10:
        yorushika_left = songs[:10]
        yorushika_right = songs[10:]
    else:
        yorushika_left = songs
        yorushika_right = []

    daily_song = None
    daily_lyric = ''
    if songs:
        seed = datetime.date.today().isoformat()
        rng = random.Random(seed)
        daily_song = rng.choice(songs)
        daily_lyric = LYRIC_SNIPPETS.get(daily_song.title, 'Music for tonight.')

    return render_template(
        'index.html',
        yorushika=yorushika_left,
        yorushika_right=yorushika_right,
        daily_song=daily_song,
        daily_lyric=daily_lyric,
    )


@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    year = request.args.get('year')
    sort_by = request.args.get('sort', 'hot_desc')

    sql_query = MusicYorushika.query

    if query:
        sql_query = sql_query.filter(
            (MusicYorushika.title.contains(query))
            | (MusicYorushika.album.contains(query))
        )

    if year and year.isdigit():
        sql_query = sql_query.filter_by(release_year=int(year))

    if sort_by == 'hot_desc':
        sql_query = sql_query.order_by(MusicYorushika.rating.desc())
    elif sort_by == 'hot_asc':
        sql_query = sql_query.order_by(MusicYorushika.rating.asc())
    elif sort_by == 'date_desc':
        sql_query = sql_query.order_by(MusicYorushika.release_year.desc())

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
    current_avatar = get_current_avatar()
    avatar_url = (
        current_avatar
        if current_avatar.startswith('http')
        else url_for('static', filename='uploads/' + current_avatar)
    )

    skills = [
        {'name': 'Python / Flask', 'progress': 90, 'color': 'success'},
        {'name': 'Linux / Ops', 'progress': 75, 'color': 'info'},
        {'name': 'MySQL / Database', 'progress': 80, 'color': 'warning'},
        {'name': 'Java / Backend', 'progress': 60, 'color': 'danger'},
    ]

    return render_template('about.html', skills=skills, avatar_url=avatar_url)
