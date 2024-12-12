import asyncio
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Optional, List
from loguru import logger

class BrowserManager:
    """浏览器管理类"""
    
    def __init__(self):
        self.options = self._init_chrome_options()
        self.driver = None
        
    def _init_chrome_options(self) -> uc.ChromeOptions:
        """初始化Chrome选项"""
        options = uc.ChromeOptions()
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        # 设置用户代理
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...')
        return options
        
    async def init_browser(self):
        """初始化浏览器"""
        try:
            self.driver = uc.Chrome(options=self.options)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise
            
    async def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            
    async def wait_for_element(self, selector: str, timeout: int = 10):
        """等待元素出现"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except Exception as e:
            logger.error(f"等待元素超时: {selector}")
            raise 