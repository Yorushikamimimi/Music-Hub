import pytest

from models import MusicYorushika, db


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/discography",
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
    assert 'aria-label="搜索作品"' in page


def test_discography_groups_tracks_and_supports_filters(client):
    page = client.get("/discography").get_data(as_text=True)

    assert "作品集" in page
    assert "89 首已核对曲目" in page
    assert "盗作" in page
    assert "14 首完整曲序" in page
    assert "音楽泥棒の自白" in page
    assert "2020.07.29" in page
    assert "资料核对：2026.07.28" in page
    assert 'href="https://www.bilibili.com/video/BV1gw411e7Dk/"' in page
    assert 'href="/songs/thoughtcrime"' in page

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
    assert "最后核对于 2026.07.28" in page
    assert "https://www.bilibili.com/video/BV16k8bzGE31/" in page
    assert "https://yorushika.com/discography/detail/18/" in page
    assert 'rel="noopener noreferrer"' in page


def test_song_sequence_stays_inside_the_same_release(client):
    page = client.get("/songs/night-journey").get_data(as_text=True)

    assert "幼年期、思い出の中" in page
    assert "花に亡霊" in page
    assert "アルジャーノン" not in page


def test_unknown_song_detail_returns_404(client):
    assert client.get("/songs/not-in-catalog").status_code == 404


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
    assert "8 <span>部</span>" in page
    assert "89 <span>首</span>" in page
    assert "24 <span>首</span>" in page
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
