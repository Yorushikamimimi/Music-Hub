# 运行与合规手册（Operations）

## 1. 线上运行基线
- 站点域名：`music.yoruming.cn`
- 反向代理：`Nginx`（反向代理，负责 HTTPS 与转发）
- 应用服务：`Gunicorn + Flask`
- 服务名：`yorushika-web`
- 应用目录：`/var/www/My_Homepage`

## 2. 为什么会出现“不安全”（证书有效但仍警告）
最常见根因不是证书本身，而是 `mixed content`（混合内容：HTTPS 页面里加载了 HTTP 资源）或入口路由冲突。

高概率原因：
1. `mixed content`：页面中某些资源被 `http://` 加载（图片、脚本、字体、接口）。
2. Nginx 多份 `server_name` 冲突：同一域名命中到旧站点或错误 upstream。
3. 证书命中错误（`SNI`）：域名正确但命中默认站点证书或历史配置。
4. 浏览器缓存/HSTS 历史状态未刷新。

## 3. 一次性排查命令（服务器）
```bash
# 1) 证书链和域名是否匹配
openssl s_client -connect music.yoruming.cn:443 -servername music.yoruming.cn < /dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates

# 2) Nginx 是否有重复 server_name
sudo nginx -T 2>/dev/null | grep -nE "server_name\s+music\.yoruming\.cn|listen\s+443|proxy_pass"

# 3) 线上首页是否含 http:// 资源
curl -s https://music.yoruming.cn | grep -oE "http://[^\" )]+"

# 4) 本机回环验证（绕过 DNS）
curl -I -H "Host: music.yoruming.cn" http://127.0.0.1
curl -Ik https://music.yoruming.cn
```

如果第 3 条有输出，就属于 `mixed content`，需要把对应资源改成 `https://` 或相对路径。

## 4. 统一更新方式（一键脚本）
脚本位置：`scripts/deploy_music_hub.sh`

能力说明：
1. 从 GitHub 拉取指定分支。
2. 通过 `rsync` 同步到 `/var/www/My_Homepage`。
3. 保留 `.env`、`venv/`、`static/uploads/`、`current_avatar.txt`。
4. 安装依赖、执行 `compile check`（编译检查）。
5. 重启 `yorushika-web` 并做健康检查。
6. 生成增量备份目录：`/var/backups/music-hub/<timestamp>`。

使用方法：
```bash
cd /var/www/My_Homepage
chmod +x scripts/deploy_music_hub.sh
./scripts/deploy_music_hub.sh
```

可选参数：
```bash
BRANCH=main \
DOMAIN=music.yoruming.cn \
SERVICE_NAME=yorushika-web \
REPO_URL=https://github.com/Yorushikamimimi/Music-Hub.git \
./scripts/deploy_music_hub.sh
```

## 5. 本轮已加安全响应头（应用层）
在 `app.py` 新增了安全响应头：
- `Content-Security-Policy`（内容安全策略）：包含 `upgrade-insecure-requests` 与 `block-all-mixed-content`。
- `Strict-Transport-Security`（HSTS，强制 HTTPS）。
- `X-Content-Type-Options`、`X-Frame-Options`、`Referrer-Policy`、`Permissions-Policy`。

## 6. 变更后验收清单
1. `https://music.yoruming.cn` 打开后浏览器地址栏不再提示“不安全”。
2. `curl -Ik https://music.yoruming.cn` 返回 `HTTP/2 200`。
3. `sudo systemctl status yorushika-web` 为 `active (running)`。
4. `/`、`/search`、`/about` 页面可正常打开。
