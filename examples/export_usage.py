import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 首先设置EXPORT配置
from core.config import EXPORT
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 在导入其他模块之前设置配置
EXPORT.clear()
EXPORT.update({
    'output_dir': os.path.join(ROOT_DIR, 'exports'),
    'template_dir': os.path.join(ROOT_DIR, 'core', 'export', 'templates'),
    'encoding': 'utf-8',
})

# 确保目录存在
os.makedirs(EXPORT['output_dir'], exist_ok=True)
os.makedirs(EXPORT['template_dir'], exist_ok=True)

# 然后再导入其他模块
import asyncio
from core.export.export_manager import ExportManager
from database.models import Article
from database.crud_article import article_crud
from database.db_manager import db_manager

async def main():
    # 创建导出管理器
    export_manager = ExportManager()
    
    # 获取要导出的文章
    with db_manager.get_session() as session:
        articles = article_crud.get_multi(session, limit=10)
        
    # 导出单篇文章
    article = articles[0]
    result = await export_manager.export_article(
        article,
        formats=['html', 'pdf', 'markdown']
    )
    print(f"单篇文章导出结果: {result}")
    
    # 批量导出文章
    results = await export_manager.batch_export(
        articles,
        formats=['html', 'pdf']
    )
    print(f"批量导出结果: {results}")

if __name__ == "__main__":
    asyncio.run(main()) 