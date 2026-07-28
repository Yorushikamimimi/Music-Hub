#!/usr/bin/env python3
"""Create complete code snapshots and perform explicit Music Hub rollbacks."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile


DEFAULT_APP_DIR = pathlib.Path("/var/www/My_Homepage")
DEFAULT_BACKUP_DIR = pathlib.Path("/var/backups/music-hub/releases")
DEFAULT_STATE_FILE = pathlib.Path("/var/lib/music-hub-monitor/deployed-version.json")
SNAPSHOT_NAME = re.compile(
    r"^predeploy-\d{8}T\d{6}(?:\d{6})?Z-[0-9a-f]{7,40}\.tar\.gz$"
)
EXCLUDED_PARTS = {
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".playwright-cli",
    "playwright-report",
    "test-results",
    "instance",
}
EXCLUDED_FILES = {".env", "current_avatar.txt"}


def run_text(command: list[str], default: str = "unknown") -> str:
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else default


def load_deployed_version(state_file: pathlib.Path) -> tuple[str, str] | None:
    if not state_file.is_file():
        return None
    try:
        payload = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    commit = str(payload.get("commit", ""))
    branch = str(payload.get("branch", ""))
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit) or not branch:
        return None
    return commit, branch


def record_deployed_version(
    state_file: pathlib.Path,
    commit: str,
    branch: str,
    source: str,
) -> pathlib.Path:
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        raise ValueError("commit must be a hexadecimal Git object id")
    if not branch or any(character in branch for character in "\x00\r\n"):
        raise ValueError("branch is invalid")
    state_file.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
    os.chmod(state_file.parent, 0o750)
    payload = {
        "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "commit": commit,
        "branch": branch,
        "source": source,
    }
    temporary = state_file.with_name(f".{state_file.name}.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary, 0o640)
    os.replace(temporary, state_file)
    return state_file


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def should_exclude(relative: pathlib.Path) -> bool:
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return True
    if relative.name in EXCLUDED_FILES or relative.suffix == ".pyc":
        return True
    return len(relative.parts) >= 2 and relative.parts[:2] == ("static", "uploads")


def add_application_tree(
    archive: tarfile.TarFile,
    app_dir: pathlib.Path,
) -> None:
    archive.add(app_dir, arcname="app", recursive=False)
    for root, directories, files in os.walk(app_dir, topdown=True, followlinks=False):
        root_path = pathlib.Path(root)
        relative_root = root_path.relative_to(app_dir)
        directories[:] = [
            name
            for name in directories
            if not should_exclude(relative_root / name)
            and not (root_path / name).is_symlink()
        ]
        for directory in directories:
            path = root_path / directory
            relative = path.relative_to(app_dir)
            archive.add(path, arcname=str(pathlib.Path("app") / relative), recursive=False)
        for filename in files:
            path = root_path / filename
            relative = path.relative_to(app_dir)
            if should_exclude(relative) or path.is_symlink() or not path.is_file():
                continue
            archive.add(path, arcname=str(pathlib.Path("app") / relative), recursive=False)


def snapshots(backup_dir: pathlib.Path) -> list[pathlib.Path]:
    if not backup_dir.exists():
        return []
    return sorted(
        (
            path
            for path in backup_dir.iterdir()
            if path.is_file() and SNAPSHOT_NAME.fullmatch(path.name)
        ),
        key=lambda path: (path.stat().st_mtime, path.name),
        reverse=True,
    )


def prune_snapshots(
    backup_dir: pathlib.Path,
    keep: int,
    apply: bool,
) -> list[pathlib.Path]:
    if keep < 1:
        raise ValueError("keep must be at least 1")
    candidates = snapshots(backup_dir)[keep:]
    if apply:
        for snapshot in candidates:
            snapshot.unlink()
            snapshot.with_name(f"{snapshot.name}.json").unlink(missing_ok=True)
    return candidates


def create_snapshot(
    app_dir: pathlib.Path,
    backup_dir: pathlib.Path,
    keep: int,
    prune_mode: str,
    state_file: pathlib.Path = DEFAULT_STATE_FILE,
) -> dict:
    app_dir = app_dir.resolve(strict=True)
    backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(backup_dir, 0o700)

    deployed_version = load_deployed_version(state_file)
    commit = (
        deployed_version[0]
        if deployed_version
        else run_text(
            ["git", "-C", str(app_dir), "rev-parse", "--verify", "HEAD"],
            default="unknown",
        )
    )
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        commit = "0000000"
    branch = (
        deployed_version[1]
        if deployed_version
        else run_text(
            ["git", "-C", str(app_dir), "branch", "--show-current"],
            default="detached-or-untracked",
        )
    )
    dirty = bool(
        run_text(
            ["git", "-C", str(app_dir), "status", "--short"],
            default="",
        )
    )
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = backup_dir / f"predeploy-{timestamp}-{commit}.tar.gz"
    temporary = target.with_name(f".{target.name}.partial")
    temporary.unlink(missing_ok=True)

    old_umask = os.umask(0o077)
    try:
        with tarfile.open(temporary, mode="w:gz", compresslevel=9) as archive:
            add_application_tree(archive, app_dir)
        os.replace(temporary, target)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    finally:
        os.umask(old_umask)

    os.chmod(target, 0o600)
    checksum = sha256_file(target)
    manifest = {
        "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "appDir": str(app_dir),
        "branch": branch,
        "commit": commit,
        "gitDirty": dirty,
        "sha256": checksum,
        "snapshot": target.name,
    }
    manifest_path = target.with_name(f"{target.name}.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(manifest_path, 0o600)

    candidates = prune_snapshots(
        backup_dir,
        keep=keep,
        apply=prune_mode == "apply",
    )
    return {
        "status": "ok",
        "snapshot": str(target),
        "sha256": checksum,
        "retention": {
            "keep": keep,
            "mode": prune_mode,
            "candidates": [path.name for path in candidates],
        },
    }


def validate_snapshot(
    snapshot: pathlib.Path,
    backup_dir: pathlib.Path,
) -> tuple[pathlib.Path, list[tarfile.TarInfo]]:
    snapshot = snapshot.resolve(strict=True)
    if snapshot.parent != backup_dir.resolve(strict=True):
        raise RuntimeError("snapshot must be inside the dedicated release backup directory")
    if not SNAPSHOT_NAME.fullmatch(snapshot.name):
        raise RuntimeError("snapshot name does not match the managed prefix")

    manifest_path = snapshot.with_name(f"{snapshot.name}.json")
    if not manifest_path.is_file():
        raise RuntimeError("snapshot manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("sha256") != sha256_file(snapshot):
        raise RuntimeError("snapshot checksum does not match its manifest")

    with tarfile.open(snapshot, mode="r:gz") as archive:
        members = archive.getmembers()
    if not members:
        raise RuntimeError("snapshot archive is empty")
    for member in members:
        path = pathlib.PurePosixPath(member.name)
        if (
            path.is_absolute()
            or ".." in path.parts
            or not path.parts
            or path.parts[0] != "app"
            or not (member.isdir() or member.isfile())
        ):
            raise RuntimeError(f"unsafe snapshot member: {member.name}")
    return snapshot, members


def rollback_snapshot(
    snapshot: pathlib.Path,
    app_dir: pathlib.Path,
    backup_dir: pathlib.Path,
    apply: bool,
    state_file: pathlib.Path = DEFAULT_STATE_FILE,
    host_header: str = "81.68.72.245",
) -> dict:
    snapshot, members = validate_snapshot(snapshot, backup_dir)
    plan = {
        "status": "planned" if not apply else "running",
        "snapshot": str(snapshot),
        "appDir": str(app_dir),
        "members": len(members),
        "databaseRollback": False,
        "services": ["musichub.service", "yorushika-radio.service"],
    }
    if not apply:
        return plan

    require_commands = ("curl", "rsync", "systemctl")
    missing = [command for command in require_commands if shutil.which(command) is None]
    if missing:
        raise RuntimeError(f"required commands are missing: {', '.join(missing)}")

    safety_snapshot = create_snapshot(
        app_dir=app_dir,
        backup_dir=backup_dir,
        keep=5,
        prune_mode="report",
        state_file=state_file,
    )
    with tempfile.TemporaryDirectory(prefix="music-hub-rollback-") as temporary:
        temporary_dir = pathlib.Path(temporary)
        with tarfile.open(snapshot, mode="r:gz") as archive:
            archive.extractall(temporary_dir)

        source = temporary_dir / "app"
        subprocess.run(
            [
                "rsync",
                "-a",
                "--delete",
                "--exclude=.git/",
                "--exclude=.env",
                "--exclude=venv/",
                "--exclude=static/uploads/",
                "--exclude=current_avatar.txt",
                "--exclude=scripts/health_check.py",
                "--exclude=scripts/mysql_backup.py",
                "--exclude=scripts/record_unit_failure.py",
                "--exclude=scripts/release_snapshot.py",
                f"{source}/",
                f"{app_dir}/",
            ],
            check=True,
            timeout=120,
        )

    pip = app_dir / "venv/bin/pip"
    python = app_dir / "venv/bin/python"
    if not pip.is_file() or not python.is_file():
        raise RuntimeError("existing virtual environment is unavailable")
    subprocess.run(
        [str(pip), "install", "--require-hashes", "-r", str(app_dir / "requirements.txt")],
        check=True,
        timeout=600,
    )
    subprocess.run(
        [str(python), "-m", "compileall", "-q", str(app_dir)],
        check=True,
        timeout=120,
    )
    for service in plan["services"]:
        subprocess.run(["systemctl", "restart", service], check=True, timeout=60)
    for path in ("/", "/radio", "/hls/yorushika.m3u8"):
        subprocess.run(
            [
                "curl",
                "--fail",
                "--silent",
                "--show-error",
                "--max-time",
                "15",
                "--header",
                f"Host: {host_header}",
                f"http://127.0.0.1{path}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            timeout=30,
        )

    manifest_path = snapshot.with_name(f"{snapshot.name}.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    record_deployed_version(
        state_file=state_file,
        commit=manifest["commit"],
        branch=manifest["branch"],
        source="rollback",
    )
    plan["status"] = "ok"
    plan["safetySnapshot"] = safety_snapshot["snapshot"]
    return plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="create a complete code snapshot")
    create.add_argument("--app-dir", type=pathlib.Path, default=DEFAULT_APP_DIR)
    create.add_argument("--backup-dir", type=pathlib.Path, default=DEFAULT_BACKUP_DIR)
    create.add_argument("--state-file", type=pathlib.Path, default=DEFAULT_STATE_FILE)
    create.add_argument("--keep", type=int, default=5)
    create.add_argument("--prune", choices=("report", "apply"), default="report")

    rollback = subparsers.add_parser("rollback", help="plan or apply a rollback")
    rollback.add_argument("snapshot", type=pathlib.Path)
    rollback.add_argument("--app-dir", type=pathlib.Path, default=DEFAULT_APP_DIR)
    rollback.add_argument("--backup-dir", type=pathlib.Path, default=DEFAULT_BACKUP_DIR)
    rollback.add_argument("--state-file", type=pathlib.Path, default=DEFAULT_STATE_FILE)
    rollback.add_argument("--host-header", default="81.68.72.245")
    rollback.add_argument(
        "--apply",
        action="store_true",
        help="perform the rollback; without this flag only a plan is printed",
    )

    record = subparsers.add_parser(
        "record",
        help="record the commit that passed deployment health checks",
    )
    record.add_argument("--commit", required=True)
    record.add_argument("--branch", required=True)
    record.add_argument("--source", default="deploy")
    record.add_argument("--state-file", type=pathlib.Path, default=DEFAULT_STATE_FILE)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "create":
        result = create_snapshot(
            app_dir=args.app_dir,
            backup_dir=args.backup_dir,
            keep=args.keep,
            prune_mode=args.prune,
            state_file=args.state_file,
        )
    elif args.command == "rollback":
        result = rollback_snapshot(
            snapshot=args.snapshot,
            app_dir=args.app_dir,
            backup_dir=args.backup_dir,
            apply=args.apply,
            state_file=args.state_file,
            host_header=args.host_header,
        )
    else:
        result = {
            "status": "ok",
            "stateFile": str(
                record_deployed_version(
                    state_file=args.state_file,
                    commit=args.commit,
                    branch=args.branch,
                    source=args.source,
                )
            ),
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
