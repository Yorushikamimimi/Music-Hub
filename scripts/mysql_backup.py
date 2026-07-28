#!/usr/bin/env python3
"""Create, retain, and restore-test private Music Hub MySQL backups."""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
import pathlib
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time


DEFAULT_BACKUP_DIR = pathlib.Path("/var/backups/music-hub/mysql")
DEFAULT_CONTAINER = "mysql-server"
DEFAULT_IMAGE = "mysql:8.0"
BACKUP_NAME = re.compile(
    r"^musichub-mysql-\d{8}T\d{6}(?:\d{6})?Z\.sql\.gz$"
)


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_gzip_dump(path: pathlib.Path) -> None:
    total = 0
    prefix = bytearray()
    with gzip.open(path, "rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            total += len(chunk)
            if len(prefix) < 4096:
                prefix.extend(chunk[: 4096 - len(prefix)])
    if total == 0 or b"MySQL dump" not in prefix:
        raise RuntimeError("backup is empty or does not look like a MySQL dump")


def backup_files(backup_dir: pathlib.Path) -> list[pathlib.Path]:
    if not backup_dir.exists():
        return []
    return sorted(
        (
            path
            for path in backup_dir.iterdir()
            if path.is_file() and BACKUP_NAME.fullmatch(path.name)
        ),
        key=lambda path: (path.stat().st_mtime, path.name),
        reverse=True,
    )


def prune_backups(
    backup_dir: pathlib.Path,
    keep: int,
    apply: bool,
) -> list[pathlib.Path]:
    if keep < 1:
        raise ValueError("keep must be at least 1")

    candidates = backup_files(backup_dir)[keep:]
    if apply:
        for backup in candidates:
            backup.unlink()
            checksum = backup.with_name(f"{backup.name}.sha256")
            checksum.unlink(missing_ok=True)
    return candidates


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"required command is missing: {command}")


def required_environment(name: str) -> str:
    value = os.environ.get(name, "")
    if not value or "\x00" in value or "\r" in value or "\n" in value:
        raise RuntimeError(f"required protected environment value is unavailable: {name}")
    return value


def mysql_option_value(value: str) -> str:
    """Quote a value for a temporary MySQL option file."""
    if "\x00" in value or "\r" in value or "\n" in value:
        raise ValueError("MySQL option value contains a forbidden control character")
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def install_temporary_client_config(
    container: str,
    path: str,
    database_user: str,
    database_password: str,
) -> None:
    content = (
        "[client]\n"
        f"user={mysql_option_value(database_user)}\n"
        f"password={mysql_option_value(database_password)}\n"
        "protocol=socket\n"
    ).encode("utf-8")
    installed = subprocess.run(
        [
            "docker",
            "exec",
            "--interactive",
            container,
            "sh",
            "-ec",
            'umask 077; cat > "$1"',
            "sh",
            path,
        ],
        input=content,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if installed.returncode != 0:
        raise RuntimeError(
            installed.stderr.decode("utf-8", errors="replace").strip()
            or "could not install the temporary MySQL client configuration"
        )


def create_backup(
    backup_dir: pathlib.Path,
    container: str,
    keep: int,
    prune_mode: str,
) -> dict:
    require_command("docker")
    require_command("gzip")
    database_name = required_environment("DB_NAME")
    database_user = required_environment("DB_USER")
    database_password = required_environment("DB_PASSWORD")
    if not re.fullmatch(r"[A-Za-z0-9_$-]+", database_name):
        raise RuntimeError("database name contains unsupported characters")

    backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(backup_dir, 0o700)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = backup_dir / f"musichub-mysql-{timestamp}.sql.gz"
    partial = target.with_name(f".{target.name}.partial")
    partial.unlink(missing_ok=True)
    client_config = f"/tmp/musichub-backup-{os.getpid()}.cnf"

    dump_command = [
        "docker",
        "exec",
        container,
        "sh",
        "-ec",
        (
            "exec mysqldump "
            '--defaults-extra-file="$1" '
            "--single-transaction --quick --skip-lock-tables --no-tablespaces "
            '--skip-triggers --databases "$2"'
        ),
        "sh",
        client_config,
        database_name,
    ]

    old_umask = os.umask(0o077)
    try:
        install_temporary_client_config(
            container=container,
            path=client_config,
            database_user=database_user,
            database_password=database_password,
        )
        with tempfile.TemporaryFile() as dump_stderr, partial.open("xb") as output:
            dump_process = subprocess.Popen(
                dump_command,
                stdout=subprocess.PIPE,
                stderr=dump_stderr,
            )
            if dump_process.stdout is None:
                raise RuntimeError("failed to capture mysqldump output")
            gzip_result = subprocess.run(
                ["gzip", "-9"],
                stdin=dump_process.stdout,
                stdout=output,
                capture_output=False,
                check=False,
            )
            dump_process.stdout.close()
            dump_return_code = dump_process.wait(timeout=300)
            dump_stderr.seek(0)
            dump_error = dump_stderr.read(8192).decode("utf-8", errors="replace").strip()
    except Exception:
        partial.unlink(missing_ok=True)
        raise
    finally:
        os.umask(old_umask)
        subprocess.run(
            ["docker", "exec", container, "rm", "-f", client_config],
            check=False,
            capture_output=True,
            timeout=30,
        )

    if dump_return_code != 0 or gzip_result.returncode != 0:
        partial.unlink(missing_ok=True)
        detail = dump_error or "mysqldump or gzip exited unsuccessfully"
        raise RuntimeError(detail)

    verify_gzip_dump(partial)
    os.replace(partial, target)
    os.chmod(target, 0o600)
    checksum = sha256_file(target)
    checksum_file = target.with_name(f"{target.name}.sha256")
    checksum_file.write_text(f"{checksum}  {target.name}\n", encoding="ascii")
    os.chmod(checksum_file, 0o600)

    candidates = prune_backups(
        backup_dir,
        keep=keep,
        apply=prune_mode == "apply",
    )
    return {
        "status": "ok",
        "backup": str(target),
        "bytes": target.stat().st_size,
        "sha256": checksum,
        "retention": {
            "keep": keep,
            "mode": prune_mode,
            "candidates": [path.name for path in candidates],
        },
    }


def docker_exec_with_stdin(
    container: str,
    command: str,
    source,
    timeout: int,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "exec", "--interactive", container, "sh", "-ec", command],
        stdin=source,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def verify_restore(
    backup: pathlib.Path,
    image: str,
    timeout: int,
) -> dict:
    require_command("docker")
    verify_gzip_dump(backup)

    container = f"musichub-restore-check-{os.getpid()}"
    password = secrets.token_urlsafe(32)
    env_path: pathlib.Path | None = None
    started = False

    try:
        env_directory = pathlib.Path("/run") if pathlib.Path("/run").is_dir() else None
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix="musichub-restore-",
            suffix=".env",
            dir=env_directory,
            delete=False,
        ) as env_file:
            env_file.write(f"MYSQL_ROOT_PASSWORD={password}\n")
            env_path = pathlib.Path(env_file.name)
        os.chmod(env_path, 0o600)

        start = subprocess.run(
            [
                "docker",
                "run",
                "--detach",
                "--rm",
                "--name",
                container,
                "--network",
                "none",
                "--env-file",
                str(env_path),
                image,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if start.returncode != 0:
            raise RuntimeError(start.stderr.strip() or "temporary MySQL did not start")
        started = True

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            ready = subprocess.run(
                [
                    "docker",
                    "exec",
                    container,
                    "sh",
                    "-ec",
                    'mysqladmin ping --silent --user=root --password="$MYSQL_ROOT_PASSWORD"',
                ],
                check=False,
                capture_output=True,
                timeout=10,
            )
            if ready.returncode == 0:
                break
            time.sleep(2)
        else:
            raise RuntimeError("temporary MySQL did not become ready")

        with gzip.open(backup, "rb") as dump_source:
            imported = docker_exec_with_stdin(
                container,
                'exec mysql --user=root --password="$MYSQL_ROOT_PASSWORD"',
                dump_source,
                timeout=max(timeout, 60),
            )
        if imported.returncode != 0:
            raise RuntimeError(
                imported.stderr.decode("utf-8", errors="replace").strip()
                or "restore import failed"
            )

        query = subprocess.run(
            [
                "docker",
                "exec",
                container,
                "sh",
                "-ec",
                (
                    "exec mysql --batch --skip-column-names "
                    '--user=root --password="$MYSQL_ROOT_PASSWORD" '
                    "-e \"SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_name='music_yorushika';\""
                ),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if query.returncode != 0:
            raise RuntimeError(query.stderr.strip() or "restore verification query failed")
        table_count = int(query.stdout.strip())
        if table_count < 1:
            raise RuntimeError("restored backup does not contain music_yorushika")

        return {
            "status": "ok",
            "backup": str(backup),
            "musicTableCount": table_count,
            "ephemeralContainer": True,
        }
    finally:
        if started:
            subprocess.run(
                ["docker", "rm", "--force", container],
                check=False,
                capture_output=True,
                timeout=30,
            )
        if env_path is not None:
            env_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup = subparsers.add_parser("backup", help="create a compressed backup")
    backup.add_argument("--backup-dir", type=pathlib.Path, default=DEFAULT_BACKUP_DIR)
    backup.add_argument("--container", default=DEFAULT_CONTAINER)
    backup.add_argument("--keep", type=int, default=14)
    backup.add_argument(
        "--prune",
        choices=("report", "apply"),
        default="report",
        help="report or delete exact-prefix backups outside the retention count",
    )

    verify = subparsers.add_parser(
        "verify",
        help="restore a backup into a temporary isolated MySQL container",
    )
    verify.add_argument("backup", type=pathlib.Path)
    verify.add_argument("--image", default=DEFAULT_IMAGE)
    verify.add_argument("--timeout", type=int, default=90)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "backup":
        result = create_backup(
            backup_dir=args.backup_dir,
            container=args.container,
            keep=args.keep,
            prune_mode=args.prune,
        )
    else:
        result = verify_restore(
            backup=args.backup.resolve(strict=True),
            image=args.image,
            timeout=args.timeout,
        )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
