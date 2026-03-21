# My_Homepage

一个以 `Yorushika` 主题为核心的音乐站点，提供歌曲展示、搜索筛选与本地收藏（心愿单）能力。

## 项目定位
- `Web App`：面向个人展示与轻量互动的 Flask 网站。
  - 中文解释：`Web App` 指通过浏览器访问并完成主要交互的应用。
- `MVP`：当前为可运行的最小可交付版本。
  - 中文解释：`MVP` 指保留核心能力、可被真实使用的最小版本。

## 当前状态（2026-03-21）
- 已完成：评论功能下线、头像悬停音乐下线、头像上传入口关闭、配置凭据加固。
- 新增：一键更新脚本 `scripts/deploy_music_hub.sh`（用于服务器统一部署）。
- 可用功能：首页歌曲列表、每日推荐、搜索筛选、收藏/心愿单。

## 快速开始
详见 [docs/quick-start.md](./docs/quick-start.md)。

## 服务器一键更新（推荐）
在服务器执行：

```bash
cd /var/www/My_Homepage
chmod +x scripts/deploy_music_hub.sh
./scripts/deploy_music_hub.sh
```

常用参数覆盖（按需）：

```bash
BRANCH=main DOMAIN=music.yoruming.cn SERVICE_NAME=yorushika-web ./scripts/deploy_music_hub.sh
```

说明：
- `BRANCH`：要部署的 Git 分支。
- `DOMAIN`：健康检查域名。
- `SERVICE_NAME`：systemd 服务名。

## 文档导航
- 项目总览：[docs/overview.md](./docs/overview.md)
- 快速开始：[docs/quick-start.md](./docs/quick-start.md)
- 进度跟踪：[docs/progress.md](./docs/progress.md)
- 路线图：[docs/roadmap.md](./docs/roadmap.md)
- 运行与合规手册：[docs/operations.md](./docs/operations.md)
