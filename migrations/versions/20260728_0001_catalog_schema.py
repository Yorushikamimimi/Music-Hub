"""Add the curated Yorushika catalog schema.

Revision ID: 20260728_0001
Revises:
Create Date: 2026-07-28
"""

from alembic import op
import sqlalchemy as sa


revision = "20260728_0001"
down_revision = None
branch_labels = None
depends_on = None

TABLE_NAME = "music_yorushika"

NEW_COLUMNS = (
    sa.Column("slug", sa.String(length=120), nullable=True),
    sa.Column("title_ja", sa.String(length=255), nullable=True),
    sa.Column("title_en", sa.String(length=255), nullable=True),
    sa.Column("album_title", sa.String(length=255), nullable=True),
    sa.Column("release_type", sa.String(length=80), nullable=True),
    sa.Column("story_summary", sa.Text(), nullable=True),
    sa.Column("source_url", sa.String(length=500), nullable=True),
    sa.Column(
        "display_order",
        sa.Integer(),
        nullable=False,
        server_default=sa.text("0"),
    ),
    sa.Column(
        "is_featured",
        sa.Boolean(),
        nullable=False,
        server_default=sa.false(),
    ),
    sa.Column(
        "created_at",
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.now(),
    ),
)

INDEXES = (
    ("ix_music_yorushika_slug", ("slug",), True),
    ("ix_music_yorushika_release_year", ("release_year",), False),
    ("ix_music_yorushika_display_order", ("display_order",), False),
    ("ix_music_yorushika_is_featured", ("is_featured",), False),
)


def _column_names(bind):
    return {column["name"] for column in sa.inspect(bind).get_columns(TABLE_NAME)}


def _index_names(bind):
    return {index["name"] for index in sa.inspect(bind).get_indexes(TABLE_NAME)}


def _create_catalog_table():
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("title_ja", sa.String(length=255), nullable=True),
        sa.Column("title_en", sa.String(length=255), nullable=True),
        sa.Column("album_title", sa.String(length=255), nullable=True),
        sa.Column("release_type", sa.String(length=80), nullable=True),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.Column("cover_path", sa.String(length=255), nullable=True),
        sa.Column("link", sa.String(length=500), nullable=True),
        sa.Column("story_summary", sa.Text(), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "is_featured",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def upgrade():
    bind = op.get_bind()
    if TABLE_NAME not in sa.inspect(bind).get_table_names():
        _create_catalog_table()
    else:
        existing_columns = _column_names(bind)
        missing_columns = [
            column for column in NEW_COLUMNS if column.name not in existing_columns
        ]
        if bind.dialect.name == "sqlite" and missing_columns:
            with op.batch_alter_table(TABLE_NAME, recreate="always") as batch_op:
                for column in missing_columns:
                    batch_op.add_column(column)
        else:
            for column in missing_columns:
                op.add_column(TABLE_NAME, column)

        link_column = next(
            (
                column
                for column in sa.inspect(bind).get_columns(TABLE_NAME)
                if column["name"] == "link"
            ),
            None,
        )
        if (
            bind.dialect.name == "mysql"
            and link_column is not None
            and getattr(link_column["type"], "length", 0) < 500
        ):
            op.alter_column(
                TABLE_NAME,
                "link",
                existing_type=link_column["type"],
                type_=sa.String(length=500),
                existing_nullable=link_column["nullable"],
            )

    existing_indexes = _index_names(bind)
    columns = _column_names(bind)
    for name, index_columns, unique in INDEXES:
        if name not in existing_indexes and set(index_columns).issubset(columns):
            op.create_index(name, TABLE_NAME, list(index_columns), unique=unique)


def downgrade():
    bind = op.get_bind()
    if TABLE_NAME not in sa.inspect(bind).get_table_names():
        return

    columns = _column_names(bind)
    legacy_table = "album" in columns or "rating" in columns
    if not legacy_table:
        op.drop_table(TABLE_NAME)
        return

    existing_indexes = _index_names(bind)
    for name, _index_columns, _unique in reversed(INDEXES):
        if name in existing_indexes:
            op.drop_index(name, table_name=TABLE_NAME)

    removable_columns = [
        column.name for column in reversed(NEW_COLUMNS) if column.name in columns
    ]
    if bind.dialect.name == "sqlite" and removable_columns:
        with op.batch_alter_table(TABLE_NAME, recreate="always") as batch_op:
            for column_name in removable_columns:
                batch_op.drop_column(column_name)
    else:
        for column_name in removable_columns:
            op.drop_column(TABLE_NAME, column_name)
