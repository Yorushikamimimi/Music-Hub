#!/usr/bin/env python3
"""Persist the latest Music Hub unit failure without exposing configuration."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys


SAFE_UNIT = re.compile(r"^[A-Za-z0-9@_.:-]+$")
DEFAULT_STATE_DIR = pathlib.Path("/var/lib/music-hub-monitor")


def unit_status(unit: str) -> dict[str, str]:
    result = subprocess.run(
        [
            "systemctl",
            "show",
            unit,
            "--property=ActiveState",
            "--property=SubState",
            "--property=Result",
            "--property=ExecMainStatus",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    status = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition("=")
        if separator:
            status[key] = value
    return status


def record_failure(unit: str, state_dir: pathlib.Path) -> pathlib.Path:
    if not SAFE_UNIT.fullmatch(unit):
        raise ValueError("invalid systemd unit name")

    state_dir.mkdir(parents=True, exist_ok=True, mode=0o750)
    os.chmod(state_dir, 0o750)
    payload = {
        "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "unit": unit,
        "status": unit_status(unit),
    }

    target = state_dir / "last-failure.json"
    temporary = state_dir / ".last-failure.json.tmp"
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary, 0o640)
    os.replace(temporary, target)
    subprocess.run(
        [
            "logger",
            "--priority",
            "daemon.err",
            "--tag",
            "music-hub-monitor",
            f"Recorded failure for {unit}",
        ],
        check=False,
        timeout=10,
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("unit")
    parser.add_argument("--state-dir", type=pathlib.Path, default=DEFAULT_STATE_DIR)
    args = parser.parse_args()
    target = record_failure(args.unit, args.state_dir)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
