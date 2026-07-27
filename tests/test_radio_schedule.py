import json

from scripts import generate_radio_schedule


def test_playlist_only_includes_curated_yorushika_files(tmp_path):
    first = tmp_path / f"{generate_radio_schedule.PLAYLIST_ORDER[0]}.mp3"
    second = tmp_path / f"{generate_radio_schedule.PLAYLIST_ORDER[1]}.mp3"
    unknown = tmp_path / "unreviewed-track.mp3"
    for path in (first, second, unknown):
        path.touch()

    assert generate_radio_schedule.ordered_music_files(tmp_path) == [first, second]
    assert len(generate_radio_schedule.PLAYLIST_ORDER) == 24
    assert set(generate_radio_schedule.PLAYLIST_ORDER) == set(
        generate_radio_schedule.TITLE_OVERRIDES
    )


def test_generated_schedule_is_private(tmp_path, monkeypatch):
    music_dir = tmp_path / "music"
    runtime_dir = tmp_path / "runtime"
    music_dir.mkdir()
    track_stem = generate_radio_schedule.PLAYLIST_ORDER[0]
    (music_dir / f"{track_stem}.mp3").touch()

    monkeypatch.setenv("RADIO_MUSIC_DIR", str(music_dir))
    monkeypatch.setenv("RADIO_RUNTIME_DIR", str(runtime_dir))
    monkeypatch.setattr(generate_radio_schedule, "duration_for", lambda _path: 180.0)
    monkeypatch.setattr(generate_radio_schedule.time, "time", lambda: 1000.0)

    generate_radio_schedule.main()

    schedule = json.loads(
        (runtime_dir / "hls" / "radio-schedule.json").read_text(encoding="utf-8")
    )
    assert schedule["private"] is True
    assert schedule["tracks"] == [
        {
            "title": generate_radio_schedule.TITLE_OVERRIDES[track_stem],
            "artist": "Yorushika",
            "duration": 180.0,
        }
    ]
    assert "unreviewed" not in (runtime_dir / "playlist.txt").read_text(
        encoding="utf-8"
    )
