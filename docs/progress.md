# Project Progress

> Updated: 2026-03-21 (Asia/Shanghai)

## Current Stage
- Stage: `Online Stabilization`
- Meaning: Core pages are online and accessible. Focus is now on stability and operations.

## Completed in This Round
1. Availability fixes
- Fixed `/search` 500 by importing `request`.
- Restored `/lyrics` and `/radio` routes.

2. Homepage UX fixes
- Fixed daily pick rendering issues.
- Removed distracting right-side music decoration.
- Fixed duplicated rating text (such as `HOT HOT`).

3. Encoding risk mitigation
- Switched key templates to safe fallback text to avoid `????` in production.

4. Ops workflow
- Verified deploy/restart/check flow with `systemctl` + `curl`.
- Added hotfix flow for uploading only changed files.

## Current Deliverables
- Home page with daily recommendation.
- Search page (`/search`).
- Song stories page (`/lyrics`).
- Radio page (`/radio`, optional `RADIO_STREAM_URL`).
- About page and local favorites.

## Next Steps
1. i18n cleanup
- Re-introduce Chinese copy with a strict UTF-8 content pipeline.

2. Release path hardening
- Use `local package + scp` as default deployment path on weak networks.

3. Monitoring
- Add minimal checks: service status, 5xx trend, certificate expiry reminder.
