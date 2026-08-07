#!/usr/bin/env python3
"""Build the deterministic FFmpeg playlist and browser-facing radio schedule."""

import json
import os
import pathlib
import subprocess
import time


DEFAULT_MUSIC_DIR = "/srv/media/yorushika-radio/music"
DEFAULT_RUNTIME_DIR = "/run/yorushika-radio"

CONCERT_PLAYLISTS = {
    "2021前世": [
        "蓝二乘",
        "所以我放弃了音乐",
        "雨和卡布奇诺",
        "游行",
        "言って",
        "只为你拨云放晴",
        "希区柯克",
        "卖春",
        "思想犯+花人局",
        "春泥棒",
        "鹦鹉螺",
        "Elma",
        "冬眠",
    ],
    "2022月光": [
        "傍晚风平浪静、某处、烟火",
        "八月某日、明月",
        "蓝二乘",
        "神之舞",
        "难辨夜色",
        "雨和卡布奇诺",
        "六月は雨上がりの街を書く",
        "雨过天晴",
        "起舞吧",
        "漫步",
        "心中空洞",
        "游行",
        "憂一乗",
        "鹦鹉螺",
        "所以我放弃了音乐",
    ],
    "2024前世": [
        "負け犬にアンコールはいらない",
        "言って",
        "靴の花火",
        "希区柯克",
        "只为你拨云放晴",
        "Rubato+雨和卡布奇诺",
        "嘘月",
        "忘れてください",
        "花に亡霊",
        "晴る",
        "冬眠",
        "詩書きとコーヒー+游行",
        "所以我放弃了音乐",
        "左右盲",
        "春泥棒",
    ],
    "2024月猫": [
        "不莱梅+雨和卡布奇诺",
        "再见莫顿",
        "又三郎",
        "嘘月",
        "都落",
        "只为你拨云放晴",
        "地粮",
        "雪国",
        "勇鱼",
        "斜阳",
        "靴之花火",
        "左右盲",
        "春泥棒",
        "阿尔吉侬",
    ],
}

PLAYLIST_ORDER = [
    f"{concert} {title}"
    for concert, titles in CONCERT_PLAYLISTS.items()
    for title in titles
]

TITLE_OVERRIDES = {stem: stem for stem in PLAYLIST_ORDER}

ARTWORK_BY_TITLE = {
    "蓝二乘": "藍二乗",
    "所以我放弃了音乐": "だから僕は音楽を辞めた",
    "雨和卡布奇诺": "雨とカプチーノ",
    "游行": "パレード",
    "言って": "言って。",
    "只为你拨云放晴": "ただ君に晴れ",
    "希区柯克": "ヒッチコック",
    "卖春": "春ひさぎ",
    "思想犯+花人局": "思想犯",
    "春泥棒": "春泥棒",
    "鹦鹉螺": "ノーチラス",
    "Elma": "エルマ",
    "冬眠": "冬眠",
    "傍晚风平浪静、某处、烟火": "夕凪、某、花惑い",
    "八月某日、明月": "八月、某、月明かり",
    "神之舞": "神様のダンス",
    "难辨夜色": "夜紛い",
    "六月は雨上がりの街を書く": "六月は雨上がりの街を書く",
    "雨过天晴": "雨晴るる",
    "起舞吧": "踊ろうぜ",
    "漫步": "歩く",
    "心中空洞": "心に穴が空いた",
    "憂一乗": "憂一乗",
    "負け犬にアンコールはいらない": "負け犬にアンコールはいらない",
    "靴の花火": "靴の花火",
    "Rubato+雨和卡布奇诺": "ルバート",
    "嘘月": "嘘月",
    "忘れてください": "忘れてください",
    "花に亡霊": "花に亡霊",
    "晴る": "晴る",
    "詩書きとコーヒー+游行": "詩書きとコーヒー",
    "左右盲": "左右盲",
    "不莱梅+雨和卡布奇诺": "ブレーメン",
    "再见莫顿": "さよならモルテン",
    "又三郎": "又三郎",
    "都落": "都落ち",
    "地粮": "チノカテ",
    "雪国": "雪国",
    "勇鱼": "いさな",
    "斜阳": "斜陽",
    "靴之花火": "靴の花火",
    "阿尔吉侬": "アルジャーノン",
}

ARTWORK_TITLES = {
    stem: ARTWORK_BY_TITLE[stem.split(" ", 1)[1]] for stem in PLAYLIST_ORDER
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
