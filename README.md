# My_Homepage

一个以 `Yorushika` 主题为核心的音乐站点，提供歌曲展示、搜索筛选与本地收藏（心愿单）能力。

## 项目定位
- `Web App`：面向个人展示与轻量互动的 Flask 网站。
  - 中文解释：`Web App` 指通过浏览器访问并完成主要交互的应用。
- `MVP`：当前为可运行的最小可交付版本。
  - 中文解释：`MVP` 指保留核心能力、可被真实使用的最小版本。

## 当前状态（2026-03-21）
- 已完成：评论功能下线、头像悬停音乐下线、头像上传入口关闭、配置凭据加固、项目清理。
- 可用功能：首页歌曲列表、每日推荐、搜索筛选、收藏/心愿单。
- 风险提示：模板中仍存在部分历史乱码文案，建议后续统一修正文案编码。

## 核心功能
1. 首页歌曲展示与每日推荐。
2. 搜索页按关键词/年份/排序筛选歌曲。
3. 心愿单（浏览器 `localStorage` 本地持久化）。
4. 关于页个人信息与技能展示（上传能力已关闭）。

## 技术栈
- `Flask`：Python Web 框架，负责路由和页面渲染。
- `Flask-SQLAlchemy`：ORM 层，负责数据库模型与查询。
- `MySQL`：关系型数据库，存储歌曲数据。
- `Bootstrap`：前端样式基础库。

## 快速开始
详见 [docs/quick-start.md](./docs/quick-start.md)。

## 文档导航
- 项目总览：[docs/overview.md](./docs/overview.md)
- 快速开始：[docs/quick-start.md](./docs/quick-start.md)
- 进度跟踪：[docs/progress.md](./docs/progress.md)
- 路线图：[docs/roadmap.md](./docs/roadmap.md)
- 运行与合规手册：[docs/operations.md](./docs/operations.md)

## 下一步
1. 完成数据库密码轮换并同步 `.env`。
2. 清理页面乱码文案并统一 UTF-8 文本。
3. 增补基础测试与上线前自检清单。
