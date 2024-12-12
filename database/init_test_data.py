import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from loguru import logger
from database.connection import db
from database.models import Account, PublicAccount, Article
from database.init_db import init_database

def init_test_data():
    """初始化测试数据"""
    try:
        # 先确保数据库表已创建
        init_database()
        
        with db.get_session() as session:
            # 1. 创建测试账号
            test_account = Account(
                nickname="测试账号",
                cookie="test_cookie",
                last_login=datetime.now(),
                status=1
            )
            session.add(test_account)
            session.flush()  # 获取ID
            
            # 2. 创建测试公众号
            test_public_account = PublicAccount(
                name="Python编程",
                biz="MzI5MjAxNzM4MA==",  # 示例biz
                description="分享Python编程技术和经验",
                status=1,
                last_sync=datetime.now()
            )
            session.add(test_public_account)
            session.flush()  # 获取ID
            
            # 3. 创建测试文章
            test_articles = [
                Article(
                    public_account_id=test_public_account.id,
                    title="Sora之后，苹果发布视频生成大模型STIV，87亿参数一统T2V、TI2V任务",
                    author="机器之心",
                    url="https://mp.weixin.qq.com/s?src=11&timestamp=1734000105&ver=5684&signature=reVAWVQtVIRsc9s15cVVZLvxeyKDLeXdTtkmw0R3hm8LnzzF-9OyFualtUeW8KJguDBU1VYbKB-bg-oC9WUfl9c6iH2fzecUQCRkPwm-I14Mswv9vCLe1ZdOa*6ItXbK&new=1",
                    content="",  # 待爬取
                    status=0,  # 待采集
                    publish_time=datetime(2024, 12, 12)
                ),
                Article(
                    public_account_id=test_public_account.id,
                    title="更快、更高清、能剪辑，新版Sora来了",
                    author=" 果壳",
                    url="https://mp.weixin.qq.com/s?src=11&timestamp=1734000105&ver=5684&signature=C*5oI5OkLvTORPE4PMU7KPc1Uk3G9orX57gYNxYGSzvZVl5gXAvhFWVbfPzfJzEqCxbr4XLUjKhKEDzJ8bH0MApOe7JyThSS4w7iqwFsHxIBoS6Zh00sS0lYhgckLqa9&new=1",
                    content="",  # 待爬取
                    status=0,  # 待采集
                    publish_time=datetime(2024, 12, 10)
                )
            ]
            
            session.add_all(test_articles)
            session.commit()
            
            logger.info(f"测试数据初始化成功：")
            logger.info(f"- 创建测试账号: {test_account.nickname}")
            logger.info(f"- 创建测试公众号: {test_public_account.name}")
            logger.info(f"- 创建测试文章: {len(test_articles)}篇")
            
    except Exception as e:
        logger.error(f"测试数据初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    init_test_data() 