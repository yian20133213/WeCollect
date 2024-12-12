from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import asyncio
from loguru import logger

from database.models import Article
from .html_exporter import HTMLExporter
from .pdf_exporter import PDFExporter
from .markdown_exporter import MarkdownExporter

class ExportManager:
    """导出管理器"""
    
    def __init__(self):
        self.exporters = {
            'html': HTMLExporter(),
            'pdf': PDFExporter(),
            'markdown': MarkdownExporter()
        }
        self.max_workers = 4
        
    async def export_article(
        self,
        article: Article,
        formats: List[str] = None
    ) -> Dict[str, Path]:
        """导出单篇文章"""
        if formats is None:
            formats = ['html', 'pdf', 'markdown']
            
        results = {}
        for fmt in formats:
            if fmt not in self.exporters:
                logger.warning(f"不支持的导出格式: {fmt}")
                continue
                
            try:
                path = self.exporters[fmt].export(article)
                if path:
                    results[fmt] = path
            except Exception as e:
                logger.error(f"导出失败[{fmt}]: {str(e)}")
                
        return results
        
    async def batch_export(
        self,
        articles: List[Article],
        formats: List[str] = None
    ) -> Dict[str, List[Path]]:
        """批量导出文章"""
        if formats is None:
            formats = ['html', 'pdf', 'markdown']
            
        results = {fmt: [] for fmt in formats}
        
        # 使用线程池处理导出任务
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 创建导出任务
            tasks = []
            for article in articles:
                task = self.export_article(article, formats)
                tasks.append(task)
                
            # 等待所有任务完成
            export_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 整理结果
            for result in export_results:
                if isinstance(result, Exception):
                    logger.error(f"导出任务失败: {str(result)}")
                    continue
                    
                for fmt, path in result.items():
                    results[fmt].append(path)
                    
        return results 