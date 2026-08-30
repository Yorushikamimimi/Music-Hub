# 项目进度（中文索引）

本文件保留为根目录入口，详细进度请查看：

- [docs/progress.md](./docs/progress.md)

## 当前结论（2026-08-30）
- `main` 已承接原硬化分支和原上线分支的完整有效历史，并作为唯一公开长期分支；
  默认部署脚本也改为读取 `main`。
- 当前仓库保存 22 部发行作品、111 首独立曲目、124 个曲序位置，以及四场
  Live 共 57 个 Radio 分曲的顺序、显示名和运行配置；音频字节仍不进入 Git。
- `radio.yoruming.cn` 的独立 HTTPS、完整 origin Basic Auth、Trusted Host、
  Nginx 模板和证书续签 hook 已版本化；公开模板不保存密码哈希或真实个人出口 IP。
- 收口前验证为 `98 passed`，Python 编译与 Flask import、Bash / POSIX shell
  语法及 Git diff 检查均通过。本机无可用 Nginx 运行时，因此未重复执行 `nginx -t`。
- 本次仅整理 GitHub 代码与运维配置，没有部署、重启、修改 DNS、防火墙或服务器；
  线上精确版本继续以服务器 `deployed-version.json` 为准。
