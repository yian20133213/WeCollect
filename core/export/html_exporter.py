from typing import List, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from .base_exporter import BaseExporter
from database.models import Article

class HTMLExporter(BaseExporter):
    """HTML导出器"""
    
    def __init__(self):
        super().__init__()
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        self.template = self.env.get_template('article.html')
        
    def export(self, article: Article) -> Optional[Path]:
        """导出单篇文章为HTML"""
        try:
            # 准备模板数据
            template_data = {
                "title": article.title,
                "author": article.author,
                "publish_time": article.publish_time,
                "content": article.content,
                "media_items": article.media_items
            }
            
            # 渲染HTML
            html_content = self.template.render(**template_data)
            
            # 保存文件
            output_path = self.get_export_path(article, 'html')
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"HTML导出成功: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"HTML导出失败: {str(e)}")
            return None
            
    def batch_export(self, articles: List[Article]) -> List[Path]:
        """批量导出HTML"""
        results = []
        for article in articles:
            try:
                path = self.export(article)
                if path:
                    results.append(path)
            except Exception as e:
                logger.error(f"文章{article.id}导出失败: {str(e)}")
        return results 