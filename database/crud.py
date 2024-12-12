from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .models import Account, PublicAccount, Article, Media

class CRUDBase:
    """基础CRUD操作类"""
    
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: dict):
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int):
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

class ArticleCRUD(CRUDBase):
    """文章相关的CRUD操作"""
    
    def __init__(self):
        super().__init__(Article)

    def get_by_url(self, db: Session, url: str) -> Optional[Article]:
        return db.query(Article).filter(Article.url == url).first()

    def get_pending_articles(self, db: Session, limit: int = 10) -> List[Article]:
        return db.query(Article).filter(
            Article.status == 0
        ).limit(limit).all()

    def get_articles_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
        public_account_id: Optional[int] = None
    ) -> List[Article]:
        query = db.query(Article).filter(
            and_(
                Article.publish_time >= start_date,
                Article.publish_time <= end_date
            )
        )
        
        if public_account_id:
            query = query.filter(Article.public_account_id == public_account_id)
            
        return query.all()

# 创建CRUD操作实例
article_crud = ArticleCRUD()
account_crud = CRUDBase(Account)
public_account_crud = CRUDBase(PublicAccount)
media_crud = CRUDBase(Media) 
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .models import Account, PublicAccount, Article, Media

class CRUDBase:
    """基础CRUD操作类"""
    
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: dict):
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int):
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

class ArticleCRUD(CRUDBase):
    """文章相关的CRUD操作"""
    
    def __init__(self):
        super().__init__(Article)

    def get_by_url(self, db: Session, url: str) -> Optional[Article]:
        return db.query(Article).filter(Article.url == url).first()

    def get_pending_articles(self, db: Session, limit: int = 10) -> List[Article]:
        return db.query(Article).filter(
            Article.status == 0
        ).limit(limit).all()

    def get_articles_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
        public_account_id: Optional[int] = None
    ) -> List[Article]:
        query = db.query(Article).filter(
            and_(
                Article.publish_time >= start_date,
                Article.publish_time <= end_date
            )
        )
        
        if public_account_id:
            query = query.filter(Article.public_account_id == public_account_id)
            
        return query.all()

# 创建CRUD操作实例
article_crud = ArticleCRUD()
account_crud = CRUDBase(Account)
public_account_crud = CRUDBase(PublicAccount)
media_crud = CRUDBase(Media) 