# Project Progress

## 当前审查修复（2026-10-19）

- 已核实：GitHub About 的 Website 仍是已停用的 `music.yoruming.cn`；它不是站内 About 模板。已清空 Website，并将描述与 README 明示为“无公开在线演示”，未以私人电台替代公开演示。
- 许可：有权许可的原创代码补 MIT；`THIRD_PARTY_NOTICES.md` 单列 Outfit 1.100 / OFL 1.1、Bootstrap Icons 1.11.1 / MIT、Bootstrap 5.3.0 / MIT。完整原许可随文件保存；Icons 两份字体与该上游版本逐字节一致，Outfit 内嵌版权与上游 OFL 对应，但生成批次未独立证明。42 份封面与 2 份 SVG 已逐项列出来源证据/未知项；所有封面的再分发许可仍待核，未改删原件，未纳入项目 MIT。
- 上线：本轮只有 GitHub 元数据、项目文档和三份静态许可文本，没有 UI/业务改动。三份许可已按白名单最小同步至受保护站点，Unix socket 实际 HTTP 200 且 SHA-256 与本地一致；Web 与 Radio 的 PID 均未变，未重启、迁移、读取生产记录或改认证。现有健康 service Result=success；首页/About/Radio/healthz/HLS 及许可文件未认证 HTTPS 均 401。未进行登录后浏览器/完整播放验收，历史验收不升级为本轮实时事实。
- 版本与恢复：应用 release 仍 `maintenance-20261002T113255Z`；许可增量 `license-notices-20261019`。运行清单由 111 增为 114 项，全部 SHA-256 匹配，整体指纹 `22e161a8c5fa2ba9bcd9836f89357b1e0a30b679f12d224b9bc19822372dcff1`。原版本记录和三文件 payload 保存在 `/var/backups/music-hub/content-releases/license-notices-20261019/`；回滚仅需将三份新增文本保留到备份后移出静态目录并恢复原版本记录，不需改服务/数据库；本轮未演练。
- 验证与交付：现有项目 .venv 在 `PYTHON_DOTENV_DISABLED=1`、临时 SQLite fixture 下 114 Python tests passed；12 Node frontend tests passed；文档链接、原许可与文件指纹检查通过；上游 OFL 原文的一处行尾空格原样保留，其余暂存文件 diff 检查通过。READY 仅限本轮新增文本和 About 元数据修正；封面授权、历史/远端附件的全面公开审计未完成，不对整个项目素材再分发给 READY。仓库本来已公开，本轮不新增媒体或改写旧 refs。
- Git 边界与下一步：本轮按明确授权只提交许可文件、第三方说明、README 相关修正与当前进度/运维记录的新节，保留原有 10-02 未提交维护改动。该维护内容已在服务器，但未混入本轮提交，Git HEAD 仍不能替代完整线上清单；后续完整 Git 对齐须另定范围。后续按用户新需求恢复；素材复用或新发布包前先补足授权证据。

> Updated: 2026-10-19 (Asia/Shanghai)

## Current Stage
- Stage: `Canonical main repository consolidation complete`
- Meaning: `main` carries the complete accepted hardening, archive redesign,
  four-Live Radio and authenticated-domain history. It is the sole long-lived
  public branch and the default deployment source.
- Repository content baseline: `96dab70` contains the 2026-08-23 HTTPS / Basic
  Auth versioned configuration and the sanitized legacy-IP template.
- Validation: 98 tests passed; Python compile, Flask import, Bash / POSIX shell
  syntax and Git diff checks passed. Local `nginx -t` was N/A because no Nginx
  runtime was available, and this Git-only closeout did not connect to production.
- Production boundary: no deploy, restart, DNS, firewall or server-file change
  was performed. The exact live version remains owned by the server-side
  `deployed-version.json` source of truth.

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

## Phase 6 Production Release
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
7. Commit `4ae5f5a` was accepted, pushed and deployed after the complete release
   catalog was reviewed in production.

## Phase 7 Production Release
1. Rechecked all 22 current music releases against the official Yorushika artist
   discography on `2026-07-29`; titles, dates, official URLs and release order match.
2. Rechecked complete legacy release pages where the current artist pages omit
   instrumental interludes. At this stage, the 122 stored positions were treated
   as complete; Phase 8 later superseded that conclusion for `二人称` with stronger
   official release and score evidence.
3. Confirmed the two identical `二人称` and `プレイシック` cover files match two
   distinct official image URLs that currently return the same official artwork.
4. Confirmed all 24 stored Bilibili links are reachable and their page titles match
   the intended tracks. This does not prove official authorization or future
   availability.
5. Defined the catalog scope as music releases under the official Yorushika artist
   tab, excluding live video products, the letter-format novel and suis / n-buna
   solo works.
6. Updated page and document wording so official release facts, third-party link
   checks and personal listening notes no longer share an ambiguous evidence label.
7. The full 80-test suite passes. Desktop and 390 px mobile browser regression
   passed for the discography, About, release archive and song detail pages with
   no console warnings/errors or horizontal overflow.
8. Commit `3bd67d87c132e8990ac0e5b44a77a7b45127bce3` was accepted, pushed
   and deployed as the current production baseline.

## Phase 8 Production Release
1. Replaced the 14 factual-only release overviews with complete archives. Every one
   of the 22 releases now separates official facts, personal listening notes,
   non-official listening paths, the complete official sequence and source links.
2. Used official release and news pages for every new archive. Unsupported
   interpretation remains explicitly labelled as a personal note rather than an
   official production fact.
3. Corrected `二人称` from 20 to 22 tracks after its official release announcement
   identified the opening `早朝、郵便受け` and closing `海へ`; the official score
   announcement independently distinguishes these two as instrumental pieces.
4. The normalized catalog now contains 111 canonical tracks and 124 ordered
   placements. All release-story chapter sequences are checked against the stored
   official sequence.
5. Expanded archive, catalog, route and migration coverage to 94 passing tests.
6. Desktop and 390 px mobile browser regression covered the discography, the
   22-track album archive, a digital-single archive, song detail navigation and
   the expanded mobile menu. There were no console warnings/errors or horizontal
   overflow.
7. Commit `2a3ea91522d7b94d6404d4bcb3577cabe197d534` was accepted,
   pushed and deployed after a complete code snapshot and verified MySQL backup.
   The Web/database/Radio health check passed, desktop and 390 px production
   browser checks produced no console warnings/errors or horizontal overflow, and
   the separate Personal Knowledge Hub remained HTTP 200.

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
- Twenty-two evidence-bounded editorial release archives.
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

The last repository-recorded deployed application before this closeout is
`ff9d974`. The 2026-08-30 branch consolidation is Git-only and does not replace
the server-side `deployed-version.json` as the production source of truth.
