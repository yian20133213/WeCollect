import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from loguru import logger

class ContentCleaner:
    """内容清洗器"""
    
    @staticmethod
    def clean_html(html: str) -> str:
        """清理HTML内容"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 移除注释
            for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
                comment.extract()
            
            # 移除script标签
            for script in soup.find_all('script'):
                script.decompose()
                
            # 移除style标签
            for style in soup.find_all('style'):
                style.decompose()
                
            # 清理标签属性
            for tag in soup.find_all(True):
                # 保留的属性列表
                keep_attrs = ['src', 'href', 'title', 'alt']
                attrs = dict(tag.attrs)
                for attr in attrs:
                    if attr not in keep_attrs:
                        del tag[attr]
                        
            return str(soup)
            
        except Exception as e:
            logger.error(f"清理HTML失败: {str(e)}")
            return html
            
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本内容"""
        try:
            # 移除HTML标签
            text = re.sub(r'<[^>]+>', '', text)
            
            # 移除多余空白字符
            text = " ".join(text.split())
            
            # 移除特殊字符
            text = text.replace('\u200b', '').replace('\xa0', ' ')
            
            # 移除表情符号
            text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF]', '', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"清理文本失败: {str(e)}")
            return text
            
    @staticmethod
    def normalize_url(url: str) -> str:
        """规范化URL"""
        try:
            # 移除URL中的跟踪参数
            url = re.sub(r'[?&]from=.*?(?=&|$)', '', url)
            url = re.sub(r'[?&]scene=.*?(?=&|$)', '', url)
            url = re.sub(r'[?&]timestamp=.*?(?=&|$)', '', url)
            
            # 确保使用HTTPS
            if url.startswith('http:'):
                url = 'https:' + url[5:]
                
            return url
            
        except Exception as e:
            logger.error(f"规范化URL失败: {str(e)}")
            return url 