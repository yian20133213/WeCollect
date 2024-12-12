from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Account(Base):
    """微信账号信息表"""
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    nickname = Column(String(100))  # 微信昵称
    cookie = Column(Text)           # 登录Cookie
    last_login = Column(DateTime)   # 最后登录时间
    status = Column(Integer, default=1)  # 账号状态：1-正常，0-禁用
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class PublicAccount(Base):
    """公众号信息表"""
    __tablename__ = 'public_accounts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))      # 公众号名称
    biz = Column(String(100))       # 公众号唯一标识
    description = Column(Text)      # 公众号描述
    status = Column(Integer, default=1)  # 状态：1-正常，0-禁用
    last_sync = Column(DateTime)    # 最后同步时间
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Article(Base):
    """文章信息表"""
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    public_account_id = Column(Integer, ForeignKey('public_accounts.id'))
    title = Column(String(500))     # 文章标题
    author = Column(String(100))    # 作者
    url = Column(Text)              # 原文链接
    content = Column(Text)          # 文章内容
    publish_time = Column(DateTime) # 发布时间
    status = Column(Integer, default=0)  # 状态：0-待采集，1-采集中，2-采集完成，3-采集失败
    local_path = Column(String(500))# 本地存储路径
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    public_account = relationship("PublicAccount", backref="articles")
    media_items = relationship("Media", backref="article")

class Media(Base):
    """媒体资源表"""
    __tablename__ = 'media'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    type = Column(String(20))       # 类型：image, video, audio
    url = Column(Text)              # 原始链接
    local_path = Column(String(500))# 本地存储路径
    status = Column(Integer, default=0)  # 状态：0-待下载，1-下载中，2-下载完成，3-下载失败
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
