# Project Progress

> Updated: 2026-07-28 (Asia/Shanghai)

## Current Stage
- Stage: `Online Stabilization`
- Meaning: Core pages are online and accessible. Focus is now on stability and operations.

## Completed in This Round
1. Persistent Radio delivery
- Replaced the transient FFmpeg unit with a versioned `yorushika-radio.service`.
- Added deterministic playlist and schedule generation for 28 local tracks.
- Added current track, approximate progress, next track, LIVE state, and 25% initial volume.
- Added versioned systemd and IP-restricted Nginx configuration.
- Kept audio files and generated HLS segments outside Git.

2. Availability fixes
- Fixed `/search` 500 by importing `request`.
- Restored `/lyrics` and `/radio` routes.

3. Homepage UX fixes
- Fixed daily pick rendering issues.
- Removed distracting right-side music decoration.
- Fixed duplicated rating text (such as `HOT HOT`).

4. Encoding risk mitigation
- Switched key templates to safe fallback text to avoid `????` in production.

5. Ops workflow
- Verified deploy/restart/check flow with `systemctl` + `curl`.
- Added hotfix flow for uploading only changed files.

## Current Deliverables
- Home page with daily recommendation.
- Search page (`/search`).
- Song stories page (`/lyrics`).
- Radio page (`/radio`, optional `RADIO_STREAM_URL`).
- About page and local favorites.

## Next Steps
1. Repository-backed deployment
- Use the tracked systemd and Nginx files as the runtime source of truth.

2. i18n cleanup
- Re-introduce Chinese copy with a strict UTF-8 content pipeline.

3. Release path hardening
- Use `local package + scp` as default deployment path on weak networks.

4. Monitoring
- Add minimal checks: service status, 5xx trend, certificate expiry reminder.
