import asyncio
from core.storage.file_manager import FileManager
from core.storage.media_manager import MediaManager
from core.storage.cache_manager import CacheManager
from database.models import Media
from config.settings import DATA_DIR

async def main():
    # 文件管理器示例
    file_manager = FileManager()
    # 保存文章内容
    article_content = "文章内容...".encode('utf-8')
    article_path = file_manager.save_file(
        article_content,
        "article", 
        "test_article.html"
    )
    
    # 媒体管理器示例
    media_manager = MediaManager()
    
    # 创建测试媒体记录
    test_media = Media(
        url="https://example.com/image.jpg",
        type="image",
        article_id=1,
        status=0
    )
    
    # 下载媒体文件
    file_path = await media_manager.download_media(test_media)
    
    # 缓存管理器示例
    cache_manager = CacheManager(DATA_DIR / "cache")
    
    # 设置缓存
    cache_manager.set("test_key", {"data": "test"}, ttl=3600)
    
    # 获取缓存
    cached_data = cache_manager.get("test_key")
    
    # 清理过期��存
    cleaned_count = cache_manager.clear_expired()

if __name__ == "__main__":
    asyncio.run(main()) 