import os

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 爬虫相关配置
CRAWLER = {
    'concurrent_tasks': 3,  # 并发任务数
    'timeout': 30,         # 请求超时时间（秒）
    'retry_times': 3,      # 重试次数
    'retry_interval': 5,   # 重试间隔（秒）
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    # 文件保存相关
    'download_path': os.path.join(ROOT_DIR, 'downloads'),  # 下载文件保存路径
    'media_path': os.path.join(ROOT_DIR, 'downloads', 'media'),  # 媒体文件保存路径
    
    # 浏览器配置
    'browser': {
        'headless': True,  # 是否使用无头模式
        'proxy': None,     # 代理设置
        'window_size': (1920, 1080),  # 窗口大小
    },
    
    # 延迟设置
    'delay': {
        'min': 1,  # 最小延迟（秒）
        'max': 3,  # 最大延迟（秒）
    }
}

# 确保下载目录存在
os.makedirs(CRAWLER['download_path'], exist_ok=True)
os.makedirs(CRAWLER['media_path'], exist_ok=True)

# 导出相关配置（之前已有的）
EXPORT = {
    'output_dir': os.path.join(ROOT_DIR, 'exports'),
    'template_dir': os.path.join(ROOT_DIR, 'core', 'export', 'templates'),
    'encoding': 'utf-8',
}

# 确保导出目录存在
os.makedirs(EXPORT['output_dir'], exist_ok=True) 