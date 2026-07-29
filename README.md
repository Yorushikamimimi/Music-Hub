# Music Hub

一个仅供本人访问的 `Yorushika` 主题音乐站点，提供作品索引、Song Stories、
搜索筛选、本地收藏和白名单 Radio。

## 项目定位
- `Web App`：面向个人展示与轻量互动的 Flask 网站。
  - 中文解释：`Web App` 指通过浏览器访问并完成主要交互的应用。
- `MVP`：当前为可运行的最小可交付版本。
  - 中文解释：`MVP` 指保留核心能力、可被真实使用的最小版本。

## 当前状态（2026-07-29）
- 目录：以 Yorushika 官方艺人目录中的音乐发行为范围，整理 22 部作品、109 首独立曲目与 122 个曲序位置，保留发行日期、类型、封面、官方来源和复核日期。
- 页面：首页、作品集、单曲详情、搜索、Song Stories、Radio、策展说明与浏览器本地收藏。
- 作品页：8 部作品保留完整策展档案，其余 14 部提供不虚构背景的来源型发行概览。
- 影像：24 首已有人工核对的 Bilibili 影像入口；只确认页面可达且标题与曲目相符，不代表官方授权或长期可用。其余曲目只展示官方作品来源。
- Radio：24 首白名单曲目，手动播放、当前曲目、近似进度、下一首和 25% 初始音量。
- 私密边界：禁止搜索引擎收录，Radio 不提供下载入口，只面向 Nginx 白名单。
- 工程：图片和字体已减重；数据库使用可回滚迁移；依赖带哈希锁定；具备集成测试。
- 数据：曲目与发行作品已拆分，多作品收录的同一首歌只保留一份曲目资料，并按作品分别保存曲序。
- 运维：Web 与 Radio 使用独立非 root 用户，Unix socket 放在 `/run`。
- 可靠性：5 分钟健康检查、每日 MySQL 备份、失败记录、完整发布快照和显式回滚已上线。
- 视觉：采用“夜鹿集 / YORUSHIKA ARCHIVE”内容型设计，中文说明为主、日文标题为作品标识。

> 2026-07-28 已完成真实备份与隔离恢复演练，并启用健康检查和备份 timer。
> 当前备份仍与服务器同盘；它能处理误操作和发布回退，不能替代异地灾备。
>
> 2026-07-29 已按官方艺人目录重新核对当前 22 部音乐发行，并确认 24 个
> Bilibili 链接可达且标题与曲目相符。当前目录不含 Live 影像制品、书简型小说及
> suis / n-buna 个人作品。

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
BRANCH=codex/yorushika-redesign-prototype \
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
- `deploy/systemd/music-hub-health.{service,timer}`
- `deploy/systemd/music-hub-backup.{service,timer}`
- `deploy/systemd/music-hub-failure@.service`
- `deploy/nginx/musichub-ip.conf`

音频文件不进入 Git。电台服务从 `/srv/media/yorushika-radio/music` 读取人工
白名单内的 MP3，并在 `/run/yorushika-radio/` 生成临时 HLS 分片与曲目元数据。

## 文档导航
- 项目总览：[docs/overview.md](./docs/overview.md)
- 快速开始：[docs/quick-start.md](./docs/quick-start.md)
- 进度跟踪：[docs/progress.md](./docs/progress.md)
- 路线图：[docs/roadmap.md](./docs/roadmap.md)
- 运行与合规手册：[docs/operations.md](./docs/operations.md)
