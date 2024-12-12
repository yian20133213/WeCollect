from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from loguru import logger

from .models import Base

ModelType = TypeVar("ModelType", bound=Base)

class CRUDBase(Generic[ModelType]):
    """基础CRUD操作类"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def create(self, session: Session, *, data: Dict[str, Any]) -> ModelType:
        """创建记录"""
        try:
            db_obj = self.model(**data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(f"创建记录失败: {str(e)}")
            raise
    
    def batch_create(self, session: Session, *, data_list: List[Dict[str, Any]]) -> List[ModelType]:
        """批量创建记录"""
        try:
            db_objs = [self.model(**data) for data in data_list]
            session.bulk_save_objects(db_objs)
            session.commit()
            return db_objs
        except Exception as e:
            logger.error(f"批量创建记录失败: {str(e)}")
            raise
    
    def get(self, session: Session, id: Any) -> Optional[ModelType]:
        """获取单条记录"""
        return session.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self,
        session: Session,
        *,
        filters: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: str = None
    ) -> List[ModelType]:
        """获取多条记录"""
        query = session.query(self.model)
        
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):
                    filter_conditions.append(getattr(self.model, key) == value)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))
        
        if order_by:
            if order_by.startswith('-'):
                query = query.order_by(desc(getattr(self.model, order_by[1:])))
            else:
                query = query.order_by(getattr(self.model, order_by))
        
        return query.offset(skip).limit(limit).all()
    
    def update(
        self,
        session: Session,
        *,
        id: Any,
        data: Dict[str, Any]
    ) -> Optional[ModelType]:
        """更新记录"""
        try:
            db_obj = session.query(self.model).filter(self.model.id == id).first()
            if db_obj:
                for key, value in data.items():
                    setattr(db_obj, key, value)
                session.commit()
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(f"更新记录失败: {str(e)}")
            raise
    
    def delete(self, session: Session, *, id: Any) -> bool:
        """删除记录"""
        try:
            db_obj = session.query(self.model).filter(self.model.id == id).first()
            if db_obj:
                session.delete(db_obj)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"删除记录失败: {str(e)}")
            raise 