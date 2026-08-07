#!/usr/bin/env python3
"""Build the deterministic FFmpeg playlist and browser-facing radio schedule."""

import json
import os
import pathlib
import subprocess
import time


DEFAULT_MUSIC_DIR = "/srv/media/yorushika-radio/music"
DEFAULT_RUNTIME_DIR = "/run/yorushika-radio"

PLAYLIST_ORDER = [
    "2021前世 蓝二乘",
    "2021前世 所以我放弃了音乐",
    "2021前世 雨和卡布奇诺",
    "2021前世 游行",
    "2021前世 言って",
    "2021前世 只为你拨云放晴",
    "2021前世 希区柯克",
    "2021前世 卖春",
    "2021前世 思想犯+花人局",
    "2021前世 春泥棒",
    "2021前世 鹦鹉螺",
    "2021前世 Elma",
    "2021前世 冬眠",
]

TITLE_OVERRIDES = {stem: stem for stem in PLAYLIST_ORDER}

ARTWORK_TITLES = {
    "2021前世 蓝二乘": "藍二乗",
    "2021前世 所以我放弃了音乐": "だから僕は音楽を辞めた",
    "2021前世 雨和卡布奇诺": "雨とカプチーノ",
    "2021前世 游行": "パレード",
    "2021前世 言って": "言って。",
    "2021前世 只为你拨云放晴": "ただ君に晴れ",
    "2021前世 希区柯克": "ヒッチコック",
    "2021前世 卖春": "春ひさぎ",
    "2021前世 思想犯+花人局": "思想犯",
    "2021前世 春泥棒": "春泥棒",
    "2021前世 鹦鹉螺": "ノーチラス",
    "2021前世 Elma": "エルマ",
    "2021前世 冬眠": "冬眠",
}


def ordered_music_files(music_dir):
    discovered = {path.stem: path for path in music_dir.glob("*.mp3") if path.is_file()}
    ordered = [discovered[stem] for stem in PLAYLIST_ORDER if stem in discovered]
    if not ordered:
        raise RuntimeError(f"No curated Yorushika MP3 files found in {music_dir}")
    return ordered


def duration_for(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return max(1, round(float(result.stdout.strip()), 3))


def concat_line(path):
    escaped_path = str(path).replace("'", "'\\''")
    return f"file '{escaped_path}'"


def clear_generated_hls(hls_dir):
    for pattern in ("yorushika-*.ts", "yorushika.m3u8", "radio-schedule.json*"):
        for path in hls_dir.glob(pattern):
            if path.is_file():
                path.unlink()


def write_atomic(path, content):
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(content, encoding="utf-8")
    os.replace(temporary_path, path)
    path.chmod(0o644)


def main():
    music_dir = pathlib.Path(os.environ.get("RADIO_MUSIC_DIR", DEFAULT_MUSIC_DIR))
    runtime_dir = pathlib.Path(os.environ.get("RADIO_RUNTIME_DIR", DEFAULT_RUNTIME_DIR))
    hls_dir = runtime_dir / "hls"
    playlist_path = runtime_dir / "playlist.txt"
    schedule_path = hls_dir / "radio-schedule.json"

    runtime_dir.mkdir(parents=True, exist_ok=True)
    hls_dir.mkdir(parents=True, exist_ok=True)
    clear_generated_hls(hls_dir)

    files = ordered_music_files(music_dir)
    playlist_content = "\n".join(concat_line(path) for path in files) + "\n"
    write_atomic(playlist_path, playlist_content)

    tracks = [
        {
            "title": TITLE_OVERRIDES.get(path.stem, path.stem.replace("_", " ")),
            "artworkTitle": ARTWORK_TITLES.get(path.stem, path.stem),
            "artist": "Yorushika",
            "duration": duration_for(path),
        }
        for path in files
    ]

    now = time.time()
    payload = {
        "station": os.environ.get("RADIO_STATION_NAME", "Yorushika Radio"),
        "startedAt": round(now, 3),
        "generatedAt": round(now, 3),
        "bufferDelaySeconds": int(os.environ.get("RADIO_BUFFER_DELAY_SECONDS", "16")),
        "private": True,
        "tracks": tracks,
    }
    write_atomic(
        schedule_path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )
    print(f"Prepared {len(tracks)} tracks in {runtime_dir}")


if __name__ == "__main__":
    main()
