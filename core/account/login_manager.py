import asyncio
from datetime import datetime
import time
from typing import Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

from database.models import Account
from database.db_manager import db_manager
from .cookie_manager import CookieManager
from utils.browser import create_browser

class LoginManager:
    """登录管理类"""
    
    def __init__(self):
        self.cookie_manager = CookieManager()
        self.login_url = "https://mp.weixin.qq.com/"
        self.qrcode_selector = "#qrcode img"  # 二维码元素选择器
        
    async def check_login_status(self, account_id: int) -> bool:
        """检查登录状态"""
        try:
            with db_manager.get_session() as db:
                account = db.query(Account).filter(Account.id == account_id).first()
                if not account:
                    return False
                    
                # 检查最后登录时间是否在24小时内
                if account.last_login:
                    delta = datetime.now() - account.last_login
                    if delta.total_seconds() < 24 * 3600:
                        return True
                        
            # 尝试验证Cookie
            cookies = self.cookie_manager.load_cookies(account_id)
            if not cookies:
                return False
                
            return await self._verify_cookies(cookies)
        except Exception as e:
            logger.error(f"登录状态检查失败: {str(e)}")
            return False
            
    async def login(self, account_id: int) -> Tuple[bool, str]:
        """执行登录流程"""
        try:
            # 检查是否已登录
            if await self.check_login_status(account_id):
                return True, "已登录"
                
            # 创建浏览器实例
            browser = await create_browser()
            try:
                # 打开登录页面
                await browser.get(self.login_url)
                
                # 等待二维码出现
                qr_element = await browser.wait_for_element(self.qrcode_selector, timeout=10)
                qr_image = await qr_element.get_attribute("src")
                
                # 等待扫码登录
                success = await self._wait_for_scan(browser)
                if not success:
                    return False, "扫码超时"
                    
                # 获取并保存Cookie
                cookies = await browser.get_cookies()
                self.cookie_manager.save_cookies(account_id, cookies)
                
                # 更新账号登录时间
                with db_manager.get_session() as db:
                    account = db.query(Account).filter(Account.id == account_id).first()
                    account.last_login = datetime.now()
                    db.commit()
                
                return True, "登录成功"
                
            finally:
                await browser.close()
                
        except Exception as e:
            logger.error(f"登录失败: {str(e)}")
            return False, f"登录异常: {str(e)}"
            
    async def _wait_for_scan(self, browser, timeout: int = 120) -> bool:
        """等待用户扫码"""
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                # 检查是否已登录成功
                if "logged_in" in browser.current_url:
                    return True
                await asyncio.sleep(1)
            return False
        except Exception as e:
            logger.error(f"等待扫码失败: {str(e)}")
            return False
            
    async def _verify_cookies(self, cookies: dict) -> bool:
        """验证Cookie是否有效"""
        try:
            browser = await create_browser()
            try:
                # 添加Cookie
                await browser.get(self.login_url)
                for cookie in cookies:
                    await browser.add_cookie(cookie)
                    
                # 刷新页面
                await browser.refresh()
                
                # 检查是否需要重新登录
                login_elements = await browser.find_elements(By.CSS_SELECTOR, ".login__type__container")
                return len(login_elements) == 0
                
            finally:
                await browser.close()
        except Exception as e:
            logger.error(f"Cookie验证失败: {str(e)}")
            return False 