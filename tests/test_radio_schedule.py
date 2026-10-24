import json
import os
import pathlib

import pytest

from catalog_data import CATALOG_TRACKS
from scripts import generate_radio_schedule


def test_playlist_only_includes_curated_yorushika_files(tmp_path):
    first = tmp_path / f"{generate_radio_schedule.PLAYLIST_ORDER[0]}.mp3"
    second = tmp_path / f"{generate_radio_schedule.PLAYLIST_ORDER[1]}.mp3"
    unknown = tmp_path / "unreviewed-track.mp3"
    for path in (first, second, unknown):
        path.touch()

    assert generate_radio_schedule.ordered_music_files(tmp_path) == [first, second]
    assert len(generate_radio_schedule.PLAYLIST_ORDER) == 57
    assert len(set(generate_radio_schedule.PLAYLIST_ORDER)) == 57
    assert {
        concert: len(titles)
        for concert, titles in generate_radio_schedule.CONCERT_PLAYLISTS.items()
    } == {
        "2021前世": 13,
        "2022月光": 15,
        "2024前世": 15,
        "2024月猫": 14,
    }
    assert set(generate_radio_schedule.PLAYLIST_ORDER) == set(
        generate_radio_schedule.TITLE_OVERRIDES
    )
    assert set(generate_radio_schedule.PLAYLIST_ORDER) == set(
        generate_radio_schedule.ARTWORK_TITLES
    )
    catalog_titles = {track["title_ja"] for track in CATALOG_TRACKS}
    assert set(generate_radio_schedule.ARTWORK_TITLES.values()) <= catalog_titles


def test_generated_schedule_is_private(tmp_path, monkeypatch):
    music_dir = tmp_path / "music"
    runtime_dir = tmp_path / "runtime"
    cache_dir = tmp_path / "cache"
    music_dir.mkdir()
    track_stem = generate_radio_schedule.PLAYLIST_ORDER[0]
    (music_dir / f"{track_stem}.mp3").touch()

    monkeypatch.setenv("RADIO_MUSIC_DIR", str(music_dir))
    monkeypatch.setenv("RADIO_RUNTIME_DIR", str(runtime_dir))
    monkeypatch.setenv("RADIO_CACHE_DIR", str(cache_dir))
    monkeypatch.setattr(generate_radio_schedule, "duration_for", lambda _path: 180.0)
    monkeypatch.setattr(generate_radio_schedule.time, "time", lambda: 1000.0)
    loop_cache_path = cache_dir / "loop.mka"
    monkeypatch.setattr(
        generate_radio_schedule,
        "ensure_loop_cache",
        lambda _files, _durations, _cache_dir: (loop_cache_path, 180.0),
    )

    generate_radio_schedule.main([])

    schedule = json.loads(
        (runtime_dir / "hls" / "radio-schedule.json").read_text(encoding="utf-8")
    )
    assert schedule["private"] is True
    assert schedule["tracks"] == [
        {
            "title": generate_radio_schedule.TITLE_OVERRIDES[track_stem],
            "artworkTitle": generate_radio_schedule.ARTWORK_TITLES[track_stem],
            "artist": "Yorushika",
            "duration": 180.0,
        }
    ]
    assert (runtime_dir / "playlist.txt").read_text(encoding="utf-8") == (
        f"file '{loop_cache_path}'\n"
    )


def test_loop_cache_copies_curated_mp3s_and_rebuilds_when_source_changes(
    tmp_path,
    monkeypatch,
):
    first = tmp_path / "first.mp3"
    second = tmp_path / "second.mp3"
    first.write_bytes(b"first-original")
    second.write_bytes(b"second-original")
    cache_dir = tmp_path / "cache"
    ffmpeg_calls = []

    def fake_run(command, **_kwargs):
        ffmpeg_calls.append(command)
        assert "-c:a" in command
        assert command[command.index("-c:a") + 1] == "copy"
        assert command[-3:-1] == ["-f", "matroska"]
        pathlib.Path(command[-1]).write_bytes(b"uncompressed-matroska-cache")

    monkeypatch.setattr(generate_radio_schedule.subprocess, "run", fake_run)
    monkeypatch.setattr(
        generate_radio_schedule,
        "precise_duration_for",
        lambda path: (
            3.01
            if pathlib.Path(path).suffix in {".tmp", ".mka"}
            else 3.0
        ),
    )

    cache_path, cache_duration = generate_radio_schedule.ensure_loop_cache(
        [first, second], [1.5, 1.5], cache_dir
    )
    assert cache_path == cache_dir / "loop.mka"
    assert cache_duration == 3.01
    assert len(ffmpeg_calls) == 1
    assert first.read_bytes() == b"first-original"
    assert second.read_bytes() == b"second-original"

    generate_radio_schedule.ensure_loop_cache([first, second], [1.5, 1.5], cache_dir)
    assert len(ffmpeg_calls) == 1

    stat = first.stat()
    os.utime(first, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    generate_radio_schedule.ensure_loop_cache([first, second], [1.5, 1.5], cache_dir)
    assert len(ffmpeg_calls) == 2

    generate_radio_schedule.ensure_loop_cache(
        [first, second], [1.501, 1.499], cache_dir
    )
    assert len(ffmpeg_calls) == 3

    first.write_bytes(b"first-source-changed-size")
    generate_radio_schedule.ensure_loop_cache([first, second], [1.5, 1.5], cache_dir)
    assert len(ffmpeg_calls) == 4


def test_loop_cache_rejects_a_duration_mismatch_of_one_second_or_more(
    tmp_path,
    monkeypatch,
):
    source = tmp_path / "source.mp3"
    source.write_bytes(b"source")

    def fake_run(command, **_kwargs):
        pathlib.Path(command[-1]).write_bytes(b"bad duration cache")

    monkeypatch.setattr(generate_radio_schedule.subprocess, "run", fake_run)
    monkeypatch.setattr(
        generate_radio_schedule,
        "precise_duration_for",
        lambda path: 4.0 if pathlib.Path(path).suffix == ".tmp" else 3.0,
    )

    with pytest.raises(RuntimeError, match="limit < 1s"):
        generate_radio_schedule.ensure_loop_cache([source], [3.0], tmp_path / "cache")

    assert not (tmp_path / "cache" / "loop.mka").exists()
    assert not (tmp_path / "cache" / "loop.tmp").exists()


def test_schedule_last_track_absorbs_loop_cache_duration_difference():
    durations = generate_radio_schedule.schedule_track_durations(
        [1.5, 1.5], 3.041
    )

    assert durations == [1.5, 1.541]
    assert abs(sum(durations) - 3.041) <= 0.003


def test_schedule_rejects_a_non_positive_adjusted_last_track():
    with pytest.raises(RuntimeError, match="final track non-positive"):
        generate_radio_schedule.schedule_track_durations([1.5, 1.5], 1.499)


def test_prepare_cache_only_leaves_live_runtime_files_untouched(tmp_path, monkeypatch):
    music_dir = tmp_path / "music"
    runtime_dir = tmp_path / "runtime"
    cache_dir = tmp_path / "cache"
    music_dir.mkdir()
    track = music_dir / f"{generate_radio_schedule.PLAYLIST_ORDER[0]}.mp3"
    track.touch()
    hls_dir = runtime_dir / "hls"
    hls_dir.mkdir(parents=True)
    live_playlist = hls_dir / "yorushika.m3u8"
    live_playlist.write_text("leave live HLS alone\n", encoding="utf-8")

    monkeypatch.setenv("RADIO_MUSIC_DIR", str(music_dir))
    monkeypatch.setenv("RADIO_RUNTIME_DIR", str(runtime_dir))
    monkeypatch.setenv("RADIO_CACHE_DIR", str(cache_dir))
    monkeypatch.setattr(generate_radio_schedule, "duration_for", lambda _path: 180.0)
    monkeypatch.setattr(
        generate_radio_schedule,
        "ensure_loop_cache",
        lambda _files, _durations, _cache_dir: (cache_dir / "loop.mka", 180.0),
    )

    generate_radio_schedule.main(["--prepare-cache-only"])

    assert live_playlist.read_text(encoding="utf-8") == "leave live HLS alone\n"
    assert not (hls_dir / "radio-schedule.json").exists()
