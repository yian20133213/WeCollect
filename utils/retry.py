import asyncio
from functools import wraps
from typing import TypeVar, Callable
from loguru import logger

T = TypeVar("T")

def retry_async(max_retries: int = 3, delay: int = 1):
    """异步重试装饰器"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"重试 {attempt + 1}/{max_retries}: {func.__name__}, "
                        f"错误: {str(e)}"
                    )
                    if attempt + 1 < max_retries:
                        await asyncio.sleep(delay * (attempt + 1))
            
            logger.error(
                f"重试{max_retries}次后失败: {func.__name__}, "
                f"错误: {str(last_exception)}"
            )
            raise last_exception
            
        return wrapper
    return decorator 