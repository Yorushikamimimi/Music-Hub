# Music Hub

一个以 `Yorushika` 主题为核心的音乐站点，提供歌曲展示、搜索筛选与本地收藏（心愿单）能力。

## 项目定位
- `Web App`：面向个人展示与轻量互动的 Flask 网站。
  - 中文解释：`Web App` 指通过浏览器访问并完成主要交互的应用。
- `MVP`：当前为可运行的最小可交付版本。
  - 中文解释：`MVP` 指保留核心能力、可被真实使用的最小版本。

## 当前状态（2026-07-28）
- 已完成：评论功能下线、头像悬停音乐下线、头像上传入口关闭、配置凭据加固。
- 可用功能：首页歌曲列表、每日推荐、搜索筛选、收藏/心愿单。
- Radio：提供手动播放的 HLS 电台、当前曲目、近似进度、下一首和 25% 初始音量。
- 运行方式：`musichub.service` 与 `yorushika-radio.service` 均由 systemd 管理并支持开机恢复。
- 当前入口：服务器 IP 的 HTTP 页面，仅允许 localhost 与维护者当前公网 IP 访问。

## 快速开始
详见 [docs/quick-start.md](./docs/quick-start.md)。

## 服务器更新
在服务器执行：

```bash
cd /var/www/My_Homepage
chmod +x scripts/deploy_music_hub.sh
./scripts/deploy_music_hub.sh
```

常用参数覆盖（按需）：

```bash
BRANCH=main \
HOST_HEADER=81.68.72.245 \
SERVICE_NAME=musichub.service \
RADIO_SERVICE_NAME=yorushika-radio.service \
./scripts/deploy_music_hub.sh
```

说明：
- `BRANCH`：要部署的 Git 分支。
- `HOST_HEADER`：本机 Nginx 健康检查使用的 Host。
- `SERVICE_NAME`：systemd 服务名。
- `RADIO_SERVICE_NAME`：HLS 电台 systemd 服务名。

部署配置位于：

- `deploy/systemd/musichub.service`
- `deploy/systemd/yorushika-radio.service`
- `deploy/nginx/musichub-ip.conf`

音频文件不进入 Git。电台服务默认从服务器已有目录读取 MP3，并在 `/run/yorushika-radio/` 生成临时 HLS 分片与曲目元数据。

## 文档导航
- 项目总览：[docs/overview.md](./docs/overview.md)
- 快速开始：[docs/quick-start.md](./docs/quick-start.md)
- 进度跟踪：[docs/progress.md](./docs/progress.md)
- 路线图：[docs/roadmap.md](./docs/roadmap.md)
- 运行与合规手册：[docs/operations.md](./docs/operations.md)
