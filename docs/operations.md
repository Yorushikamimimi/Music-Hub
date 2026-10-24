# Operations Guide

## 2026-10-19 公开入口与静态许可修复

GitHub About Website 已清空，描述注明无公开在线演示；未把私人 `radio.yoruming.cn` 作为公开 Demo。项目原创代码使用 MIT，第三方代码、字体、图像单列 `THIRD_PARTY_NOTICES.md`，封面公开再分发许可仍待核。

本轮仅上线 `static/fonts/OFL-Outfit.txt`、`static/fonts/LICENSE-bootstrap-icons.txt`、`static/css/LICENSE-bootstrap.txt` 三份静态原许可，未改页面、服务配置、认证、依赖、数据库或曲库；不因授权上线就执行无必要重启。部署前原 111 项指纹全匹配，现清单 114 项匹配；原记录与 payload 备份在 `/var/backups/music-hub/content-releases/license-notices-20261019/`，原应用 release 不变，增量 ID 为 `license-notices-20261019`。

实际验证：三份许可经 Unix socket HTTP 获取为 200 且指纹一致；未登录正式域名首页、About、Radio、healthz、HLS 和许可文本均 401，私人功能未被公开。Web/Radio PID 保持 `1681547`/`1681545`，NRestarts 均 0，健康 service Result=success。未读取凭证或生产数据，未做登录后页面/完整播放验收或回滚演练。现有 .venv 的隔离测试为 114 Python 与 12 Node tests passed，不等于私人站点所有流程验收。

版本状态、Git 范围和后续入口唯一见 `docs/progress.md` 顶部；本轮 commit/push 只覆盖审查修复，保留原有可靠性维护改动。

## Current Runtime

- Primary entry: `https://radio.yoruming.cn/`
- Primary access boundary: HTTPS plus HTTP Basic Auth for the complete origin, including `/hls/`
- Legacy rollback entry: `http://81.68.72.245/`, restricted to the existing Nginx source allowlist
- Reverse proxy: `Nginx`
- App server: `Gunicorn + Flask`
- App service: `musichub.service`
- Radio service: `yorushika-radio.service`
- App path: `/var/www/My_Homepage`
- App socket: `/run/musichub/musichub.sock`
- HLS runtime path: `/run/yorushika-radio/hls`
- Seekable loop cache: `/var/cache/yorushika-radio/loop.mka` (MP3 stream-copy,
  regenerated when the curated source fingerprint changes)
- Radio library: `/srv/media/yorushika-radio/music`
- Service identities: `musichub` and `musichub-radio` (no login shells)

The retired `music.yoruming.cn` entry is not part of the current runtime. The
`radio.yoruming.cn` certificate and Nginx server are independent of the main
`yoruming.cn` website.

The versioned legacy-IP template intentionally contains only localhost plus a
commented RFC 5737 TEST-NET example. Real owner source IPs belong only in the
server-local Nginx config and must never be committed. Runtime preparation
preserves an existing server-local legacy allowlist instead of overwriting it.

## Persistent Radio Design

`yorushika-radio.service` performs the full startup sequence:

1. Creates `/run/yorushika-radio/` through systemd `RuntimeDirectory`.
2. Runs `scripts/generate_radio_schedule.py`.
3. Builds a deterministic MP3 stream-copy Matroska cache from 57 reviewed files across
   2021 `Live「前世」`, 2022 `Live「月光」`, 2024 `Live「前世」` and
   2024 `Live「月と猫のダンス」`.
4. Probes the real duration of each track and writes `radio-schedule.json`.
5. Starts an audio-only FFmpeg HLS stream with `-stream_loop -1` on the seekable
   cache; normal playlist completion no longer exits the service.
6. Regenerates runtime files after service restart or server reboot.

The repository intentionally excludes the MP3 collection, generated HLS segments and cache,
`.env`, databases and virtual environments. Unknown MP3 files are ignored.

Before and after every Radio library replacement, archive the complete MP3 directory,
copy it off the server, and verify a SHA-256 manifest. Git preserves the curated order,
display names and runtime code, but is not a backup for the audio bytes.

The stream is a private, login-protected personal listening tool. It does not
autoplay, expose a download feature, provide public indexing, or reproduce full lyrics.

## Domain Authentication and TLS

- Nginx config: `/etc/nginx/conf.d/musichub-radio.conf`
- Versioned template: `deploy/nginx/musichub-radio.conf`
- Password hash: `/etc/nginx/.htpasswd-radio` (`root:www-data`, mode `0640`)
- Certificate: `/etc/letsencrypt/live/radio.yoruming.cn/`
- ACME webroot: `/var/www/certbot`
- Renewal deploy hook: `/etc/letsencrypt/renewal-hooks/deploy/reload-nginx`
- Pre-auth rollback config: `/var/backups/music-hub/nginx/musichub-radio-pre-auth-20260823T1115CST.conf`

The server stores only a password hash. The current plaintext credential is kept
in the owner's macOS Keychain under service `radio.yoruming.cn` and account
`Yorushika`; it must never be added to Git, Vault, `.env`, or operations logs.
Changing the password requires a separately confirmed credential rotation.

## Runtime Preparation

```bash
cd /var/www/My_Homepage
sudo bash scripts/prepare_server_runtime.sh
```

This keeps the locked service users and Radio library permissions, creates dedicated
backup/monitor directories, installs the versioned unit/Nginx files, runs
`nginx -t` and `systemd-analyze verify`, and stops before restarting or enabling
anything. It limits `.env` to `root:musichub` mode `0640` without printing it.

Before activation, verify:

```bash
id musichub
id musichub-radio
sudo -u musichub-radio test -r /srv/media/yorushika-radio/music
systemd-analyze verify deploy/systemd/musichub.service
systemd-analyze verify deploy/systemd/yorushika-radio.service
systemd-analyze verify deploy/systemd/music-hub-health.service
systemd-analyze verify deploy/systemd/music-hub-health.timer
systemd-analyze verify deploy/systemd/music-hub-backup.service
systemd-analyze verify deploy/systemd/music-hub-backup.timer
systemd-analyze verify deploy/systemd/music-hub-failure@.service
```

When Tian's public IPv4 changes, the authenticated HTTPS entry should continue
to work. Only SSH administration and the legacy IP rollback entry depend on
source-IP allowlists. Update those server-local rules only after explicit
approval; do not copy real client IPs back into the public repository template.

## Service Checks

```bash
systemctl status musichub.service --no-pager
systemctl status yorushika-radio.service --no-pager
systemctl is-enabled musichub.service yorushika-radio.service
journalctl -u musichub.service -n 100 --no-pager
journalctl -u yorushika-radio.service -n 100 --no-pager
```

## Health Checks

```bash
nginx -t
curl -I http://radio.yoruming.cn/
curl -I https://radio.yoruming.cn/
# Expect 401 without credentials; use an interactive prompt or protected local
# credential source for authenticated checks. Never put the password in docs.
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/radio
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/hls/yorushika.m3u8
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/hls/radio-schedule.json
python3 scripts/health_check.py
```

Browser acceptance should additionally prove:

1. Current track, approximate progress, and next track are populated.
2. Initial audio volume is `0.25` when no valid saved preference exists; keep an
   existing saved volume.
3. Playback advances with `readyState=4` and no media error.
4. Mobile layout has no horizontal overflow.
5. `https://yoruming.cn/` remains healthy because it is a separate project.
6. The unauthenticated domain returns `401`, a wrong password returns `401`,
   and authenticated page, static and HLS requests return `200`.
7. `certbot renew --cert-name radio.yoruming.cn --dry-run --run-deploy-hooks --non-interactive --no-random-sleep-on-renew` succeeds and the versioned hook validates and reloads Nginx.

## Deployment

`main` is the canonical public branch and the deployment script defaults to it.
Selecting another branch is an explicit maintenance override, not the normal
release path.

The 2026-10-02 maintenance was a verified content release from the working tree.
Its implementation is being saved in the 2026-10-24 Git delivery. Verify the
remote branch before any future pull-based deployment; this delivery does not
redeploy or update the production content manifest.

`scripts/deploy_music_hub.sh` keeps `.env`, `venv/`, uploads and the current
avatar; creates a complete pre-deploy code snapshot; installs hash-locked
dependencies; creates a verified pre-migration database backup; compiles the
app; applies additive migrations; synchronizes the catalog; restarts both
services; runs the full local health check; and records the commit that passed.

Because the script writes the database and restarts services, it requires an
explicit maintenance confirmation. Do not run it as a routine read-only check.

Before deploying, keep a known-good Git commit and the existing cloud snapshot.
Do not delete the legacy audio directory until live Radio playback is accepted.
The Git repository covers source and deployment configuration, not the MP3
collection, database or complete server state.

## Automated Health and Failure State

`music-hub-health.timer` runs every five minutes. The oneshot check proves:

1. `musichub.service`, `yorushika-radio.service` and `nginx.service` are active.
2. `/healthz` can execute a database query through the live Flask process.
3. The HLS playlist contains active media segments.
4. The Radio schedule remains private and contains tracks.

Run it manually before enabling the timer:

```bash
systemctl start music-hub-health.service
systemctl status music-hub-health.service --no-pager
journalctl -u music-hub-health.service -n 100 --no-pager
```

When the health or backup service fails, systemd starts
`music-hub-failure@.service`. The failure remains in journal and the latest
minimal status is written to:

```text
/var/lib/music-hub-monitor/last-failure.json
```

This is local error monitoring, not an off-server notification channel. It does
not send email, SMS or chat messages.

Production activation evidence before the Phase 3 catalog release:

- `music-hub-health.timer` and `music-hub-backup.timer` are enabled and waiting.
- A transient non-production failure invoked `music-hub-failure@.service`,
  produced the expected unit result, and was then cleaned up.
- The last recorded version before the Phase 3 catalog release was
  `04f9199a6bac071e2dfd372e11d0dd0392b118e2`.

## MySQL Backup and Restore Proof

systemd injects the existing protected application database variables into the
backup process. The script passes them to MySQL through a mode-`0600` temporary
option file inside the container, removes that file in `finally`, and never
prints the values or places them in command-line arguments. The dump is
compressed atomically, validated as a MySQL dump, hashed and stored with mode
`0600` under:

```text
/var/backups/music-hub/mysql/
```

The managed prefix is `musichub-mysql-*.sql.gz`. Retention keeps the newest
14 files and only deletes older files with that exact prefix in this dedicated
directory. The older manual backup under `/var/backups/mysql/` is outside this
scope and cannot be removed by the timer.

Manual proof before timer activation:

```bash
python3 scripts/mysql_backup.py backup --keep 14 --prune report
python3 scripts/mysql_backup.py verify \
  /var/backups/music-hub/mysql/<managed-backup>.sql.gz
```

`verify` starts a temporary MySQL 8 container with no published port or volume,
imports the dump, checks for `music_yorushika`, and removes the temporary
container. After one real restore proof passes, activate the scheduled job:

```bash
systemctl enable --now music-hub-backup.timer
systemctl list-timers music-hub-backup.timer --no-pager
```

The daily local backup is not an automatic off-server backup. Disk loss still
requires the separately maintained Mac copy or another off-host destination.

The first production proof created
`musichub-mysql-20260728T053055121496Z.sql.gz`, verified gzip and SHA-256
integrity, restored it in an isolated MySQL 8 container, found the
`music_yorushika` table, and removed the temporary container.

## Release Snapshots and Rollback

Each controlled deployment creates a complete code snapshot under:

```text
/var/backups/music-hub/releases/
```

Snapshots exclude `.env`, virtual environments, runtime caches, uploads and
avatar state. The newest five managed snapshots are retained. Each snapshot has
a checksum manifest and the deployed commit is recorded only after health checks
pass.

Rollback is dry-run-first:

```bash
python3 scripts/release_snapshot.py rollback \
  /var/backups/music-hub/releases/<snapshot>.tar.gz
```

The command above only prints the plan. Applying it requires an explicit flag:

```bash
python3 scripts/release_snapshot.py rollback \
  /var/backups/music-hub/releases/<snapshot>.tar.gz \
  --apply
```

An applied rollback first creates a safety snapshot, restores only application
code, preserves `.env`, `venv/`, uploads and reliability control scripts,
reinstalls locked dependencies, restarts Web and Radio, and checks the private
IP routes. It does not reverse database migrations; current migrations must
remain backward compatible or a separate confirmed database restore is needed.

## MySQL Network Boundary

The live MySQL container is published as `127.0.0.1:3306:3306`. The cloud
firewall still retains a server-self source rule, but the host no longer listens
for remote MySQL clients.

Changing the port binding requires a controlled container recreation with the
existing named volume and a user-supplied protected environment file. Do not
extract or print the running container's environment to reconstruct it. The
sequence must include a volume check, downtime notice, rollback container name,
local application query, and external port probe.

## 2026-10-02 只读审查（浏览器待验收）

以下保留审查当时的历史结论；后续实际修复与登录后验收见本页末尾维护发布记录。

### 大白话结论

截至当晚检查，网站服务器、数据库连通性和电台输出正常，没有发现持续宕机。
值得优先处理的是连续听歌的恢复能力、下一次部署的旧分支问题和备份防丢。
本轮没有实施任何修复；正式域名在 Chrome 要求登录，浏览器实际播放及手机布局仍待用户登录后补验，不能称为全部线上验收通过。

### 待选择的问题与优化

| 项目 | 已确认的证据与用户影响 | 建议 |
|---|---|---|
| 优先：电台循环与故障恢复 | 57 首歌单约 4.713 小时一轮；播完会正常退出、等待 3 秒、清理/重建 HLS 再启动。近 7 天 35 次重启；4 次健康检查失败均与该窗口重合，随后恢复。切换时确有 HLS 404，不代表已经测得浏览器断音时长。前端媒体错误只更新提示，时间表只取一次，初次获取失败不重试、后台重启后不刷新。 | 实现有上限的重连和时间表刷新；减少循环断流窗口，监控应容忍有界切换并核对分片新鲜度。补网络/重启回归测试。 |
| 下次部署前必须处理：默认分支与误删防护 | 服务器的 `scripts/deploy_music_hub.sh:8` 默认仍是 `codex/yorushika-redesign-prototype`，远端现场只存在 `main`，不传覆盖参数的默认部署会在 clone 阶段失败。本地默认已是 main。脚本 `:10,45-53` 允许覆盖临时目录且会递归删除该目录；错误设置路径可误删数据，未发现实际误删事故。 | 同步默认分支；使用自动创建的专用临时目录和删除边界校验。没有运行部署脚本或危险命令进行复现。 |
| 建议优先：异机备份与故障通知 | 每日备份已启用且成功，保留 14 份，最新为 2026-10-02 凌晨的备份，文件 mode 0600、gzip 与已记录 SHA-256 均通过。现有自动流程把备份放在生产服务器同盘；本轮核对到的 Mac Music Hub 数据库副本仍为 2026-08-07。失败只写本机 journal/JSON。 | 增加加密异机副本、定期隔离恢复验证和可被用户收到的故障通知；通知渠道和备份目的地由用户选定，不擅自连接外部服务。 |
| 可合并小修：存储不可用时降级 | `static/site.js:20` 和 `static/radio.js:347` 未保护 localStorage 读取；隔离 Node 模拟 SecurityError 时，两者在控件事件绑定前中断。`static/favorites.js:20` 写入失败会抛出异常，收藏操作没有失败提示。普通浏览器场景未证明正在发生此故障。 | 存储读写失败时保留默认主题/音量及页面操作，收藏失败明确提示；不能假装已保存。 |
| 安排维护：依赖安全公告 | 在线虚拟环境 31 个包经 OSV 按版本查询，8 个包命中公告：cryptography、idna、pip、python-dotenv、requests、setuptools、soupsieve、urllib3。命中不是 8 个已可通过本站利用的漏洞；维护工具、抓取工具和具体 API 的触发条件不同。 | 逐项核对可达调用路径、升级约束与哈希锁文件，先在隔离环境跑测试再发布。不能把“装有受影响版本”写成“网站已被攻破”。 |
| 顺带对齐：部署记录 | `/var/lib/music-hub-monitor/deployed-version.json` 仍记 2026-08-07 的 `ff9d974`。15 个核对的关键文件与本地 main 相同，含之后增加正式域名 Trusted Host 的 config 和 Radio 登录文案；服务器部署脚本另与 ff9d974 相同。实际是混合历史，记录不足以单独证明全部运行内容。 | 下一次受控发布记录完整来源与文件指纹；不要为使记录好看而只修改 commit 标签。 |

播放器证据位置：`static/radio.js:269-277,316-344,347-394`；
循环证据：`scripts/generate_radio_schedule.py:172-224` 和现场 systemd ExecStart/Restart；
当前健康检查只检查服务 active 和播放列表存在，没有分片新鲜度验证：`scripts/health_check.py:47-82`。
已有显式快照回滚，不将“没有自动回滚”本身当作必须修改的漏洞；数据库回滚需单独授权。

### 已实际验证的范围

- 正式 HTTPS 未登录首页与 HLS 均返回 401；HTTP 跳转 HTTPS。Nginx 配置检查通过，认证文件权限 0640，MySQL 只监听 127.0.0.1:3306；未读取任何密码、密钥、认证文件内容或环境秘密。
- 证书有效至 2026-11-21，续签 timer 在运行；本轮未执行会引起续签/重载的 dry-run。
- Web 和 Radio active，Web NRestarts=0；磁盘约 41% 使用，可用内存约 2.0 GiB，当前资源有余量，不代表压力测试结论。
- 通过现有 Unix socket 检查主要页面、搜索正常与异常参数、healthz、robots；全部 200。再遍历页面列出的 22 个发行详情地址与 134 个带发行上下文的歌曲地址，共 156 个详情请求全部 200；134 是地址数，不是唯一曲目数。32 项页面引用静态资源经现有本机 Nginx 入口全部 200。
- 现有白名单本机 HLS 入口连续解码 8 秒无错误；播放列表新鲜度采样约 1.69 秒，57 首时间表存在。此证据不是用户浏览器已成功播放。
- 近 7 天含轮转文件的两套 Music Hub Nginx 访问日志分别采样到 52、7316 条请求，没有 5xx；401/403 与登录和旧 IP 白名单一致，不能把所有被拒请求当故障。
- 健康检查 1869 次成功、4 次失败；失败时间（UTC）：09-27 13:54:27、09-28 22:54:51、09-30 07:54:59、10-01 16:55:21，均与正常循环启动窗口逐一对齐。没有发现同期 Web 持续失败。
- 本地 `main` 为 `ad1dc3e34e4a2352b81742ba107733418d09fd0f`；使用隔离临时 SQLite fixture、禁用 dotenv 加载与 pytest 缓存运行，98 tests passed（6.56 秒）。Node 模拟存储异常、100 次时间表渲染及媒体错误验证了前端风险。测试通过不等于真实浏览器交互通过。

### 依赖公告核对与边界

- `cryptography 46.0.5` 实际链接 OpenSSL 3.5.5；[维护者 OpenSSL 公告](https://github.com/pyca/cryptography/security/advisories/GHSA-537c-gmf6-5ccf) 对项目 wheel 要求至少 48.0.1；其他 PKCS#7/证书验证公告还需结合实际使用 API 核对，不能只升到这个单项最低版本就声称全部修复。
- `urllib3 2.6.3` 命中 [流式 Deflate 公告](https://github.com/urllib3/urllib3/security/advisories/GHSA-gh4c-6fx4-qh6g) 与 [HTTPS 代理配置公告](https://github.com/urllib3/urllib3/security/advisories/GHSA-8988-9cw3-xx77)，这些公告的修复版本为 2.8.0；本轮未证明本站公开请求能触发它们。
- `requests 2.32.5` 的 [维护者公告](https://github.com/psf/requests/security/advisories/GHSA-gc5v-m9x4-r6x2) 限定在特定解压辅助函数，普通 Requests 用法不受该项影响。
- `python-dotenv 1.2.1` 的 OSV 范围与 [维护者公告](https://github.com/theskumar/python-dotenv/security/advisories/GHSA-mf9w-mj56-hr94) 的 affected/patched 表述有不一致，且公告针对 set_key/unset_key；保留核对项，不计为本轮确认可利用漏洞。
- pip/setuptools 是安装链路；idna/soupsieve 的命中本轮只完成版本数据库比对，没有逐项利用分析。结果不涵盖全部系统包和云平台漏洞，也不是完整渗透或入侵取证。

### 尚未验证与下一步

- Chrome 新标签页访问正式域名停在 Basic Auth 登录提示；已请用户手动登录，不索取/读取凭证。本轮未完成登录后桌面/手机页面、播放、跨页不断播、深浅主题及收藏交互验收。
- 未做长时间播放、故障注入、服务重启、压力测试、最新备份的数据库恢复或整机灾备演练；没有批量重新验收第三方 Bilibili 链接。HLS 跨浏览器支持依赖运行环境，未把无 fallback 的代码直接宣称为 Chrome 不能播放。
- 建议先选电台稳定性和下次部署安全，再决定异机备份目的地与通知渠道；新功能和外观调整等待浏览器审查证据。
- 本次仅更新本项目审查与进度文档，未改业务代码、服务、数据库、媒体、认证、Nginx、防火墙；未 commit/push/deploy。
- 子代理 2 个，派发配置均为 `gpt-6-luna` + `high`、fork none；一个负责前端，一个负责后端。平台未提供独立运行元数据，实际配置无法独立验证，未收到替换或降级报告。根任务复核了文件指纹、代码位置、模拟结果和线上日志，不把子代理口头结论直接当事实。

## 2026-10-02 可靠性维护发布

### 结论与来源

修复版于 19:49 CST 上线，随后正式域名登录后的 Chrome 验收与服务器复查通过。
发布使用已有 server-ops MCP；原始曲库、生产数据库内容、认证、DNS、防火墙与
`/etc/nginx` 当前配置均未修改。仓库内旧部署模板补齐为 main 的版本，但没有重新运行
会覆盖服务器本地白名单的准备脚本，也没有执行数据库迁移或 catalog-sync。

- release：`maintenance-20261002T113255Z`
- 运行文件数：111；逐项 SHA-256 核验与服务器文件一致。
- 内容指纹：`778507fcbb7c0608b7250dae2723309c3195120ad0e6c8526f606f2171f116a1`；算法为按路径排序的文件 SHA 映射，使用 JSON `sort_keys=True, separators=(',', ':')` 编码后 SHA-256。
- 来源基线：本地 main `ad1dc3e34e4a2352b81742ba107733418d09fd0f` 加本轮未提交修改。不是已 commit/push 的新版本。
- 正式记录：`/var/lib/music-hub-monitor/deployed-version.json`，包含上述指纹和完整文件映射；`commit` 明示为 base commit、`gitDirty=true`，不能把它误读成当前内容的精确 Git commit。
- 服务使用的新环境：`/var/lib/music-hub-runtime/venvs/maintenance-20261002T113255Z`，通过 `/var/www/My_Homepage/venv` 的链接使用；不要移动新环境本体，启动脚本依赖其固定路径。

### 实际修复

- Radio：不直接循环不支持 seek 的 MP3 concat。将白名单音频以 `-c:a copy` 封装为 Matroska，无再次压缩、不改原 MP3；从 cache 无限循环并持续生成 HLS。cache 指纹包含源路径、大小、mtime 与时长，失效时原子重建；曲目时间表总时长对齐 cache，防止累计偏移。
- 缓存：真实 57 首为 16967.376 秒、276559770 字节，源总时长与 cache 差远小于 1 秒；由 `musichub-radio:www-data` 管理。首次预热在旧电台运行期间完成，未触碰其 HLS。
- 浏览器：最多 5 次递增重连，手动暂停/取消不会重新自动播放；时间表每 60 秒刷新、10 秒请求超时，失败有退避；进度每秒刷新且不会重复初始化 timer。主题/音量存储异常保留基本操作；收藏读写、取消与清空失败均反馈，不能假装保存成功。
- 缓存更新：四个前端脚本使用内容版本 `d9bcdaaeaabd1314`，普通页面刷新即可请求新脚本，不依赖用户清空浏览器数据。
- 部署：默认 main；专用 mktemp 目录，只删除本次创建目录而不是用户设置的 TMP_DIR；安装工具也单独锁定哈希。
- 健康：有限重试、播放列表最近分片时间不超过 30 秒、同源获取最新安全相对分片地址，检查 TS packet 长度和同步字节；兼容 Python 3.10 对 FFmpeg `+0800` 时区的解析。
- 依赖：cryptography 50.0.2、python-dotenv 1.2.4、pip 26.2.1、setuptools 84.0.0；运行和开发锁按 Linux/Python 3.10 重生成，补齐 greenlet。新建干净环境，未携带旧 requirements 中未声明的 Requests/Beautiful Soup 等残留。
  版本与兼容约束核对 [cryptography PyPI](https://pypi.org/project/cryptography/)、[dotenv 发布记录](https://pypi.org/project/python-dotenv/1.2.4/)、[pip](https://pypi.org/project/pip/26.2.1/)、[setuptools](https://pypi.org/project/setuptools/84.0.0/)；24 个新运行/安装包经 OSV 当晚查询未命中公告，不代表系统零漏洞或完成渗透测试。

### 验证与发布中的恢复

- 本地隔离新环境、临时 SQLite、禁用 dotenv：114 Python tests passed（7.30 秒）；Node VM 前端 12 tests passed；Shell 语法、Python 编译与 diff 检查通过。
- 服务器 Python 3.10 隔离内存 SQLite：111 曲目、22 作品、124 曲序；8 个主要页面/健康地址全部 200。该隔离 catalog-sync 未接触生产数据。
- 合成 MP3 → Matroska 在本机 FFmpeg 9 与服务器 4.4.2 均连续超过三轮；服务器 12 秒采样 sequence 4→14→24→34、PDT 递增、进程持续运行。真实曲库正常输出再解码 8 秒音频无错误；未宣称完成真实 4.713 小时整轮聆听。
- 第一次发布的新健康检查未适配 FFmpeg 的 `+0800`，部署事务已恢复旧代码、旧 unit、原 venv 和版本记录；复查站点正常。添加真实格式回归并在服务器原生 Python 3.10 下先验证后，再次发布成功。没有留下失败版本作为当前版本。
- 上线健康检查全部 ok；health/backup timers active，定时健康 service Result=success；未登录正式站与 HLS 为预期 401，主站 `yoruming.cn` 200，Nginx/unit 检查通过（另两个无关系统 unit 的既有警告没有修改）。
- Chrome 正式域名：新脚本已载入，音频 readyState=4、error=null、currentTime 前进；Radio→About 保持同一 audio 对象，11.637→35.312 秒。时间表实际 fetch 出现在约 0、60、120、180 秒。
- 浏览器故障探针：临时指向同源不存在的 HLS 地址，界面进入“取消重连”；恢复原地址后没有再次点击播放，播放器自动恢复并持续推进（7.166→29.133 秒、readyState=4）。404/警告是本次有意的故障探针，不是验收前无错误的证明。
- 390 px Radio/About：innerWidth=scrollWidth=390，导航展开/关闭、深浅主题通过，实际截图布局检查通过。正常收藏新增→About 显示→取消成功；只移除本次测试条目，原收藏状态未清空。已关闭开发者工具/手机模拟，恢复原浅色主题、音量 0.45 和暂停状态；留下 Chrome 最右的正式 Radio 标签供用户验收。

### 备份、恢复点与未完成项

- 最新数据库备份：`musichub-mysql-20261002T113538006423Z.sql.gz`；服务器与 Mac 的 SHA-256 均为 `04b39b57d95f2bbe91047a933c696db1d5bf4ac6a79808f68188607bf4297261`，gzip 完整性通过。
- 异机副本：保存在维护者指定的本机私有备份目录，权限为 0600，准确路径仅保留在本机记录、不进入公开仓库；曾用现有 verify 脚本在 network=none、无生产卷的临时 MySQL 容器恢复成功，确认曲目表存在并清理测试容器。此检查不等于整机灾备验收。
- 完整代码快照：`/var/backups/music-hub/releases/predeploy-20261002T114849393067Z-ff9d974517dc1291c9e22abf83ef5243d6163c8b.tar.gz`；文件名继承当时旧标签，实际归档保存现场文件，不以旧标签证明源码。
- 原 venv：`/var/backups/music-hub/venvs/venv-maintenance-20261002T113255Z`；本次覆盖前代码、旧 Radio unit、旧发布记录与 manifest 另存 `/var/backups/music-hub/content-releases/maintenance-20261002T113255Z/`（0700）。回滚必须同时恢复代码、unit 与原 venv；不能只改版本标签，旧版通用 rollback 脚本也不替代本次 unit/venv 恢复。
- 用户确认：先保存到现有 Mac 目录，自动异机备份和通知另定，因此没有新增云存储、通知服务或定时任务。
- 尚未证明：57 首完整长轮次、跨浏览器/实体手机、压力与整机灾备；所有第三方影像没有重新逐条核验。About 的“已核对影像 111”目前来自 `sum(bool(song.link))`，不是人工核验状态，且 README 历史记录为 24；记录为待专项核对，不顺手改生产数据或冒充核验完成。
- Git：该维护发布当时已验证、已部署，尚未提交；2026-10-24 按用户授权分批保存实现与记录。提交、推送结果以 Git 历史和远端回读为准；本次未重新部署。
- 子代理：2 个，显式配置均 `gpt-6-luna` + `high`、fork none，前端/运维分工；未沿用此前一次 Sol 授权，未收到模型替换/降级报告。平台未提供独立运行元数据，实际模型无法独立验证。根任务发现并复核回归、执行服务器实验、发布回滚及浏览器验收；没有把代理口述当作最终上线证据。发布记录/交付 Skill 用于维护现有入口与证据边界，没有创建重复状态文档。
