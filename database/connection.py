from contextlib import contextmanager
import threading
from typing import Generator
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from config.settings import DATABASE

class DatabaseConnection:
    """数据库连接管理类"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'engine'):
            self.engine = create_engine(
                f"sqlite:///{DATABASE['path']}",
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600,
                echo=False
            )
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """获取数据库会话"""
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            logger.error(f"数据库会话异常: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_all_tables(self):
        """创建所有数据表"""
        from .models import Base
        Base.metadata.create_all(self.engine)
        
    def drop_all_tables(self):
        """删除所有数据表"""
        from .models import Base
        Base.metadata.drop_all(self.engine)

# 全局数据库连接实例
db = DatabaseConnection() 