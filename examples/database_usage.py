import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from database.connection import db
from database.crud_article import article_crud

async def example_usage():
    # 创建文章
    article_data = {
        "title": "测试文章",
        "author": "测试作者",
        "url": "https://example.com/article/1",
        "public_account_id": 1,
        "publish_time": datetime.now(),
        "status": 0
    }
    
    with db.get_session() as session:
        # 创建文章
        article = article_crud.create(session, data=article_data)
        print(f"创建文章: {article.id}")
        
        # 获取文章
        article = article_crud.get(session, article.id)
        print(f"获取文章: {article.title}")
        
        # 更新文章状态
        article = article_crud.update_status(session, article.id, status=1)
        print(f"更新文章状态: {article.status}")
        
        # 获取待采集文章
        pending_articles = article_crud.get_pending_articles(session)
        print(f"待采集文章数: {len(pending_articles)}")
        
        # 获取日期范围内的文章
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        articles = article_crud.get_by_date_range(
            session,
            start_date=start_date,
            end_date=end_date
        )
        print(f"最近7天文章数: {len(articles)}") 