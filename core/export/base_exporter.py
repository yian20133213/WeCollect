from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from loguru import logger

from database.models import Article, Media
from config.settings import EXPORT

class BaseExporter(ABC):
    """导出器基类"""
    
    def __init__(self):
        self.export_dir = EXPORT['output_dir']
        self.template_dir = EXPORT['template_dir']
        self.export_dir.mkdir(parents=True, exist_ok=True)
        
    def get_export_path(self, article: Article, ext: str) -> Path:
        """获取导出文件路径"""
        # 使用日期和文章ID创建目录结构
        date_str = datetime.now().strftime("%Y%m%d")
        dir_path = self.export_dir / date_str
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        filename = f"{article.id}_{self._clean_filename(article.title)}.{ext}"
        return dir_path / filename
        
    def _clean_filename(self, filename: str) -> str:
        """清理文件名"""
        # 移除不允许的字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:100]  # 限制长度
        
    @abstractmethod
    def export(self, article: Article) -> Optional[Path]:
        """导出文章"""
        pass
        
    @abstractmethod
    def batch_export(self, articles: List[Article]) -> List[Path]:
        """批量导出文章"""
        pass 