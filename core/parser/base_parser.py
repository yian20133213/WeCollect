from abc import ABC, abstractmethod
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from loguru import logger

class BaseParser(ABC):
    """解析器基类"""
    
    def __init__(self):
        self.soup = None
        
    def init_soup(self, html: str):
        """初始化BeautifulSoup"""
        self.soup = BeautifulSoup(html, 'html.parser')
        
    @abstractmethod
    def parse(self, html: str) -> Dict[str, Any]:
        """解析内容"""
        pass
        
    def clean_text(self, text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
        # 移除多余空白字符
        text = " ".join(text.split())
        # 移除特殊字符
        text = text.replace('\u200b', '').replace('\xa0', ' ')
        return text.strip() 