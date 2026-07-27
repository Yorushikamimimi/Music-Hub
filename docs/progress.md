# Project Progress

> Updated: 2026-07-28 (Asia/Shanghai)

## Current Stage
- Stage: `Hardening release candidate`
- Meaning: Selected content, privacy, migration, performance and runtime work is
  implemented locally. Production activation is pending a controlled maintenance step.

## Completed in This Round
1. Performance
- Re-encoded 20 covers as WebP and removed roughly 20 MB of redundant CJK font files.
- Added one-day caching for versioned static assets and reduced Gunicorn target workers from 3 to 2.

2. Content and data
- Replaced fabricated ranking/HOT data with a 20-track curated catalog.
- Added real album/release metadata, original summaries and official source links.
- Replaced the destructive crawler with an idempotent catalog sync.

3. Privacy and accessibility
- Radio is explicitly private, manual-play only and excluded from search indexing.
- Added a functional mobile navigation toggle, keyboard Escape support, focus states,
  landmarks and touch-size controls without changing the overall visual direction.

4. Operations and reliability
- Added additive Flask/Alembic migrations that preserve legacy columns for rollback.
- Added hash-locked runtime and development dependency sets.
- Added non-root target units for Web and Radio plus a no-restart preparation script.
- Added 21 automated tests covering routes, catalog, CSP, migrations and Radio schedule.

## Current Deliverables
- Home page with daily recommendation.
- Search page (`/search`).
- Song stories page (`/lyrics`).
- Radio page (`/radio`, optional `RADIO_STREAM_URL`).
- About page and local favorites.

## Pending Production Proof
1. Create the two system users and copy the Radio library to `/srv/media`.
2. Apply the additive database migration and catalog sync.
3. Install target systemd/Nginx configuration and restart both services.
4. Complete real desktop/mobile browser regression and live audio progression checks.
5. Recreate or otherwise firewall the MySQL container so port 3306 is not externally bound.

The visual redesign remains intentionally deferred until a separate design version can be reviewed.
