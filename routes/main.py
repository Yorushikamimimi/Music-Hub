import random
import datetime

from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import or_

from catalog_data import (
    CATALOG_SCOPE_URL,
    LEGACY_TRACK_SLUG_ALIASES,
    VIDEO_LINKS_REVIEWED_ON,
)
from models import (
    db,
    MusicYorushika,
    YorushikaRelease,
    YorushikaReleaseTrack,
)
from release_data import RELEASE_STORIES

main_bp = Blueprint('main', __name__)

_CHINESE_COUNTS = {
    1: "一",
    2: "两",
    3: "三",
    4: "四",
    5: "五",
    7: "七",
    9: "九",
    14: "十四",
    20: "二十",
    22: "二十二",
    25: "二十五",
}


def _chinese_count(value):
    return _CHINESE_COUNTS.get(value, str(value))


def _featured_songs():
    return (
        MusicYorushika.query
        .filter_by(is_featured=True)
        .order_by(MusicYorushika.display_order.asc(), MusicYorushika.id.asc())
        .all()
    )


def _featured_releases():
    return (
        YorushikaRelease.query
        .filter_by(is_featured=True)
        .order_by(
            YorushikaRelease.release_date.desc(),
            YorushikaRelease.display_order.asc(),
        )
        .all()
    )


class ReleaseTrackView:
    """Expose a track with its position inside one specific release."""

    def __init__(self, membership, include_release_context=False):
        self.membership = membership
        self.track = membership.track
        self.release = membership.release
        self.track_number = membership.track_number
        self.include_release_context = include_release_context

    def __getattr__(self, name):
        return getattr(self.track, name)

    @property
    def album_title(self):
        return self.release.title

    @property
    def release_type(self):
        return self.release.release_type

    @property
    def release_year(self):
        return self.release.release_year

    @property
    def release_date(self):
        return self.release.release_date

    @property
    def cover_path(self):
        return self.release.cover_path

    @property
    def source_url(self):
        return self.release.source_url

    @property
    def source_checked_at(self):
        return self.release.source_checked_at


def _release_index(releases):
    return [
        {
            "slug": release.slug,
            "title": release.title,
            "release_year": release.release_year,
            "release_date": release.release_date,
            "release_type": release.release_type,
            "cover_path": release.cover_path,
            "source_url": release.source_url,
            "source_checked_at": release.source_checked_at,
            "detail_slug": release.slug,
            "songs": [
                ReleaseTrackView(membership)
                for membership in release.track_links
                if membership.track.is_featured
            ],
            "first_order": release.display_order,
        }
        for release in releases
    ]


def _release_context(song, requested_slug=None):
    links = [
        membership
        for membership in song.release_links
        if membership.release.is_featured
    ]
    if requested_slug:
        requested = next(
            (
                membership
                for membership in links
                if membership.release.slug == requested_slug
            ),
            None,
        )
        if requested is not None:
            return ReleaseTrackView(requested)

    primary = next(
        (
            membership
            for membership in links
            if membership.release.title == song.album_title
        ),
        None,
    )
    if primary is not None:
        return ReleaseTrackView(primary)
    if links:
        return ReleaseTrackView(
            max(links, key=lambda membership: membership.release.release_date)
        )
    return None


def _search_context(song, query="", selected_year=None):
    """Keep a release-title/year search result inside the matched release."""
    links = [
        membership
        for membership in song.release_links
        if membership.release.is_featured
    ]
    normalized_query = query.strip().casefold()
    if normalized_query:
        release_match = next(
            (
                membership
                for membership in links
                if normalized_query in membership.release.title.casefold()
            ),
            None,
        )
        if release_match is not None:
            return ReleaseTrackView(
                release_match,
                include_release_context=True,
            )

    if selected_year is not None:
        year_match = next(
            (
                membership
                for membership in links
                if membership.release.release_year == selected_year
            ),
            None,
        )
        if year_match is not None:
            return ReleaseTrackView(
                year_match,
                include_release_context=True,
            )

    return _release_context(song)


@main_bp.route('/')
def index():
    songs = _featured_songs()
    releases = _featured_releases()

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

    albums = _release_index(releases)
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
    releases = _featured_releases()
    selected_year = request.args.get('year', '').strip()
    selected_type = request.args.get('type', '').strip()

    years = sorted(
        {release.release_year for release in releases},
        reverse=True,
    )
    release_types = sorted(
        {release.release_type for release in releases}
    )

    filtered_releases = [
        release for release in releases
        if (not selected_year or str(release.release_year) == selected_year)
        and (not selected_type or release.release_type == selected_type)
    ]
    albums = _release_index(filtered_releases)

    return render_template(
        'discography.html',
        albums=albums,
        years=years,
        release_types=release_types,
        selected_year=selected_year,
        selected_type=selected_type,
        result_count=sum(len(album["songs"]) for album in albums),
        catalog_scope_url=CATALOG_SCOPE_URL,
        video_links_reviewed_on=VIDEO_LINKS_REVIEWED_ON,
    )


@main_bp.route('/songs/<slug>')
def song_detail(slug):
    canonical_slug = LEGACY_TRACK_SLUG_ALIASES.get(slug)
    if canonical_slug:
        return redirect(
            url_for(
                'main.song_detail',
                slug=canonical_slug,
                release=request.args.get('release'),
            ),
            code=301,
        )

    song = MusicYorushika.query.filter_by(
        slug=slug,
        is_featured=True,
    ).first()
    if song is None:
        abort(404)

    release_context = _release_context(
        song,
        requested_slug=request.args.get('release', '').strip(),
    )
    if release_context is None:
        abort(404)

    release_songs = [
        ReleaseTrackView(membership)
        for membership in release_context.release.track_links
        if membership.track.is_featured
    ]
    current_index = next(
        index
        for index, item in enumerate(release_songs)
        if item.id == song.id
    )
    previous_song = (
        release_songs[current_index - 1]
        if current_index > 0
        else None
    )
    next_song = (
        release_songs[current_index + 1]
        if current_index + 1 < len(release_songs)
        else None
    )
    related_songs = [
        item for item in release_songs if item.id != song.id
    ][:4]
    release_appearances = sorted(
        [
            ReleaseTrackView(membership)
            for membership in song.release_links
            if membership.release.is_featured
        ],
        key=lambda item: item.release.release_date,
        reverse=True,
    )

    return render_template(
        'song_detail.html',
        song=song,
        release_context=release_context,
        release_appearances=release_appearances,
        previous_song=previous_song,
        next_song=next_song,
        related_songs=related_songs,
        video_links_reviewed_on=VIDEO_LINKS_REVIEWED_ON,
    )


@main_bp.route('/releases/<slug>')
def release_detail(slug):
    catalog_release = YorushikaRelease.query.filter_by(
        slug=slug,
        is_featured=True,
    ).first()
    if catalog_release is None:
        abort(404)

    songs = [
        ReleaseTrackView(membership)
        for membership in catalog_release.track_links
        if membership.track.is_featured
    ]
    if not songs:
        abort(404)

    release = RELEASE_STORIES.get(slug)
    if release is None:
        return render_template(
            'release_overview.html',
            release=catalog_release,
            songs=songs,
            video_count=sum(bool(song.link) for song in songs),
            video_links_reviewed_on=VIDEO_LINKS_REVIEWED_ON,
        )

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
    secondary_source = None
    if len(release["sources"]) > 1:
        secondary_source = release["sources"][
            release.get("secondary_source_index", 1)
        ]
    chapter_count = len(chapters)
    listening_path_title = (
        "从一条路径进入这部作品"
        if chapter_count == 1
        else f"沿着{_chinese_count(chapter_count)}段路径听完整部作品"
    )

    return render_template(
        'release_detail.html',
        release=release,
        catalog_release=catalog_release,
        songs=songs,
        chapters=chapters,
        track_badges=release["track_badges"],
        video_count=sum(bool(song.link) for song in songs),
        secondary_source=secondary_source,
        listening_path_title=listening_path_title,
        tracklist_title=f"{_chinese_count(len(songs))}首完整曲序",
        video_links_reviewed_on=VIDEO_LINKS_REVIEWED_ON,
    )


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    year = request.args.get('year')
    sort_by = request.args.get('sort', 'editorial')
    selected_year = int(year) if year and year.isdigit() else None

    sql_query = MusicYorushika.query.filter_by(is_featured=True)

    if query:
        sql_query = sql_query.filter(
            or_(
                MusicYorushika.title.contains(query),
                MusicYorushika.title_ja.contains(query),
                MusicYorushika.title_en.contains(query),
                MusicYorushika.album_title.contains(query),
                MusicYorushika.release_links.any(
                    YorushikaReleaseTrack.release.has(
                        YorushikaRelease.title.contains(query)
                    )
                ),
            )
        )

    if selected_year is not None:
        release_ids = [
            release.id
            for release in _featured_releases()
            if release.release_year == selected_year
        ]
        sql_query = sql_query.filter(
            MusicYorushika.release_links.any(
                YorushikaReleaseTrack.release_id.in_(release_ids)
            )
        )

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

    songs = [
        context
        for song in sql_query.all()
        if (context := _search_context(song, query, selected_year)) is not None
    ]
    years = sorted(
        {release.release_year for release in _featured_releases()},
        reverse=True,
    )

    return render_template('search.html', songs=songs, years=years)


@main_bp.route('/about')
def about():
    songs = _featured_songs()
    releases = _featured_releases()
    source_checked_dates = [
        release.source_checked_at
        for release in releases
        if release.source_checked_at is not None
    ]

    return render_template(
        'about.html',
        release_count=len(releases),
        song_count=len(songs),
        placement_count=sum(len(release.track_links) for release in releases),
        video_count=sum(bool(song.link) for song in songs),
        source_checked_at=max(source_checked_dates) if source_checked_dates else None,
        catalog_scope_url=CATALOG_SCOPE_URL,
        video_links_reviewed_on=VIDEO_LINKS_REVIEWED_ON,
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
                MusicYorushika.release_links.any(
                    YorushikaReleaseTrack.release.has(
                        YorushikaRelease.title.contains(keyword)
                    )
                ),
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
    return render_template(
        'radio.html',
        station_name=current_app.config['RADIO_STATION_NAME'],
        stream_url=current_app.config['RADIO_STREAM_URL'],
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
