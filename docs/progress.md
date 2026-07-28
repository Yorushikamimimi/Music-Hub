# Project Progress

> Updated: 2026-07-28 (Asia/Shanghai)

## Current Stage
- Stage: `Reliability baseline live`
- Meaning: The selected content, privacy, migration, performance and non-root runtime
  work is live. Automated health, backup, failure recording and rollback tooling is
  installed, enabled and production-verified on the private server.

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
- Added 43 automated tests covering routes, catalog, CSP, migrations, Radio schedule
  and reliability safety boundaries.

## Current Deliverables
- Home page with daily recommendation.
- Search page (`/search`).
- Song stories page (`/lyrics`).
- Radio page (`/radio`, optional `RADIO_STREAM_URL`).
- About page and local favorites.

## Production Proof (2026-07-28)
1. Deployed commit `fd4fa94957c9d0103ca82691f64c52fd96ab2cc6`; the server
   worktree is clean and the prior releases have checksum-protected snapshots.
2. Ran the full Web/database/Radio health service successfully and enabled the
   five-minute timer. The daily backup timer is enabled for the 03:20 window.
3. Created a mode-`0600` MySQL backup, verified its SHA-256 and gzip integrity,
   restored it into an isolated MySQL 8 container, found `music_yorushika`, and
   confirmed the temporary container was removed.
4. Ran rollback in plan-only mode against the previous release. The command reported
   `databaseRollback=false` and did not change the current commit or worktree.
5. Triggered a harmless transient systemd failure, confirmed the dedicated failure
   record and journal entry, then removed the self-test state.
6. Regressed desktop and 390 px mobile Home/Radio pages with no console errors or
   horizontal overflow; mobile navigation, current-track metadata and 25% initial
   volume were present. The Playwright Chromium build does not support native HLS,
   so audible playback remains outside this automated proof.
7. Confirmed `https://yoruming.cn/` still served the Personal Knowledge Hub after
   the Music Hub Web restart.

The visual redesign remains intentionally deferred until a separate design version can be reviewed.
