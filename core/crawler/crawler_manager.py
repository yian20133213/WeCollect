import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from typing import List
from datetime import datetime
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

from database.models import Article, Base
from database.connection import db
from database.crud_article import article_crud
from core.browser.browser_manager import BrowserManager
from core.crawler.article_crawler import ArticleCrawler
from core.config import CRAWLER

class CrawlerManager:
    """采集管理器"""
    
    def __init__(self):
        self.max_workers = CRAWLER.get('concurrent_tasks', 3)
        self.semaphore = asyncio.Semaphore(self.max_workers)
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.browser_manager = BrowserManager()
        
    async def start_crawl(self, public_account_id: int):
        """开始采集任务"""
        try:
            # 创建浏览器实例
            await self.browser_manager.init_browser()
            
            crawler = ArticleCrawler(self.browser_manager)
            
            try:
                # 获取待采集的文章
                with db.get_session() as session:
                    articles = article_crud.get_pending_articles(
                        session,
                        limit=100
                    )
                
                # 创建采集任务
                tasks = []
                for article in articles:
                    task = self.crawl_article(crawler, article)
                    tasks.append(task)
                
                # 并发执行采集任务
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 处理结果
                success_count = sum(1 for r in results if r and not isinstance(r, Exception))
                logger.info(f"采集完成: 总数={len(results)}, 成功={success_count}")
                
            finally:
                await self.browser_manager.close()
                
        except Exception as e:
            logger.error(f"采集任务执行失败: {str(e)}")
            raise
            
    async def crawl_article(self, crawler: ArticleCrawler, article: Article):
        """采集单篇文章"""
        async with self.semaphore:  # 控制并发数
            try:
                # 更新文章状态为采集中
                with db.get_session() as session:
                    article_crud.update_status(session, article.id, status=1)
                
                # 采集文章内容
                content = await crawler.get_article_content(article)
                
                # 更新文章信息
                with db.get_session() as session:
                    article_crud.update(session, id=article.id, data={
                        "content": content["content"],
                        "html": content["html"],
                        "publish_time": content["publish_time"],
                        "author": content["author"],
                        "status": 2,  # 采集完成
                        "updated_at": datetime.now()
                    })
                
                # 下载图片（异步）
                if content["images"]:
                    asyncio.create_task(
                        self.download_images(article.id, content["images"])
                    )
                
                return True
                
            except Exception as e:
                logger.error(f"文章采集失败: article_id={article.id}, error={str(e)}")
                # 更新文章状态为采集失败
                with db.get_session() as session:
                    article_crud.update_status(
                        session,
                        article.id,
                        status=3,
                        error_msg=str(e)
                    )
                return False