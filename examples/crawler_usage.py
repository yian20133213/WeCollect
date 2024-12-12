import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from loguru import logger
from core.crawler.crawler_manager import CrawlerManager
from database.init_db import init_database
from database.init_test_data import init_test_data

async def main():
    try:
        # 1. 初始化数据库表
        logger.info("初始化数据库...")
        init_database()
        
        # 2. 初始化测试数据
        logger.info("初始化测试数据...")
        init_test_data()
        
        # 3. 创建爬虫管理器并开始爬取
        logger.info("开始爬取文章...")
        crawler = CrawlerManager()
        await crawler.start_crawl(public_account_id=1)
        
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        raise
    finally:
        # 确保浏览器正常关闭
        if 'crawler' in locals() and hasattr(crawler, 'browser_manager'):
            await crawler.browser_manager.close()

if __name__ == "__main__":
    asyncio.run(main()) 