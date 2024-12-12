from typing import List, Dict, Any
from loguru import logger
from sqlalchemy import inspect, text

from .connection import db

class TableManager:
    """数据表管理类"""
    
    @staticmethod
    def get_table_info() -> List[Dict[str, Any]]:
        """获取所有数据表信息"""
        inspector = inspect(db.engine)
        tables = []
        
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    'name': column['name'],
                    'type': str(column['type']),
                    'nullable': column['nullable']
                })
            
            tables.append({
                'name': table_name,
                'columns': columns
            })
        
        return tables
    
    @staticmethod
    def vacuum_database():
        """压缩数据库"""
        try:
            with db.get_session() as session:
                session.execute(text('VACUUM'))
                logger.info("数据库压缩完成")
        except Exception as e:
            logger.error(f"数据库压缩失败: {str(e)}")
            raise
    
    @staticmethod
    def check_table_exists(table_name: str) -> bool:
        """检查表是否存在"""
        inspector = inspect(db.engine)
        return table_name in inspector.get_table_names() 