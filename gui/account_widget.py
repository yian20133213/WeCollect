from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加账号")
        self._init_ui()
        
    def _init_ui(self):
        layout = QFormLayout(self)
        
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout.addRow("用户名:", self.username)
        layout.addRow("密码:", self.password)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)

class AccountWidget(QWidget):
    """账号管理界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建工具栏
        toolbar = QHBoxLayout()
        layout.addLayout(toolbar)
        
        # 添加按钮
        add_btn = QPushButton("添加账号")
        add_btn.clicked.connect(self._add_account)
        toolbar.addWidget(add_btn)
        
        delete_btn = QPushButton("删除账号")
        delete_btn.clicked.connect(self._delete_account)
        toolbar.addWidget(delete_btn)
        
        toolbar.addStretch()
        
        # 创建账号表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["用户名", "密码", "状态", "上次使用时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # 初始化数据
        self._load_accounts()
        
    def _load_accounts(self):
        """加载账号数据"""
        # TODO: 从数据库或配置文件加载账号数据
        pass
        
    def _add_account(self):
        """添加账号"""
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username = dialog.username.text().strip()
            password = dialog.password.text().strip()
            
            if not username or not password:
                QMessageBox.warning(self, "错误", "用户名和密码不能为空！")
                return
            
            # 添加到表格
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(username))
            self.table.setItem(row, 1, QTableWidgetItem("*" * len(password)))
            self.table.setItem(row, 2, QTableWidgetItem("未使用"))
            self.table.setItem(row, 3, QTableWidgetItem(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            # TODO: 保存到数据库
        
    def _delete_account(self):
        """删除账号"""
        # TODO: 实现删除账号功能
        pass
