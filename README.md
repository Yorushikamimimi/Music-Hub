# Music Hub

一个仅供本人访问的 `Yorushika` 主题音乐站点，提供作品索引、Song Stories、
搜索筛选、本地收藏和白名单 Radio。

## 项目定位
- `Web App`：面向个人展示与轻量互动的 Flask 网站。
  - 中文解释：`Web App` 指通过浏览器访问并完成主要交互的应用。
- `MVP`：当前为可运行的最小可交付版本。
  - 中文解释：`MVP` 指保留核心能力、可被真实使用的最小版本。

## 当前状态（2026-07-28）
- 目录：20 首人工校对曲目，包含真实专辑、发行类型、年份、原创简介和官方来源。
- 页面：首页、搜索、Song Stories、Radio、About 与浏览器本地收藏。
- Radio：24 首白名单曲目，手动播放、当前曲目、近似进度、下一首和 25% 初始音量。
- 私密边界：禁止搜索引擎收录，Radio 不提供下载入口，只面向 Nginx 白名单。
- 工程：图片和字体已减重；数据库使用可回滚迁移；依赖带哈希锁定；具备集成测试。
- 运维目标：Web 与 Radio 使用独立非 root 用户，Unix socket 放在 `/run`。

> 本轮代码与配置已完成离线验证，但非 root 服务配置和数据库网络收口在服务器上
> 仍需一次受控部署；不要把仓库中的目标配置误当成线上已生效事实。

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

音频文件不进入 Git。电台服务从 `/srv/media/yorushika-radio/music` 读取人工
白名单内的 MP3，并在 `/run/yorushika-radio/` 生成临时 HLS 分片与曲目元数据。

## 文档导航
- 项目总览：[docs/overview.md](./docs/overview.md)
- 快速开始：[docs/quick-start.md](./docs/quick-start.md)
- 进度跟踪：[docs/progress.md](./docs/progress.md)
- 路线图：[docs/roadmap.md](./docs/roadmap.md)
- 运行与合规手册：[docs/operations.md](./docs/operations.md)
