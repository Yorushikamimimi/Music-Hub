#!/usr/bin/env python3
"""Build the deterministic FFmpeg playlist and browser-facing radio schedule."""

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import time


DEFAULT_MUSIC_DIR = "/srv/media/yorushika-radio/music"
DEFAULT_RUNTIME_DIR = "/run/yorushika-radio"
DEFAULT_CACHE_DIR = "/var/cache/yorushika-radio"

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
    return max(1, round(precise_duration_for(path), 3))


def precise_duration_for(path):
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
    return float(result.stdout.strip())


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


def source_fingerprint(files, durations):
    if len(files) != len(durations):
        raise ValueError("each Radio MP3 file must have one duration")
    manifest = []
    for path, duration in zip(files, durations):
        stat = path.stat()
        manifest.append(
            {
                "path": str(path.resolve()),
                "size": stat.st_size,
                "mtimeNs": stat.st_mtime_ns,
                "duration": round(float(duration), 6),
            }
        )
    encoded = json.dumps(manifest, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def ensure_loop_cache(files, durations, cache_dir):
    cache_dir = pathlib.Path(cache_dir).resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "loop.mka"
    temporary_cache_path = cache_dir / "loop.tmp"
    metadata_path = cache_dir / "loop.json"
    fingerprint = source_fingerprint(files, durations)
    source_duration = sum(float(duration) for duration in durations)

    if cache_path.is_file() and not cache_path.is_symlink() and metadata_path.is_file():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            cache_stat = cache_path.stat()
            cached_duration = precise_duration_for(cache_path)
            if (
                metadata.get("sourceFingerprint") == fingerprint
                and metadata.get("cacheSize") == cache_stat.st_size
                and abs(cached_duration - source_duration) < 1
                and abs(cached_duration - metadata.get("cacheDuration", -2)) < 0.01
            ):
                return cache_path, cached_duration
        except (OSError, ValueError, TypeError, subprocess.SubprocessError):
            pass

    before_fingerprint = fingerprint
    temporary_playlist_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".source-playlist-",
            suffix=".txt",
            dir=cache_dir,
            delete=False,
        ) as playlist_file:
            temporary_playlist_path = pathlib.Path(playlist_file.name)
            playlist_file.write("\n".join(concat_line(path) for path in files) + "\n")

        temporary_cache_path.unlink(missing_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "warning",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(temporary_playlist_path),
                "-map",
                "0:a:0",
                "-c:a",
                "copy",
                "-f",
                "matroska",
                str(temporary_cache_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if source_fingerprint(files, durations) != before_fingerprint:
            raise RuntimeError("Radio MP3 sources changed while building loop cache")

        cache_duration = precise_duration_for(temporary_cache_path)
        duration_error = abs(cache_duration - source_duration)
        if duration_error >= 1:
            raise RuntimeError(
                "Radio loop cache duration differs from the source playlist by "
                f"{duration_error:.3f}s (limit < 1s)"
            )

        os.replace(temporary_cache_path, cache_path)
        cache_stat = cache_path.stat()
        metadata = {
            "sourceFingerprint": fingerprint,
            "sourceDuration": source_duration,
            "cacheDuration": cache_duration,
            "cacheSize": cache_stat.st_size,
        }
        write_atomic(
            metadata_path,
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        )
        return cache_path, cache_duration
    finally:
        if temporary_playlist_path is not None:
            temporary_playlist_path.unlink(missing_ok=True)
        temporary_cache_path.unlink(missing_ok=True)


def schedule_track_durations(durations, loop_duration):
    scheduled = [max(1, round(float(duration), 3)) for duration in durations]
    if not scheduled:
        raise RuntimeError("Radio schedule has no tracks")

    adjusted_last_duration = round(float(loop_duration) - sum(scheduled[:-1]), 3)
    if adjusted_last_duration <= 0:
        raise RuntimeError("Radio loop duration makes the final track non-positive")
    scheduled[-1] = adjusted_last_duration
    if abs(sum(scheduled) - float(loop_duration)) > 0.003:
        raise RuntimeError("Radio schedule duration does not match loop cache duration")
    return scheduled


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prepare-cache-only",
        action="store_true",
        help="build or validate the persistent loop cache without touching live HLS files",
    )
    args = parser.parse_args(argv)

    music_dir = pathlib.Path(os.environ.get("RADIO_MUSIC_DIR", DEFAULT_MUSIC_DIR))
    runtime_dir = pathlib.Path(os.environ.get("RADIO_RUNTIME_DIR", DEFAULT_RUNTIME_DIR))
    cache_dir = pathlib.Path(os.environ.get("RADIO_CACHE_DIR", DEFAULT_CACHE_DIR))
    hls_dir = runtime_dir / "hls"
    playlist_path = runtime_dir / "playlist.txt"
    schedule_path = hls_dir / "radio-schedule.json"

    files = ordered_music_files(music_dir)
    durations = [duration_for(path) for path in files]
    loop_cache_path, loop_duration = ensure_loop_cache(files, durations, cache_dir)
    if args.prepare_cache_only:
        print(
            f"Prepared loop cache {loop_cache_path} "
            f"({loop_duration:.3f}s for {len(files)} tracks)"
        )
        return

    runtime_dir.mkdir(parents=True, exist_ok=True)
    hls_dir.mkdir(parents=True, exist_ok=True)
    clear_generated_hls(hls_dir)

    playlist_content = f"file '{loop_cache_path}'\n"
    write_atomic(playlist_path, playlist_content)
    scheduled_durations = schedule_track_durations(durations, loop_duration)
    tracks = [
        {
            "title": TITLE_OVERRIDES.get(path.stem, path.stem.replace("_", " ")),
            "artworkTitle": ARTWORK_TITLES.get(path.stem, path.stem),
            "artist": "Yorushika",
            "duration": scheduled_duration,
        }
        for path, scheduled_duration in zip(files, scheduled_durations)
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
