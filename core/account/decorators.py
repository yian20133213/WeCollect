import functools
from typing import Callable
from loguru import logger

from .login_manager import LoginManager

def login_required(func: Callable):
    """登录验证装饰器"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # 获取account_id参数
        account_id = kwargs.get('account_id')
        if not account_id:
            for arg in args:
                if hasattr(arg, 'account_id'):
                    account_id = arg.account_id
                    break
        
        if not account_id:
            raise ValueError("未找到account_id参数")
            
        # 检查登录状态
        login_manager = LoginManager()
        is_logged_in = await login_manager.check_login_status(account_id)
        
        if not is_logged_in:
            # 尝试重新登录
            success, msg = await login_manager.login(account_id)
            if not success:
                raise Exception(f"登录失败: {msg}")
                
        # 执行原函数
        return await func(*args, **kwargs)
        
    return wrapper 