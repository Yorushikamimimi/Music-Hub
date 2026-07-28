"""Add release provenance and official track order.

Revision ID: 20260728_0002
Revises: 20260728_0001
Create Date: 2026-07-28
"""

from alembic import op
import sqlalchemy as sa


revision = "20260728_0002"
down_revision = "20260728_0001"
branch_labels = None
depends_on = None

TABLE_NAME = "music_yorushika"

NEW_COLUMNS = (
    sa.Column("release_date", sa.Date(), nullable=True),
    sa.Column(
        "track_number",
        sa.Integer(),
        nullable=False,
        server_default=sa.text("0"),
    ),
    sa.Column("source_checked_at", sa.Date(), nullable=True),
)


def _column_names(bind):
    return {column["name"] for column in sa.inspect(bind).get_columns(TABLE_NAME)}


def upgrade():
    bind = op.get_bind()
    if TABLE_NAME not in sa.inspect(bind).get_table_names():
        return

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


def downgrade():
    bind = op.get_bind()
    if TABLE_NAME not in sa.inspect(bind).get_table_names():
        return

    columns = _column_names(bind)
    removable = [
        column.name for column in reversed(NEW_COLUMNS) if column.name in columns
    ]
    if bind.dialect.name == "sqlite" and removable:
        with op.batch_alter_table(TABLE_NAME, recreate="always") as batch_op:
            for column_name in removable:
                batch_op.drop_column(column_name)
    else:
        for column_name in removable:
            op.drop_column(TABLE_NAME, column_name)
