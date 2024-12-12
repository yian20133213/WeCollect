from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QSpinBox, QTabWidget,
    QFormLayout, QCheckBox, QWidget
)
from PyQt6.QtCore import Qt
from loguru import logger

class ConfigDialog(QDialog):
    """配置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置")
        self.setMinimumWidth(500)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 基础配置标签页
        basic_tab = QWidget()
        basic_layout = QFormLayout(basic_tab)
        
        self.data_dir = QLineEdit()
        basic_layout.addRow("数据目录:", self.data_dir)
        
        self.thread_count = QSpinBox()
        self.thread_count.setRange(1, 10)
        basic_layout.addRow("最大线程数:", self.thread_count)
        
        self.auto_retry = QCheckBox("自动重试")
        basic_layout.addRow("失败处理:", self.auto_retry)
        
        tab_widget.addTab(basic_tab, "基础配置")
        
        # 导出配置标签页
        export_tab = QWidget()
        export_layout = QFormLayout(export_tab)
        
        self.export_dir = QLineEdit()
        export_layout.addRow("导出目录:", self.export_dir)
        
        self.export_html = QCheckBox("HTML")
        self.export_pdf = QCheckBox("PDF")
        self.export_markdown = QCheckBox("Markdown")
        
        export_formats = QHBoxLayout()
        export_formats.addWidget(self.export_html)
        export_formats.addWidget(self.export_pdf)
        export_formats.addWidget(self.export_markdown)
        export_layout.addRow("导出格式:", export_formats)
        
        tab_widget.addTab(export_tab, "导出配置")
        
        # 添加按钮
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self._save_config)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
    def _save_config(self):
        """保存配置"""
        try:
            # TODO: 实现配置保存逻辑
            self.accept()
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}") 