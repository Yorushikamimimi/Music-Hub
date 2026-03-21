import os
import logging
import config

logger = logging.getLogger(__name__)

# 允许的文件扩展名（小写）
def allowed_file(filename: str) -> bool:
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )

def get_current_avatar() -> str:
    """读取当前头像文件名；读取失败时返回默认网络头像。"""
    try:
        if os.path.exists(config.AVATAR_PERSISTENCE_FILE):
            with open(config.AVATAR_PERSISTENCE_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return content
    except OSError as e:
        logger.warning("读取头像持久化文件失败：%s", e)
    # 默认头像（网络 SVG）
    return "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"

def save_current_avatar(filename: str) -> bool:
    """持久化头像文件名；写入失败时记录日志并返回 False。"""
    try:
        with open(config.AVATAR_PERSISTENCE_FILE, 'w', encoding='utf-8') as f:
            f.write(filename)
        return True
    except OSError as e:
        logger.error("保存头像持久化文件失败：%s", e)
        return False
