from contextlib import contextmanager
from typing import Generator
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from config.settings import DATABASE
from .models import Base, Article

logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.engine = create_engine(
            f"{DATABASE['type']}:///{DATABASE['path']}",
            echo=False,  # 设置为True可以显示SQL语句
            future=True
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )

    def init_database(self):
        """初始化数据库"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("数据库初始化成功")
        except SQLAlchemyError as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """取数据库会话"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败: {str(e)}")
            raise
        finally:
            session.close()

# 创建全局数据库管理器实例
db_manager = DatabaseManager()

def init_database():
    """初始化数据库的便捷函数"""
    db_manager.init_database()

def save_articles(account_name, articles):
    """保存文章到数据库"""
    try:
        with db_manager.get_session() as session:
            for article in articles:
                new_article = Article(
                    account_name=account_name,
                    title=article['title'],
                    link=article['link'],
                    publish_time=article['publish_time'],
                    content=article['content']
                )
                session.add(new_article)
    except Exception as e:
        logger.error(f"保存文章失败: {str(e)}")
        raise

def check_article_exists(url):
    """检查文章是否已存在"""
    try:
        with db_manager.get_session() as session:
            exists = session.query(Article).filter(Article.link == url).first() is not None
            return exists
    except Exception as e:
        logger.error(f"检查文章是否存在时出错: {str(e)}")
        return False
