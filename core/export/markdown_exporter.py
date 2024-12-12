from typing import List, Optional
from pathlib import Path
import html2text
from loguru import logger

from .base_exporter import BaseExporter
from database.models import Article

class MarkdownExporter(BaseExporter):
    """Markdown导出器"""
    
    def __init__(self):
        super().__init__()
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0  # 不限制行宽
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        
    def export(self, article: Article) -> Optional[Path]:
        """导出单篇文章为Markdown"""
        try:
            # 转换文章内容为Markdown
            md_content = self._convert_to_markdown(article)
            
            # 保存文件
            output_path = self.get_export_path(article, 'md')
            output_path.write_text(md_content, encoding='utf-8')
            
            logger.info(f"Markdown导出成功: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Markdown导出失败: {str(e)}")
            return None
            
    def _convert_to_markdown(self, article: Article) -> str:
        """转换文章为Markdown格式"""
        # 添加文章元数据
        md_content = f"""# {article.title}

> 作者: {article.author}  
> 发布时间: {article.publish_time.strftime('%Y-%m-%d %H:%M')}

---

"""
        # 转换正文内容
        md_content += self.h2t.handle(article.content)
        
        # 添加媒体资源引用
        if article.media_items:
            md_content += "\n\n## 媒体资源\n\n"
            for media in article.media_items:
                if media.type == "image":
                    md_content += f"![{media.description}]({media.url})\n\n"
                elif media.type == "video":
                    md_content += f"[视频链接]({media.url})\n\n"
                    
        return md_content
        
    def batch_export(self, articles: List[Article]) -> List[Path]:
        """批量导出Markdown"""
        results = []
        for article in articles:
            try:
                path = self.export(article)
                if path:
                    results.append(path)
            except Exception as e:
                logger.error(f"文章{article.id}导出失败: {str(e)}")
        return results 