# 快速开始（Quick Start）

## 1. 环境要求
- Python 3.11+
- MySQL 8+
- Windows PowerShell（当前项目环境）

## 2. 安装依赖
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. 配置环境变量
编辑根目录 `.env`，至少包含：

```env
SECRET_KEY=<长度不少于16的随机字符串>
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=<你的数据库密码>
DB_NAME=python_study
```

说明：
- `SECRET_KEY` 有强度校验，弱值会直接报错退出。
- `DB_*` 为必填，缺失任一项会启动失败（Fail Fast，快速失败）。
  - 中文解释：配置不完整时立即报错，避免带着隐患运行。

## 4. 启动应用
```powershell
python app.py
```

默认访问：
- [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 5. 数据准备
### 方案A：直接使用现有库数据
保证 `DB_NAME` 中已有 `music_yorushika` 表和数据。

### 方案B：使用爬虫脚本重建数据（谨慎）
```powershell
python netease_spider.py
```
注意：该脚本包含 `DROP TABLE` 逻辑，会重建相关表。

## 6. 常见问题
- 启动时报 `Missing required environment variable`：补全 `.env`。
- 启动时报 `SECRET_KEY is too weak`：换成高强度随机值。
- 页面中文乱码：当前为历史遗留，建议后续统一修复模板文案编码。
