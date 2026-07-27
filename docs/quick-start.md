# 快速开始（Quick Start）

## 1. 环境要求
- Python 3.10+
- MySQL 8+

## 2. 安装依赖
```bash
python -m venv .venv
. .venv/bin/activate
pip install --require-hashes -r requirements.txt
```

## 3. 配置环境变量
编辑根目录 `.env`，至少包含：

```env
SECRET_KEY=<长度不少于16的随机字符串>
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=<你的数据库密码>
DB_NAME=python_study
RADIO_STATION_NAME=Yorushika Radio
RADIO_STREAM_URL=/hls/yorushika.m3u8
```

说明：
- `SECRET_KEY` 有强度校验，弱值会直接报错退出。
- `DB_*` 为必填，缺失任一项会启动失败（Fail Fast，快速失败）。
  - 中文解释：配置不完整时立即报错，避免带着隐患运行。

## 4. 升级数据库并同步作品目录

```bash
flask --app wsgi:app db upgrade
flask --app wsgi:app catalog-sync
```

目录同步是可重复执行的 upsert，不删除未知记录，也不再抓取第三方排行榜。
首轮迁移会保留旧 `album` / `rating` 列作为回滚余地，但运行时不再使用它们。

## 5. 启动应用

```bash
flask --app wsgi:app run --host 127.0.0.1 --port 5000
```

默认访问：[http://127.0.0.1:5000](http://127.0.0.1:5000)。

## 6. 测试

```bash
pip install --require-hashes -r requirements-dev.txt
python -m pytest -q
```

## 7. 常见问题
- 启动时报 `Missing required environment variable`：补全 `.env`。
- 启动时报 `SECRET_KEY is too weak`：换成高强度随机值。
- Radio 页面无声：确认 `RADIO_STREAM_URL` 已设置，并检查 HLS 服务与白名单。
- 不要将 `.env`、数据库密码或本地音频提交到 Git。
