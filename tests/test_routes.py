import pytest

from catalog_data import CATALOG_RELEASES
from models import MusicYorushika, db
from release_data import RELEASE_STORIES


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/discography",
        "/releases/tousaku",
        "/releases/dakara-boku-wa-ongaku-wo-yameta",
        "/releases/elma",
        "/releases/gentou",
        "/releases/sousaku",
        "/releases/makeinu-ni-encore-wa-iranai",
        "/releases/natsukusa-ga-jama-wo-suru",
        "/releases/haru",
        "/releases/nininsyou",
        "/releases/abuku",
        "/songs/spring-thief",
        "/search",
        "/lyrics",
        "/radio",
        "/about",
        "/healthz",
        "/robots.txt",
        "/favicon.ico",
    ],
)
def test_primary_routes_are_available(client, path):
    response = client.get(path)
    assert response.status_code == 200


def test_search_matches_japanese_title_and_real_album(client):
    response = client.get("/search", query_string={"q": "春泥棒"})
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Spring Thief (春泥棒)" in page
    assert "創作" in page
    assert 'href="/songs/spring-thief"' in page


def test_home_uses_archive_identity_and_internal_listening_paths(client):
    page = client.get("/").get_data(as_text=True)

    assert "夜鹿集" in page
    assert "从一首歌开始" in page
    assert "按此刻的心情进入" in page
    assert "Yorushika Picks" not in page
    assert "rank-num" not in page
    assert 'href="/discography"' in page
    assert 'href="/songs/night-journey"' in page
    assert 'href="/search"' in page
    assert 'href="/releases/tousaku"' in page
    assert 'href="/releases/nininsyou"' in page
    assert 'aria-label="搜索作品"' in page


def test_discography_groups_tracks_and_supports_filters(client):
    page = client.get("/discography").get_data(as_text=True)

    assert "作品集" in page
    assert "122 个已核对曲序位置" in page
    assert "22 个作品集合" in page
    assert "二人称" in page
    assert "20 首完整曲序" in page
    assert "盗作" in page
    assert "14 首完整曲序" in page
    assert "音楽泥棒の自白" in page
    assert "2020.07.29" in page
    assert "资料核对：2026.07.29" in page
    assert "Yorushika 官方艺人目录中的音乐发行" in page
    assert "不含 Live 影像制品、书简型小说" in page
    assert "不代表官方授权" in page
    assert 'href="https://www.bilibili.com/video/BV1gw411e7Dk/"' in page
    assert 'href="/releases/tousaku"' in page
    assert 'href="/songs/thoughtcrime?release=tousaku"' in page

    filtered = client.get(
        "/discography",
        query_string={"year": "2021", "type": "EP"},
    ).get_data(as_text=True)
    assert "創作" in filtered
    assert "春泥棒" in filtered
    assert "盗作" not in filtered


def test_song_detail_separates_facts_note_and_official_source(client):
    page = client.get("/songs/spring-thief").get_data(as_text=True)

    assert "<h1>" in page
    assert ">春泥棒</a>" in page
    assert "Spring Thief" in page
    assert "收录作品" in page
    assert "个人整理" in page
    assert "在 B 站观看影像" in page
    assert "发行日期" in page
    assert "2021.01.27" in page
    assert "第 2 首" in page
    assert "最后核对于 2026.07.29" in page
    assert "仅确认页面可达且标题与曲目相符" in page
    assert "不代表官方授权" in page
    assert "https://www.bilibili.com/video/BV16k8bzGE31/" in page
    assert "https://yorushika.com/discography/detail/18/" in page
    assert 'rel="noopener noreferrer"' in page


def test_song_sequence_stays_inside_the_same_release(client):
    page = client.get("/songs/night-journey").get_data(as_text=True)

    assert "幼年期、思い出の中" in page
    assert "花に亡霊" in page
    assert "アルジャーノン" not in page


def test_shared_song_uses_requested_release_context(client):
    album_page = client.get(
        "/songs/haru",
        query_string={"release": "nininsyou"},
    ).get_data(as_text=True)
    single_page = client.get("/songs/haru").get_data(as_text=True)

    assert "《二人称》" in album_page
    assert "第 7 首" in album_page
    assert "这首歌出现在哪些作品中" in album_page
    assert "《晴る》" in single_page
    assert "第 1 首" in single_page
    assert 'href="/songs/haru?release=nininsyou"' in single_page


def test_legacy_duplicate_track_urls_redirect_to_canonical_song(client):
    response = client.get("/songs/bakudanma-tousaku")
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/songs/bakudanma")

    response = client.get("/songs/kutsu-no-hanabi-natsukusa")
    assert response.status_code == 301
    assert response.headers["Location"].endswith("/songs/kutsu-no-hanabi")


def test_search_matches_release_title_across_shared_memberships(client):
    page = client.get("/search", query_string={"q": "二人称"}).get_data(
        as_text=True
    )

    assert "雲になる" in page
    assert "Sunny (晴る)" in page
    assert "Hitchcock (ヒッチコック)" in page
    assert page.count('data-song-album="二人称"') == 20
    assert 'href="/songs/haru?release=nininsyou"' in page
    assert 'href="/songs/hitchcock?release=nininsyou"' in page


def test_unknown_song_detail_returns_404(client):
    assert client.get("/songs/not-in-catalog").status_code == 404


def test_tousaku_release_archive_separates_sources_and_editorial_paths(client):
    page = client.get("/releases/tousaku").get_data(as_text=True)

    assert "作品档案" in page
    assert "官方公开信息" in page
    assert "本站聆听笔记" in page
    assert "个人整理 · 非官方章节划分" in page
    assert "十四首完整曲序" in page
    assert "约 130 页小说《盗作》" in page
    assert "器乐过场" in page
    assert "自白与侵入" in page
    assert "复制与盛夏" in page
    assert "逃亡与回望" in page
    assert 'href="/songs/thoughtcrime?release=tousaku"' in page
    assert 'href="https://www.bilibili.com/video/BV1gw411e7Dk/"' in page
    assert "https://yorushika.com/discography/detail/15/" in page
    assert "https://yorushika.com/news/detail/11126" in page
    assert "https://sp.universal-music.co.jp/yorushika/tousaku/" in page
    assert "完整歌词" in page


def test_dakara_boku_release_archive_keeps_facts_and_notes_separate(client):
    page = client.get(
        "/releases/dakara-boku-wa-ongaku-wo-yameta"
    ).get_data(as_text=True)

    assert "作品档案" in page
    assert "官方公开信息" in page
    assert "本站聆听笔记" in page
    assert "个人整理 · 非官方章节划分" in page
    assert "首张 Full Album" in page
    assert "写给エルマ的信" in page
    assert "故事舞台设在瑞典" in page
    assert "八月与出发" in page
    assert "季节与创作" in page
    assert "写给エルマ的告别" in page
    assert "日期节点" in page
    assert page.count('class="release-track-main"') == 14
    assert page.count('class="release-track-video"') == 4
    assert (
        'href="/songs/deep-indigo?release='
        'dakara-boku-wa-ongaku-wo-yameta"'
        in page
    )
    assert (
        'href="https://www.bilibili.com/video/BV1HA411973b/"'
        in page
    )
    assert "https://yorushika.com/discography/detail/6/" in page
    assert "https://store.universal-music.co.jp/products/dued1266" in page
    assert "https://sp.universal-music.co.jp/yorushika/elma/" in page
    assert "双作关系特设页" in page


def test_every_catalog_release_has_a_complete_archive(client):
    for catalog_release in CATALOG_RELEASES:
        slug = catalog_release["slug"]
        response = client.get(f"/releases/{slug}")
        page = response.get_data(as_text=True)
        catalog_track_slugs = [
            track_slug for track_slug, _title in catalog_release["tracks"]
        ]

        assert response.status_code == 200
        assert page.count('class="release-track-main"') == len(
            catalog_track_slugs
        )
        assert catalog_release["source_url"] in page
        assert all(
            f'href="/songs/{track_slug}?release={slug}"' in page
            for track_slug in catalog_track_slugs
        )
        if slug in RELEASE_STORIES:
            story = RELEASE_STORIES[slug]
            chapter_track_slugs = [
                track_slug
                for chapter in story["chapters"]
                for track_slug in chapter["track_slugs"]
            ]
            assert story["official_summary"] in page
            assert chapter_track_slugs == catalog_track_slugs
        else:
            assert "尚未加入没有可靠来源的背景解读" in page
            assert "资料来源与边界" in page


@pytest.mark.parametrize(
    ("slug", "track_count", "fact", "path_title"),
    [
        ("elma", 14, "エルマ写下的日记本", "沿着三段路径"),
        ("gentou", 25, "可聆听画集", "沿着两段路径"),
        ("sousaku", 5, "没有 CD 的 CD", "沿着两段路径"),
        (
            "makeinu-ni-encore-wa-iranai",
            9,
            "booklet《生まれ変わり》",
            "沿着三段路径",
        ),
        (
            "natsukusa-ga-jama-wo-suru",
            7,
            "第一张 Mini Album",
            "沿着三段路径",
        ),
        ("haru", 1, "《葬送的芙莉莲》", "从一条路径进入"),
    ],
)
def test_new_release_archives_keep_source_facts_and_full_tracklists(
    client,
    slug,
    track_count,
    fact,
    path_title,
):
    page = client.get(f"/releases/{slug}").get_data(as_text=True)

    assert "官方公开信息" in page
    assert "本站聆听笔记" in page
    assert fact in page
    assert path_title in page
    assert page.count('class="release-track-main"') == track_count
    assert "资料来源与边界" in page


def test_unknown_release_archive_returns_404(client):
    assert client.get("/releases/not-in-archive").status_code == 404


def test_stories_use_curated_summaries_and_official_links(client):
    response = client.get("/lyrics", query_string={"q": "盗作"})
    page = response.get_data(as_text=True)

    assert "Plagiarism (盗作)" in page
    assert "官方收录信息" in page
    assert "https://yorushika.com/discography/" in page
    assert "完整歌词" in page


def test_no_fake_hot_labels_remain(client):
    assert "HOT" not in client.get("/").get_data(as_text=True)
    assert "HOT" not in client.get("/search").get_data(as_text=True)


def test_mobile_navigation_and_landmarks_are_present(client):
    page = client.get("/").get_data(as_text=True)

    assert 'id="mobile-nav-toggle"' in page
    assert 'aria-controls="site-nav"' in page
    assert 'aria-expanded="false"' in page
    assert 'href="#main-content"' in page
    assert '<main id="main-content"' in page


def test_about_explains_archive_identity_scope_and_boundaries(client):
    page = client.get("/about").get_data(as_text=True)

    assert "关于夜鹿集" in page
    assert "它不是一份热度榜" in page
    assert "22 <span>部</span>" in page
    assert "109 <span>首</span>" in page
    assert "122 <span>条</span>" in page
    assert "24 <span>首</span>" in page
    assert "独立曲目" in page
    assert "曲序位置" in page
    assert "Yorushika 官方艺人目录中的音乐发行" in page
    assert "已核对 22 部作品" in page
    assert "不含 Live 影像制品、书简型小说" in page
    assert "不代表官方授权或长期可用" in page
    assert "当前只收录已经逐项核对的八部作品" not in page
    assert "资料有出处" in page
    assert "感受是个人笔记" in page
    assert "聆听保持私人" in page
    assert "不提供" in page
    assert "Full Stack Aspirant" not in page
    assert "Open to Work" not in page
    assert "技术栈" not in page


def test_radio_is_marked_private_and_never_autoplays(client):
    page = client.get("/radio").get_data(as_text=True)

    assert "私人聆听入口" in page
    assert "autoplay" not in page
    assert 'preload="none"' in page
    assert "Initial volume 25%" in page


def test_robots_disallows_all_crawlers(client):
    response = client.get("/robots.txt")
    assert response.get_data(as_text=True) == "User-agent: *\nDisallow: /\n"


def test_health_endpoint_reports_database_failures(app, client, monkeypatch):
    with app.app_context():
        monkeypatch.setattr(
            db.session,
            "execute",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("offline")),
        )
        response = client.get("/healthz")

    assert response.status_code == 503
    assert response.get_json() == {"status": "unhealthy"}


def test_uncurated_database_rows_remain_private(app, client):
    with app.app_context():
        db.session.add(
            MusicYorushika(
                title="Uncurated legacy row",
                source_url="https://example.com/not-approved",
                is_featured=False,
            )
        )
        db.session.commit()

    assert "Uncurated legacy row" not in client.get("/").get_data(as_text=True)
    assert "Uncurated legacy row" not in client.get("/search").get_data(as_text=True)
    assert "Uncurated legacy row" not in client.get("/lyrics").get_data(as_text=True)
