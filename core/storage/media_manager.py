import asyncio
import aiohttp
import hashlib
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime
from loguru import logger

from .file_manager import FileManager
from database.models import Media
from database.crud_media import media_crud
from database.db_manager import db_manager
from utils.retry import retry_async

class MediaManager:
    """媒体文件管理器"""
    
    def __init__(self):
        self.file_manager = FileManager()
        self.session = None
        
    async def init_session(self):
        """初始化HTTP会话"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close_session(self):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.session = None
            
    @retry_async(max_retries=3, delay=2)
    async def download_media(self, media: Media) -> Optional[Path]:
        """下载媒体文件"""
        try:
            if not self.session:
                await self.init_session()
                
            # 生成文件名
            url_hash = hashlib.md5(media.url.encode()).hexdigest()
            ext = media.url.split('.')[-1].lower()
            filename = f"{url_hash}.{ext}"
            
            # 下载文件
            async with self.session.get(media.url) as response:
                if response.status != 200:
                    raise Exception(f"下载失败: HTTP {response.status}")
                    
                content = await response.read()
                
            # 保存文件
            file_path = self.file_manager.save_file(
                content,
                media.type,
                filename
            )
            
            if file_path:
                # 更新数据库记录
                with db_manager.get_session() as session:
                    media_crud.update(session, media.id, {
                        "local_path": str(file_path),
                        "status": 2,  # 下载完成
                        "updated_at": datetime.now()
                    })
                    
            return file_path
            
        except Exception as e:
            logger.error(f"媒体下载失败: {str(e)}")
            # 更新失败状态
            with db_manager.get_session() as session:
                media_crud.update(session, media.id, {
                    "status": 3,  # 下载失败
                    "error_msg": str(e),
                    "updated_at": datetime.now()
                })
            raise
            
    async def batch_download(self, media_list: List[Media], max_concurrent: int = 5) 