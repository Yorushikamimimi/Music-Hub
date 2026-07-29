"""Normalize releases and track memberships without removing legacy fields.

Revision ID: 20260728_0003
Revises: 20260728_0002
Create Date: 2026-07-28
"""

from datetime import date

from alembic import op
import sqlalchemy as sa


revision = "20260728_0003"
down_revision = "20260728_0002"
branch_labels = None
depends_on = None

RELEASE_TABLE = "yorushika_release"
MEMBERSHIP_TABLE = "yorushika_release_track"
TRACK_TABLE = "music_yorushika"

LEGACY_RELEASES = (
    (
        "haru",
        "晴る",
        "Digital Single",
        date(2024, 1, 5),
        "release_haru.webp",
        "https://yorushika.com/discography/detail/37/",
    ),
    (
        "gentou",
        "幻燈",
        "Music Art Book",
        date(2023, 4, 5),
        "release_gentou.webp",
        "https://yorushika.com/discography/detail/30/",
    ),
    (
        "sousaku",
        "創作",
        "EP",
        date(2021, 1, 27),
        "release_sousaku.webp",
        "https://yorushika.com/discography/detail/18/",
    ),
    (
        "tousaku",
        "盗作",
        "Full Album",
        date(2020, 7, 29),
        "release_tousaku.webp",
        "https://yorushika.com/discography/detail/15/",
    ),
    (
        "elma",
        "エルマ",
        "Full Album",
        date(2019, 8, 28),
        "release_elma.webp",
        "https://yorushika.com/discography/detail/2/",
    ),
    (
        "dakara-boku-wa-ongaku-wo-yameta",
        "だから僕は音楽を辞めた",
        "Full Album",
        date(2019, 4, 10),
        "release_dakara_boku.webp",
        "https://yorushika.com/discography/detail/6/",
    ),
    (
        "makeinu-ni-encore-wa-iranai",
        "負け犬にアンコールはいらない",
        "Mini Album",
        date(2018, 5, 9),
        "release_makeinu.webp",
        "https://yorushika.com/discography/detail/7/",
    ),
    (
        "natsukusa-ga-jama-wo-suru",
        "夏草が邪魔をする",
        "Mini Album",
        date(2017, 6, 28),
        "release_natsukusa.webp",
        "https://yorushika.com/discography/detail/8/",
    ),
)


def upgrade():
    op.create_table(
        RELEASE_TABLE,
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("release_type", sa.String(length=80), nullable=False),
        sa.Column("release_date", sa.Date(), nullable=False),
        sa.Column("cover_path", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=False),
        sa.Column("source_checked_at", sa.Date(), nullable=False),
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
            server_default=sa.true(),
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
        sa.UniqueConstraint("title", name="uq_yorushika_release_title"),
    )
    op.create_index(
        "ix_yorushika_release_slug",
        RELEASE_TABLE,
        ["slug"],
        unique=True,
    )
    op.create_index(
        "ix_yorushika_release_date",
        RELEASE_TABLE,
        ["release_date"],
        unique=False,
    )
    op.create_index(
        "ix_yorushika_release_display_order",
        RELEASE_TABLE,
        ["display_order"],
        unique=False,
    )
    op.create_index(
        "ix_yorushika_release_is_featured",
        RELEASE_TABLE,
        ["is_featured"],
        unique=False,
    )

    op.create_table(
        MEMBERSHIP_TABLE,
        sa.Column("release_id", sa.Integer(), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("track_number", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["release_id"],
            [f"{RELEASE_TABLE}.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["track_id"],
            [f"{TRACK_TABLE}.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("release_id", "track_id"),
        sa.UniqueConstraint(
            "release_id",
            "track_number",
            name="uq_yorushika_release_track_number",
        ),
    )

    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if TRACK_TABLE not in inspector.get_table_names():
        return

    release_table = sa.table(
        RELEASE_TABLE,
        sa.column("id", sa.Integer()),
        sa.column("slug", sa.String()),
        sa.column("title", sa.String()),
        sa.column("release_type", sa.String()),
        sa.column("release_date", sa.Date()),
        sa.column("cover_path", sa.String()),
        sa.column("source_url", sa.String()),
        sa.column("source_checked_at", sa.Date()),
        sa.column("display_order", sa.Integer()),
        sa.column("is_featured", sa.Boolean()),
    )
    track_table = sa.table(
        TRACK_TABLE,
        sa.column("id", sa.Integer()),
        sa.column("album_title", sa.String()),
        sa.column("track_number", sa.Integer()),
        sa.column("is_featured", sa.Boolean()),
    )
    membership_table = sa.table(
        MEMBERSHIP_TABLE,
        sa.column("release_id", sa.Integer()),
        sa.column("track_id", sa.Integer()),
        sa.column("track_number", sa.Integer()),
    )

    for display_order, release in enumerate(LEGACY_RELEASES, start=1):
        slug, title, release_type, release_date, cover_path, source_url = release
        bind.execute(
            release_table.insert().values(
                slug=slug,
                title=title,
                release_type=release_type,
                release_date=release_date,
                cover_path=cover_path,
                source_url=source_url,
                source_checked_at=date(2026, 7, 28),
                display_order=display_order,
                is_featured=True,
            )
        )
        release_id = bind.execute(
            sa.select(release_table.c.id).where(
                release_table.c.slug == slug,
            )
        ).scalar_one()
        existing_tracks = bind.execute(
            sa.select(
                track_table.c.id,
                track_table.c.track_number,
            )
            .where(track_table.c.album_title == title)
            .where(track_table.c.is_featured.is_(True))
            .order_by(track_table.c.track_number, track_table.c.id)
        ).all()
        if existing_tracks:
            bind.execute(
                membership_table.insert(),
                [
                    {
                        "release_id": release_id,
                        "track_id": track_id,
                        "track_number": track_number,
                    }
                    for track_id, track_number in existing_tracks
                ],
            )


def downgrade():
    op.drop_table(MEMBERSHIP_TABLE)
    op.drop_index(
        "ix_yorushika_release_is_featured",
        table_name=RELEASE_TABLE,
    )
    op.drop_index(
        "ix_yorushika_release_display_order",
        table_name=RELEASE_TABLE,
    )
    op.drop_index(
        "ix_yorushika_release_date",
        table_name=RELEASE_TABLE,
    )
    op.drop_index(
        "ix_yorushika_release_slug",
        table_name=RELEASE_TABLE,
    )
    op.drop_table(RELEASE_TABLE)
