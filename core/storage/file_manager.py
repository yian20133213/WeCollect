import os
import shutil
import hashlib
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from loguru import logger

from config.settings import DATA_DIR

class FileManager:
    """文件系统管理类"""
    
    def __init__(self):
        self.root_dir = DATA_DIR
        self.articles_dir = self.root_dir / "articles"
        self.images_dir = self.root_dir / "images"
        self.videos_dir = self.root_dir / "videos"
        self.cache_dir = self.root_dir / "cache"
        
        # 创建必要的目录
        self._init_directories()
        
    def _init_directories(self):
        """初始化目录结构"""
        dirs = [
            self.articles_dir,
            self.images_dir,
            self.videos_dir,
            self.cache_dir
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def get_file_path(self, file_type: str, filename: str) -> Path:
        """获取文件路径"""
        if file_type == "article":
            base_dir = self.articles_dir
        elif file_type == "image":
            base_dir = self.images_dir
        elif file_type == "video":
            base_dir = self.videos_dir
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")
            
        # 使用日期作为子目录
        today = datetime.now().strftime("%Y%m%d")
        dir_path = base_dir / today
        dir_path.mkdir(exist_ok=True)
        
        return dir_path / filename
        
    def save_file(self, content: bytes, file_type: str, filename: str) -> Optional[Path]:
        """保存文件"""
        try:
            file_path = self.get_file_path(file_type, filename)
            
            # 确保文件名唯一
            if file_path.exists():
                base, ext = os.path.splitext(filename)
                filename = f"{base}_{datetime.now().strftime('%H%M%S')}{ext}"
                file_path = self.get_file_path(file_type, filename)
            
            # 写入文件
            with open(file_path, 'wb') as f:
                f.write(content)
                
            logger.info(f"文件保存成功: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"文件保存失败: {str(e)}")
            return None
            
    def delete_file(self, file_path: Path) -> bool:
        """删除文件"""
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"文件删除成功: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"文件删除失败: {str(e)}")
            return False
            
    def clean_old_files(self, days: int = 30) -> int:
        """清理旧文件"""
        try:
            count = 0
            cutoff = datetime.now().timestamp() - (days * 24 * 3600)
            
            for dir_path in [self.articles_dir, self.images_dir, self.videos_dir]:
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file() and file_path.stat().st_mtime < cutoff:
                        self.delete_file(file_path)
                        count += 1
                        
            logger.info(f"清理完成: 删除{count}个文件")
            return count
            
        except Exception as e:
            logger.error(f"清理文件失败: {str(e)}")
            return 0 