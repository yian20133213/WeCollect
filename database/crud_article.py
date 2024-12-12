from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .crud_base import CRUDBase
from .models import Article

class CRUDArticle(CRUDBase[Article]):
    """文章CRUD操作类"""
    
    def get_by_url(self, session: Session, url: str) -> Optional[Article]:
        """通过URL获取文章"""
        return session.query(Article).filter(Article.url == url).first()
    
    def get_pending_articles(
        self,
        session: Session,
        limit: int = 10
    ) -> List[Article]:
        """获取待采集的文章"""
        return session.query(Article).filter(
            Article.status == 0
        ).limit(limit).all()
    
    def get_by_date_range(
        self,
        session: Session,
        start_date: datetime,
        end_date: datetime,
        public_account_id: Optional[int] = None
    ) -> List[Article]:
        """获取指定日期范围的文章"""
        query = session.query(Article).filter(
            and_(
                Article.publish_time >= start_date,
                Article.publish_time <= end_date
            )
        )
        
        if public_account_id:
            query = query.filter(Article.public_account_id == public_account_id)
        
        return query.all()
    
    def update_status(
        self,
        session: Session,
        article_id: int,
        status: int,
        error_msg: str = None
    ) -> Optional[Article]:
        """更新文章状态"""
        return self.update(session, id=article_id, data={
            "status": status,
            "error_msg": error_msg,
            "updated_at": datetime.now()
        })

# 创建文章CRUD实例
article_crud = CRUDArticle(Article) 