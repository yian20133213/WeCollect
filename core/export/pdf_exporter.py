from typing import List, Optional
from pathlib import Path
import pdfkit
from loguru import logger

from .base_exporter import BaseExporter
from .html_exporter import HTMLExporter
from database.models import Article

class PDFExporter(BaseExporter):
    """PDF导出器"""
    
    def __init__(self):
        super().__init__()
        self.html_exporter = HTMLExporter()
        self.pdf_options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None
        }
        
    def export(self, article: Article) -> Optional[Path]:
        """导出单篇文章为PDF"""
        try:
            # 先导出为HTML
            html_path = self.html_exporter.export(article)
            if not html_path:
                raise Exception("HTML导出失败")
                
            # 转换为PDF
            output_path = self.get_export_path(article, 'pdf')
            pdfkit.from_file(
                str(html_path),
                str(output_path),
                options=self.pdf_options
            )
            
            logger.info(f"PDF导出成功: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"PDF导出失败: {str(e)}")
            return None
            
    def batch_export(self, articles: List[Article]) -> List[Path]:
        """批量导出PDF"""
        results = []
        for article in articles:
            try:
                path = self.export(article)
                if path:
                    results.append(path)
            except Exception as e:
                logger.error(f"文章{article.id}导出失败: {str(e)}")
        return results 