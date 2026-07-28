# Project Progress

> Updated: 2026-07-28 (Asia/Shanghai)

## Current Stage
- Stage: `Reliability hardening release candidate`
- Meaning: The selected content, privacy, migration, performance and non-root runtime
  work is live. Automated health, backup, failure recording and rollback tooling is
  implemented locally and pending a controlled production activation.

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
- Activated non-root Web and Radio units and restricted MySQL to localhost.
- Added a database-aware `/healthz` route and a five-minute full-path health timer.
- Added daily compressed MySQL backup tooling with checksum validation and exact-prefix
  retention that cannot remove the older manual full-server backup.
- Added complete pre-deploy code snapshots, deployed-version state and an explicit
  dry-run-first rollback command that preserves `.env`, uploads and the virtualenv.
- Added local failure-state recording in systemd journal and
  `/var/lib/music-hub-monitor/last-failure.json`.
- Added 41 automated tests covering routes, catalog, CSP, migrations, Radio schedule
  and reliability safety boundaries.

## Current Deliverables
- Home page with daily recommendation.
- Search page (`/search`).
- Song stories page (`/lyrics`).
- Radio page (`/radio`, optional `RADIO_STREAM_URL`).
- About page and local favorites.

## Pending Production Proof
1. Deploy the reliability scripts and install the new systemd units.
2. Run the health service once and enable its five-minute timer.
3. Create one live MySQL backup, restore it into an isolated temporary container,
   and enable the daily timer only after that proof passes.
4. Create one complete release snapshot and run rollback in plan-only mode.
5. Re-run desktop/mobile and real Radio playback regression after the Web restart.

The visual redesign remains intentionally deferred until a separate design version can be reviewed.
