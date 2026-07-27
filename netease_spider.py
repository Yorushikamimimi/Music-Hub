"""Backward-compatible catalog sync entrypoint.

The original script scraped third-party rankings and dropped production tables.
Catalog maintenance is now deterministic and non-destructive.
"""

from app import create_app
from catalog_service import sync_catalog


def main():
    app = create_app()
    with app.app_context():
        result = sync_catalog()
    print(
        "Catalog synchronized: "
        f"created={result['created']} "
        f"updated={result['updated']} "
        f"total={result['total']}"
    )


if __name__ == "__main__":
    main()

