# Project Progress

> Updated: 2026-07-28 (Asia/Shanghai)

## Current Stage
- Stage: `Phase 4 archive-about release candidate`
- Meaning: The About page now explains the archive's purpose, evidence rules,
  private-listening boundary and build history instead of presenting an unrelated
  developer profile. It has passed local automated and browser acceptance.

## Phase 2 Production Baseline
1. Replaced the generic Music Hub presentation with the reviewed
   `夜鹿集 / YORUSHIKA ARCHIVE` editorial identity.
2. Rebuilt the home page around a daily selection, listening paths and release
   spotlights instead of chart-like song columns.
3. Added `/discography` filters and `/songs/<slug>` detail pages with release-local
   previous/next navigation.
4. Expanded the curated catalog from 20 tracks to 8 releases and 63 lyric-listed
   tracks while
   preserving official release order and source URLs.
5. Restored 20 manually verified Bilibili video links; tracks without a verified
   video keep only the official release source.
6. Added eight compressed release-cover assets and a permanent design-system record.
7. Expanded the automated suite to 52 tests and completed desktop/mobile browser
   regression with no console errors or horizontal overflow.

## Phase 3 Production Release
1. Re-audited the same eight releases against their complete official release pages
   instead of relying on lyric-only listings.
2. Expanded the catalog from 63 to 89 tracks, including instrumental interludes and
   the ten `第一夜` to `第十夜` chapters in `幻燈`.
3. Added exact release dates, release-local track numbers and the `2026-07-28`
   source-audit date to the data model, migration and pages.
4. Increased manually checked Bilibili video entries from 20 to 24 without adding
   uncertain covers or re-uploads.
5. Fixed legacy synchronization so two tracks sharing one release cover cannot
   overwrite an already curated row.
6. The full automated suite passes with 54 tests. Desktop and 390 px mobile browser
   acceptance passed with no console errors or horizontal overflow; a verified
   Bilibili entry opened the expected video page in a separate tab.

## Phase 4 Release Candidate
1. Replaced the generic avatar, job-seeking badges and skill percentages with a
   site-specific `关于夜鹿集` introduction.
2. Added a curation-principles section that separates sourced release facts,
   personal listening notes and private Radio boundaries.
3. Added an archive-building timeline and an explicit list of what the site does
   and does not provide.
4. The release, track, video and source-check figures are computed from the curated
   database instead of copied into static text.
5. Kept browser-local favorites as a secondary private shelf at the end of the page.
6. The full 54-test suite passes. Desktop, dark-theme and 390 px mobile browser
   acceptance passed with no console errors or horizontal overflow; the mobile
   navigation opens with the correct expanded state.

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
- Archive home page with daily recommendation and listening paths.
- Discography page (`/discography`) with release filters and complete track order.
- Song detail pages (`/songs/<slug>`) with sources and adjacent tracks.
- Search page (`/search`).
- Song stories page (`/lyrics`).
- Radio page (`/radio`, optional `RADIO_STREAM_URL`).
- Archive About page and local favorites.

## Production Proof (2026-07-28)
1. Deployed commit `04f9199a6bac071e2dfd372e11d0dd0392b118e2`; the server
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

The Phase 3 release passed local acceptance and can be activated through the
documented deployment and rollback workflow.
