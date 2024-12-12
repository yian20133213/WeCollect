import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 数据存储配置
DATA_DIR = BASE_DIR / "data"
ARTICLES_DIR = DATA_DIR / "articles"
IMAGES_DIR = DATA_DIR / "images"
VIDEOS_DIR = DATA_DIR / "videos"
EXPORTS_DIR = DATA_DIR / "exports"

# 数据库配置
DATABASE = {
    "type": "sqlite",
    "name": "wechat_articles.db",
    "path": DATA_DIR / "wechat_articles.db"
}

# 爬虫配置
CRAWLER = {
    "timeout": 30,
    "retry_times": 3,
    "retry_interval": 5,
    "concurrent_tasks": 3,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]
}

# 导出配置
EXPORT = {
    "formats": ["html", "pdf", "markdown"],
    "template_dir": BASE_DIR / "export" / "templates"
}

APP_NAME = "WeCollect"

# 创建必要的目录
for dir_path in [ARTICLES_DIR, IMAGES_DIR, VIDEOS_DIR, EXPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
