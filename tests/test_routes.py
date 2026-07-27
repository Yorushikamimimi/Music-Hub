import pytest

from models import MusicYorushika, db


@pytest.mark.parametrize(
    "path",
    ["/", "/search", "/lyrics", "/radio", "/about", "/robots.txt", "/favicon.ico"],
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


def test_about_has_real_github_link_and_no_placeholder_contact(client):
    page = client.get("/about").get_data(as_text=True)

    assert "https://github.com/Yorushikamimimi" in page
    assert "your_email@example.com" not in page


def test_radio_is_marked_private_and_never_autoplays(client):
    page = client.get("/radio").get_data(as_text=True)

    assert "私人聆听入口" in page
    assert "autoplay" not in page
    assert 'preload="none"' in page
    assert "Initial volume 25%" in page


def test_robots_disallows_all_crawlers(client):
    response = client.get("/robots.txt")
    assert response.get_data(as_text=True) == "User-agent: *\nDisallow: /\n"


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
