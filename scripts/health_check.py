#!/usr/bin/env python3
"""Check the complete local Music Hub delivery path without changing state."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import urllib.error
import urllib.request


DEFAULT_HOST_HEADER = "81.68.72.245"
DEFAULT_BASE_URL = "http://127.0.0.1"
DEFAULT_SERVICES = ("musichub.service", "yorushika-radio.service", "nginx.service")


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


def run_checks(base_url: str, host_header: str, services: tuple[str, ...]) -> dict:
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
        if not playlist.startswith("#EXTM3U") or ".ts" not in playlist:
            raise RuntimeError("playlist has no active media segments")
        checks["http:/hls/yorushika.m3u8"] = "ok"
    except (OSError, UnicodeError, RuntimeError, urllib.error.URLError) as error:
        checks["http:/hls/yorushika.m3u8"] = "failed"
        failures.append(f"HLS playlist: {error}")

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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    services = tuple(args.services or DEFAULT_SERVICES)
    result = run_checks(args.base_url, args.host_header, services)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
