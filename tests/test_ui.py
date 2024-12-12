import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLineEdit, QLabel, QTextEdit)

class WeChatCrawlerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置主窗口
        self.setWindowTitle('微信公众号文章采集器')
        self.setGeometry(300, 300, 800, 600)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加输入框
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText('请输入公众号名称')
        layout.addWidget(QLabel('目标公众号：'))
        layout.addWidget(self.account_input)
        
        # 添加按钮
        start_btn = QPushButton('开始采集')
        start_btn.clicked.connect(self.start_crawling)
        layout.addWidget(start_btn)
        
        # 添加日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(QLabel('运行日志：'))
        layout.addWidget(self.log_area)
        
    def start_crawling(self):
        account = self.account_input.text()
        self.log_area.append(f'开始采集公众号: {account}')
        # 这里添加实际的采集逻辑
        
def main():
    app = QApplication(sys.argv)
    ui = WeChatCrawlerUI()
    ui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()