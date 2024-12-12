import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from database.models import Base
from database.connection import DATABASE_URL
from loguru import logger

def init_database():
    """初始化数据库"""
    try:
        # 创建数据库引擎
        engine = create_engine(DATABASE_URL)
        
        # 创建所有表
        Base.metadata.create_all(engine)
        
        logger.info("数据库初始化成功")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    init_database() 