import pickle
from typing import Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from loguru import logger

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: Path, default_ttl: int = 3600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        # 使用MD5生成文件名
        filename = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / filename
        
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        try:
            cache_path = self._get_cache_path(key)
            ttl = ttl if ttl is not None else self.default_ttl
            
            cache_data = {
                "value": value,
                "expires_at": datetime.now() + timedelta(seconds=ttl)
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
                
            return True
            
        except Exception as e:
            logger.error(f"设置缓存失败: {str(e)}")
            return False
            
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        try:
            cache_path = self._get_cache_path(key)
            
            if not cache_path.exists():
                return None
                
            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)
                
            # 检查是否过期
            if datetime.now() > cache_data["expires_at"]:
                self.delete(key)
                return None
                
            return cache_data["value"]
            
        except Exception as e:
            logger.error(f"获取缓存失败: {str(e)}")
            return None
            
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            cache_path = self._get_cache_path(key)
            if cache_path.exists():
                cache_path.unlink()
            return True
        except Exception as e:
            logger.error(f"删除缓存失败: {str(e)}")
            return False
            
    def clear_expired(self) -> int:
        """清理过期缓存"""
        try:
            count = 0
            for cache_path in self.cache_dir.glob("*"):
                try:
                    with open(cache_path, 'rb') as f:
                        cache_data = pickle.load(f)
                        
                    if datetime.now() > cache_data["expires_at"]:
                        cache_path.unlink()
                        count += 1
                except:
                    # 如果文件损坏，直接删除
                    cache_path.unlink()
                    count += 1
                    
            logger.info(f"清理过期缓存完成: 删除{count}个文件")
            return count
            
        except Exception as e:
            logger.error(f"清理过期缓存失败: {str(e)}")
            return 0 