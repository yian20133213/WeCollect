from loguru import logger
import sys
import os

def setup_logger():
    # 确保日志目录存在
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志输出
    logger.remove()  # 移除默认处理器
    
    # 添加控制台输出
    logger.add(sys.stderr, level="INFO")
    
    # 添加文件输出
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
        rotation="00:00",  # 每天轮换一次
        retention="30 days",  # 保留30天
        level="DEBUG",
        encoding="utf-8"
    )
