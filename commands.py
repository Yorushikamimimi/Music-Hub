"""Flask CLI commands for deterministic catalog maintenance."""

import click

from catalog_service import sync_catalog
from models import db


def register_commands(app):
    @app.cli.command("catalog-sync")
    @click.option("--dry-run", is_flag=True, help="Validate changes without committing.")
    def catalog_sync_command(dry_run):
        """Create or update the curated Yorushika catalog."""
        result = sync_catalog(commit=not dry_run)
        if dry_run:
            db.session.rollback()
        click.echo(
            "Catalog sync: "
            f"created={result['created']} "
            f"updated={result['updated']} "
            f"total={result['total']} "
            f"dry_run={dry_run}"
        )
