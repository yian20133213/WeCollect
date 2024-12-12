import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict
from loguru import logger

from config.settings import DATA_DIR

class CookieManager:
    """Cookie管理类"""
    
    def __init__(self):
        self.cookie_dir = DATA_DIR / "cookies"
        self.cookie_dir.mkdir(parents=True, exist_ok=True)
        
    def save_cookies(self, account_id: int, cookies: Dict) -> bool:
        """保存Cookie"""
        try:
            cookie_file = self.cookie_dir / f"cookie_{account_id}.pkl"
            cookie_data = {
                "cookies": cookies,
                "timestamp": datetime.now().timestamp(),
                "account_id": account_id
            }
            
            with open(cookie_file, "wb") as f:
                pickle.dump(cookie_data, f)
            logger.info(f"Cookie保存成功: account_id={account_id}")
            return True
        except Exception as e:
            logger.error(f"Cookie保存失败: {str(e)}")
            return False
    
    def load_cookies(self, account_id: int) -> Optional[Dict]:
        """加载Cookie"""
        try:
            cookie_file = self.cookie_dir / f"cookie_{account_id}.pkl"
            if not cookie_file.exists():
                return None
                
            with open(cookie_file, "rb") as f:
                cookie_data = pickle.load(f)
                
            # 检查Cookie是否过期（默认7天）
            if datetime.now().timestamp() - cookie_data["timestamp"] > 7 * 24 * 3600:
                logger.warning(f"Cookie已过期: account_id={account_id}")
                return None
                
            return cookie_data["cookies"]
        except Exception as e:
            logger.error(f"Cookie加载失败: {str(e)}")
            return None
            
    def delete_cookies(self, account_id: int) -> bool:
        """删除Cookie"""
        try:
            cookie_file = self.cookie_dir / f"cookie_{account_id}.pkl"
            if cookie_file.exists():
                cookie_file.unlink()
            return True
        except Exception as e:
            logger.error(f"Cookie删除失败: {str(e)}")
            return False 