from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QStatusBar, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction
from loguru import logger

from gui.config_dialog import ConfigDialog
from gui.task_widget import TaskWidget
from gui.result_widget import ResultWidget
from gui.account_widget import AccountWidget
from config.settings import APP_NAME

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1200, 800)
        
        # 初始化UI
        self._init_ui()
        self._init_menubar()
        self._init_statusbar()
        self._init_signals()
        
    def _init_ui(self):
        """初始化UI"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 添加任务管理标签页
        self.task_widget = TaskWidget()
        tab_widget.addTab(self.task_widget, "任务管理")
        
        # 添加结果展示标签页
        self.result_widget = ResultWidget()
        tab_widget.addTab(self.result_widget, "采集结果")
        
        # 添加账号管理标签页
        self.account_widget = AccountWidget()
        tab_widget.addTab(self.account_widget, "账号管理")
        
    def _init_menubar(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        # 配置选项
        config_action = QAction("配置", self)
        config_action.triggered.connect(self._show_config_dialog)
        file_menu.addAction(config_action)
        
        # 导出选项
        export_action = QAction("导出数据", self)
        export_action.triggered.connect(self._export_data)
        file_menu.addAction(export_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _init_statusbar(self):
        """初始化状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # 添加状态信息
        self.status_label = QLabel()
        self.statusbar.addWidget(self.status_label)
        
        # 添加进度信息
        self.progress_label = QLabel()
        self.statusbar.addPermanentWidget(self.progress_label)
        
    def _init_signals(self):
        """初始化信号连接"""
        # 连接任务状态更新信号
        self.task_widget.task_status_changed.connect(self._update_status)
        
        # 连接结果更新信号
        self.task_widget.task_completed.connect(self.result_widget.refresh_results)
        
    def _show_config_dialog(self):
        """显示配置对话框"""
        dialog = ConfigDialog(self)
        dialog.exec()
        
    def _export_data(self):
        """导出数据"""
        # TODO: 实现数据导出功能
        pass
        
    def _show_about(self):
        """显示关于对话框"""
        # TODO: 实现关于对话框
        pass
        
    def _update_status(self, message: str):
        """更新状态栏信息"""
        self.status_label.setText(message)
