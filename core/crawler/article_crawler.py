import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from core.browser.browser_manager import BrowserManager
from database.models import Article, PublicAccount
from utils.retry import retry_async
from config.settings import CRAWLER

class ArticleCrawler:
    """文章采集器"""
    
    def __init__(self, browser_manager: BrowserManager):
        self.browser = browser_manager
        self.base_url = "https://mp.weixin.qq.com"
        
    @retry_async(max_retries=3, delay=2)
    async def get_article_list(
        self,
        public_account: PublicAccount,
        offset: int = 0,
        limit: int = 10
    ) -> List[Dict]:
        """获取文章列表"""
        try:
            # 构建文章列表页URL
            url = f"{self.base_url}/cgi-bin/appmsg"
            params = {
                "begin": offset,
                "count": limit,
                "fakeid": public_account.biz,
                "type": "9",
            }
            
            # 访问文章列表页
            await self.browser.driver.get(url)
            await asyncio.sleep(2)  # 等待页面加载
            
            # 提取文章信息
            articles = []
            elements = await self.browser.driver.find_elements(
                By.CSS_SELECTOR,
                ".weui-desktop-mass-appmsg__title"
            )
            
            for elem in elements:
                article = {
                    "title": elem.text.strip(),
                    "url": elem.get_attribute("href"),
                    "public_account_id": public_account.id,
                }
                articles.append(article)
                
            return articles
            
        except Exception as e:
            logger.error(f"获取文章列表失败: {str(e)}")
            raise
            
    @retry_async(max_retries=3, delay=2)
    async def get_article_content(self, article: Article) -> Optional[Dict]:
        """获取文章内容"""
        try:
            await self.browser.driver.get(article.url)
            await asyncio.sleep(2)  # 等待页面加载
            
            # 等待文章内容加载完成
            content_selector = "#js_content"
            content_elem = await self.browser.wait_for_element(content_selector)
            
            # 获取页面HTML
            html = await self.browser.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # 提取文章信息
            content = soup.select_one(content_selector)
            publish_time = soup.select_one("#publish_time").text.strip()
            author = soup.select_one("#js_name").text.strip()
            
            # 处理图片
            images = []
            for img in content.select("img"):
                if img.get("data-src"):
                    images.append({
                        "url": img["data-src"],
                        "type": "image"
                    })
                    
            return {
                "content": content.get_text(),
                "html": str(content),
                "publish_time": datetime.strptime(publish_time, "%Y-%m-%d %H:%M"),
                "author": author,
                "images": images
            }
            
        except Exception as e:
            logger.error(f"获取文章内容失败: {str(e)}")
            raise 