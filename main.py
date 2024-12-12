import sys
from PyQt6.QtWidgets import QApplication
from loguru import logger

from gui.main_window import MainWindow
from database.db_manager import init_database
from utils.logger import setup_logger

def main():
    # 初始化日志
    setup_logger()
    logger.info("启动微信公众号文章采集工具")
    
    try:
        # 初始化数据库
        init_database()
        
        # 启动GUI应用
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
