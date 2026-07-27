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
    "【4K 60FPS】【中日双字】《パレード（游行）》ヨルシカ （Yorushika）｜前奏超好听！｜ヨルシカ Yorushika LIVE 2024「前世」",
    "Dongmian",
    "Elma",
    "Forget_it",
    "Liar",
    "Matasaburo",
    "Spring_Thief",
    "Suoyiwofangqileyinyue",
    "Thoughtcrime",
    "yinci_bayue_mou",
    "Zuoyoumang",
    "ヨルシカ-ただ君に晴れ 现场版",
    "ヨルシカ -ノーチラス 现场版",
    "ヨルシカ-ヒッチコック 现场版 中日字幕",
    "ヨルシカ - ブレーメン 现场版",
    "ヨルシカ - 嘘月 现场版 双语字幕",
    "ヨルシカ - 春ひさぎ 现场版 双语字幕",
    "ヨルシカ - 神様のダンス 现场版",
    "ヨルシカ - 花に亡霊 现场版 官中字幕",
    "ヨルシカ-花人局 现场版",
    "ヨルシカ-蓝二乘 现场版 双语字幕",
    "ヨルシカ-言って。现场版",
    "ヨルシカ-雨とカプチーノ 现场版",
    "ヨルシカ-雨晴るる 现场版 中日字幕",
]

TITLE_OVERRIDES = {
    PLAYLIST_ORDER[0]: "パレード (Live)",
    "Dongmian": "冬眠",
    "Elma": "エルマ",
    "Forget_it": "忘れてください",
    "Liar": "嘘月",
    "Matasaburo": "又三郎",
    "Spring_Thief": "春泥棒",
    "Suoyiwofangqileyinyue": "だから僕は音楽を辞めた",
    "Thoughtcrime": "思想犯",
    "yinci_bayue_mou": "八月、某、月明かり",
    "Zuoyoumang": "左右盲",
    PLAYLIST_ORDER[11]: "ただ君に晴れ (Live)",
    PLAYLIST_ORDER[12]: "ノーチラス (Live)",
    PLAYLIST_ORDER[13]: "ヒッチコック (Live)",
    PLAYLIST_ORDER[14]: "ブレーメン (Live)",
    PLAYLIST_ORDER[15]: "嘘月 (Live)",
    PLAYLIST_ORDER[16]: "春ひさぎ (Live)",
    PLAYLIST_ORDER[17]: "神様のダンス (Live)",
    PLAYLIST_ORDER[18]: "花に亡霊 (Live)",
    PLAYLIST_ORDER[19]: "花人局 (Live)",
    PLAYLIST_ORDER[20]: "藍二乗 (Live)",
    PLAYLIST_ORDER[21]: "言って。 (Live)",
    PLAYLIST_ORDER[22]: "雨とカプチーノ (Live)",
    PLAYLIST_ORDER[23]: "雨晴るる (Live)",
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
