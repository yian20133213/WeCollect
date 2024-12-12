from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar,
    QComboBox, QSpinBox, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from loguru import logger

class TaskWidget(QWidget):
    """任务管理界面"""
    
    # 自定义信号
    task_status_changed = pyqtSignal(str)
    task_completed = pyqtSignal(int)  # 任务ID
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_signals()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 添加控制面板
        control_layout = QHBoxLayout()
        layout.addLayout(control_layout)
        
        # 添加账号选择
        self.account_combo = QComboBox()
        self.account_combo.setMinimumWidth(200)
        control_layout.addWidget(QLabel("账号:"))
        control_layout.addWidget(self.account_combo)
        
        # 添加并发数设置
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 10)
        self.concurrent_spin.setValue(3)
        control_layout.addWidget(QLabel("并发数:"))
        control_layout.addWidget(self.concurrent_spin)
        
        # 添加控制按钮
        self.start_btn = QPushButton("开始采集")
        self.pause_btn = QPushButton("暂停")
        self.stop_btn = QPushButton("停止")
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        
        control_layout.addStretch()
        
        # 添加任务列表
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels([
            "ID", "公众号", "状态", "进度", "操作"
        ])
        layout.addWidget(self.task_table)
        
    def _init_signals(self):
        """初始化信号连接"""
        self.start_btn.clicked.connect(self._start_task)
        self.pause_btn.clicked.connect(self._pause_task)
        self.stop_btn.clicked.connect(self._stop_task)
        
    def _start_task(self):
        """开始任务"""
        try:
            # TODO: 实现任务启动逻辑
            self.task_status_changed.emit("任务已启动")
        except Exception as e:
            logger.error(f"启动任务失败: {str(e)}")
            
    def _pause_task(self):
        """暂停任务"""
        try:
            # TODO: 实现任务暂停逻辑
            self.task_status_changed.emit("任务已暂停")
        except Exception as e:
            logger.error(f"暂停任务失败: {str(e)}")
            
    def _stop_task(self):
        """停止任务"""
        try:
            # TODO: 实现任务停止逻辑
            self.task_status_changed.emit("任务已停止")
        except Exception as e:
            logger.error(f"停止任务失败: {str(e)}")
            
    def add_task(self, task_data: dict):
        """添加任务到列表"""
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)
        
        # 设置任务信息
        self.task_table.setItem(row, 0, QTableWidgetItem(str(task_data['id'])))
        self.task_table.setItem(row, 1, QTableWidgetItem(task_data['name']))
        self.task_table.setItem(row, 2, QTableWidgetItem("等待中"))
        
        # 添加进度条
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        self.task_table.setCellWidget(row, 3, progress_bar)
        
        # 添加操作按钮
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(lambda: self._delete_task(row))
        btn_layout.addWidget(delete_btn)
        
        self.task_table.setCellWidget(row, 4, btn_widget)
        
    def update_task_progress(self, task_id: int, progress: int, status: str):
        """更新任务进度"""
        for row in range(self.task_table.rowCount()):
            if self.task_table.item(row, 0).text() == str(task_id):
                self.task_table.item(row, 2).setText(status)
                progress_bar = self.task_table.cellWidget(row, 3)
                progress_bar.setValue(progress)
                break 