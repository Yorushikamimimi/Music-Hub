#!/usr/bin/env python3
"""Check the complete local Music Hub delivery path without changing state."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request


DEFAULT_HOST_HEADER = "81.68.72.245"
DEFAULT_BASE_URL = "http://127.0.0.1"
DEFAULT_SERVICES = ("musichub.service", "yorushika-radio.service", "nginx.service")
DEFAULT_ATTEMPTS = 4
DEFAULT_RETRY_DELAY_SECONDS = 2
DEFAULT_HLS_MAX_AGE_SECONDS = 30
HLS_SEGMENT_NAME_PATTERN = re.compile(r"yorushika-[0-9]{8}\.ts\Z")
COMPACT_UTC_OFFSET_PATTERN = re.compile(r"([+-])([0-9]{2})([0-9]{2})\Z")


def service_is_active(service: str) -> None:
    subprocess.run(
        ["systemctl", "is-active", "--quiet", service],
        check=True,
        timeout=10,
    )


def fetch(base_url: str, host_header: str, path: str) -> bytes:
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
        headers={
            "Host": host_header,
            "User-Agent": "music-hub-health/1.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"{path} returned HTTP {response.status}")
        return response.read(1024 * 1024)


def parse_program_datetime(value: str) -> dt.datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    else:
        match = COMPACT_UTC_OFFSET_PATTERN.search(value)
        if match:
            hours = int(match.group(2))
            minutes = int(match.group(3))
            if hours > 23 or minutes > 59:
                raise ValueError("invalid UTC offset")
            value = (
                value[: match.start()]
                + match.group(1)
                + match.group(2)
                + ":"
                + match.group(3)
            )
    return dt.datetime.fromisoformat(value)


def validate_live_playlist(playlist: str, max_age_seconds: int) -> str:
    lines = playlist.splitlines()
    segment_names = [line.strip() for line in lines if line and not line.startswith("#")]
    if not playlist.startswith("#EXTM3U") or not segment_names:
        raise RuntimeError("playlist has no active media segments")
    if any(not HLS_SEGMENT_NAME_PATTERN.fullmatch(name) for name in segment_names):
        raise RuntimeError("playlist contains an unsafe HLS segment path")

    program_dates = [
        line.partition(":")[2]
        for line in lines
        if line.startswith("#EXT-X-PROGRAM-DATE-TIME:")
    ]
    if not program_dates:
        raise RuntimeError("playlist has no program date-time for freshness check")
    try:
        latest_segment = parse_program_datetime(program_dates[-1])
    except ValueError as error:
        raise RuntimeError("playlist has an invalid program date-time") from error
    if latest_segment.tzinfo is None:
        raise RuntimeError("playlist program date-time has no timezone")

    age_seconds = (dt.datetime.now(dt.timezone.utc) - latest_segment).total_seconds()
    if age_seconds > max_age_seconds:
        raise RuntimeError(
            f"latest HLS segment is stale ({age_seconds:.1f}s old; "
            f"limit {max_age_seconds}s)"
        )
    if age_seconds < -max_age_seconds:
        raise RuntimeError(
            f"latest HLS segment date-time is too far in the future "
            f"({-age_seconds:.1f}s)"
        )
    return f"/hls/{segment_names[-1]}"


def validate_ts_segment(segment: bytes) -> None:
    packet_size = 188
    if len(segment) < packet_size or len(segment) % packet_size:
        raise RuntimeError("latest HLS segment is empty or truncated")
    if any(segment[offset] != 0x47 for offset in range(0, len(segment), packet_size)):
        raise RuntimeError("latest HLS segment has invalid MPEG-TS sync bytes")


def _run_checks_once(
    base_url: str,
    host_header: str,
    services: tuple[str, ...],
    hls_max_age_seconds: int,
) -> dict:
    checks: dict[str, str] = {}
    failures: list[str] = []

    for service in services:
        try:
            service_is_active(service)
            checks[f"service:{service}"] = "ok"
        except (OSError, subprocess.SubprocessError) as error:
            checks[f"service:{service}"] = "failed"
            failures.append(f"{service}: {error}")

    try:
        health = json.loads(fetch(base_url, host_header, "/healthz"))
        if health != {"status": "ok"}:
            raise RuntimeError("unexpected health payload")
        checks["http:/healthz"] = "ok"
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as error:
        checks["http:/healthz"] = "failed"
        failures.append(f"/healthz: {error}")

    try:
        playlist = fetch(base_url, host_header, "/hls/yorushika.m3u8").decode(
            "utf-8",
            errors="strict",
        )
        segment_path = validate_live_playlist(playlist, hls_max_age_seconds)
        checks["http:/hls/yorushika.m3u8"] = "ok"
    except (OSError, UnicodeError, RuntimeError, urllib.error.URLError) as error:
        checks["http:/hls/yorushika.m3u8"] = "failed"
        failures.append(f"HLS playlist: {error}")
    else:
        try:
            validate_ts_segment(fetch(base_url, host_header, segment_path))
            checks["http:/hls/latest-segment"] = "ok"
        except (OSError, RuntimeError, urllib.error.URLError) as error:
            checks["http:/hls/latest-segment"] = "failed"
            failures.append(f"HLS segment: {error}")

    try:
        schedule = json.loads(
            fetch(base_url, host_header, "/hls/radio-schedule.json")
        )
        if schedule.get("private") is not True or not schedule.get("tracks"):
            raise RuntimeError("schedule is missing its private track list")
        checks["http:/hls/radio-schedule.json"] = "ok"
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as error:
        checks["http:/hls/radio-schedule.json"] = "failed"
        failures.append(f"radio schedule: {error}")

    return {
        "checkedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "ok" if not failures else "failed",
        "checks": checks,
        "failures": failures,
    }


def run_checks(
    base_url: str,
    host_header: str,
    services: tuple[str, ...],
    attempts: int = DEFAULT_ATTEMPTS,
    retry_delay_seconds: int = DEFAULT_RETRY_DELAY_SECONDS,
    hls_max_age_seconds: int = DEFAULT_HLS_MAX_AGE_SECONDS,
) -> dict:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    if retry_delay_seconds < 0:
        raise ValueError("retry delay must not be negative")
    if hls_max_age_seconds < 1:
        raise ValueError("HLS max age must be at least 1 second")

    for attempt in range(1, attempts + 1):
        result = _run_checks_once(
            base_url,
            host_header,
            services,
            hls_max_age_seconds,
        )
        result["attempts"] = attempt
        if result["status"] == "ok" or attempt == attempts:
            return result
        time.sleep(retry_delay_seconds)

    raise AssertionError("unreachable")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--host-header", default=DEFAULT_HOST_HEADER)
    parser.add_argument(
        "--service",
        action="append",
        dest="services",
        help="systemd service to check; may be supplied more than once",
    )
    parser.add_argument("--attempts", type=int, default=DEFAULT_ATTEMPTS)
    parser.add_argument(
        "--retry-delay-seconds",
        type=int,
        default=DEFAULT_RETRY_DELAY_SECONDS,
    )
    parser.add_argument(
        "--hls-max-age-seconds",
        type=int,
        default=DEFAULT_HLS_MAX_AGE_SECONDS,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    services = tuple(args.services or DEFAULT_SERVICES)
    result = run_checks(
        args.base_url,
        args.host_header,
        services,
        attempts=args.attempts,
        retry_delay_seconds=args.retry_delay_seconds,
        hls_max_age_seconds=args.hls_max_age_seconds,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
