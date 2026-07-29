# Project Progress

> Updated: 2026-07-28 (Asia/Shanghai)

## Current Stage
- Stage: `Phase 6 normalized full discography release candidate`
- Meaning: The local release candidate now covers 22 official releases, 109 unique
  tracks and 122 release positions. Shared tracks keep one canonical record while
  preserving their position and navigation inside every release. This phase has
  not been committed, pushed or deployed yet.

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

## Phase 5 Production Release
1. Added `/releases/tousaku` as the first complete release archive rather than
   sending every album interaction directly to a flat track list.
2. Kept official release facts and their three source links separate from the
   site's explicitly labelled personal listening note.
3. Added three editorial listening paths while preserving the official 14-track
   order as the primary catalog sequence.
4. Preserved internal song-detail navigation and exposed five manually verified
   Bilibili video links as separate external actions.
5. Linked the release archive from the home album thread, discography cover/title
   and song-detail breadcrumb.
6. Hardened the deployment clone step with forced HTTP/1.1, three bounded attempts
   and increasing delays; a fresh branch clone from GitHub succeeded.
7. The full 57-test suite passes. Desktop light/dark and 390 px mobile browser
   acceptance passed with no console warnings, errors or horizontal overflow.
   Mobile navigation and 44 px controls were verified.
8. Production commit `81194672d54778a9c227c49997a48aa6025386d2` was deployed
   after a verified code snapshot and MySQL backup. The first health check reached
   HLS before its playlist existed; a repeat after Radio startup passed all Web,
   database, Nginx, Radio schedule and HLS checks, and the deployed-version state
   was recorded with the exact commit.
9. Production desktop and 390 px mobile acceptance confirmed 14 tracks, three
   listening paths, the verified `思想犯` Bilibili link, zero browser warnings or
   errors and no horizontal overflow. `https://yoruming.cn/` remained HTTP 200.

## Phase 6 Release Candidate
1. Added all 22 releases listed by the official discography at the review date,
   including `二人称` and 13 previously missing digital singles.
2. Normalized tracks, releases and release-track positions into separate models:
   109 canonical tracks now produce 122 ordered placements without duplicated song
   records.
3. Added official release dates, source links and compressed local covers for the
   14 newly represented releases.
4. Kept the eight editorial release archives and added a factual overview template
   for the other 14 releases without inventing background interpretation.
5. Added release-context song navigation, all-release appearances and permanent
   redirects from four legacy duplicate track slugs.
6. Added an additive migration with a data-preserving downgrade path and expanded
   catalog, route and migration coverage.

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
- Discography page (`/discography`) with 22 release filters and complete track order.
- Eight editorial release archives plus 14 source-backed release overviews.
- Song detail pages (`/songs/<slug>`) with release context, sources and adjacent tracks.
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

The deployed Phase 5 release remains the production baseline. Phase 6 is local-only
until final verification and explicit approval to commit, push and deploy.
