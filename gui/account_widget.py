from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QMessageBox,
    QLabel, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
import io
from utils.wx_api import WeChatAPI
from loguru import logger

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("微信登录")
        self.setFixedSize(300, 400)
        self.api = WeChatAPI()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_scan_status)
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # 添加说明文字
        tip_label = QLabel("请使用微信扫描二维码登录")
        tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tip_label)
        
        # 添加二维码显示区域
        self.qr_label = QLabel()
        self.qr_label.setFixedSize(200, 200)
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qr_label)
        
        # 添加状态显示
        self.status_label = QLabel("等待扫码...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # TODO: 获取登录二维码并显示
        self.show_qrcode()
        
    def show_qrcode(self):
        """显示登录二维码"""
        uuid = self.api.get_qr_uuid()
        if not uuid:
            self.status_label.setText("获取二维码失败")
            return
            
        qr_data = self.api.get_qr_code()
        if not qr_data:
            self.status_label.setText("获取二维码失败")
            return
            
        qr_pixmap = QPixmap()
        qr_pixmap.loadFromData(qr_data)
        self.qr_label.setPixmap(qr_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        
        # 开始检查扫码状态
        self.check_timer.start(2000)  # 每2秒检查一次
        
    def check_scan_status(self):
        """检查扫码状态"""
        status = self.api.check_scan()
        
        if status == 408:
            self.status_label.setText("等待扫码...")
        elif status == 201:
            self.status_label.setText("扫码成功，请在手机上确认")
        elif status == 200:
            self.status_label.setText("登录成功")
            self.check_timer.stop()
            if self.api.login():
                self.accept()
            else:
                self.status_label.setText("登录失败")

class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加公众号")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout()
        
        self.name = QLineEdit()
        layout.addRow("公众号名称:", self.name)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        
        layout.addRow(buttons)
        self.setLayout(layout)

class AccountWidget(QWidget):
    """账号管理界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wx_api = WeChatAPI()
        self.accounts = []
        self.uuid = None
        self.init_ui()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_login_status)
        
    def init_ui(self):
        # 使用垂直布局
        main_layout = QVBoxLayout(self)
        
        # 登录状态显示区域
        self.status_label = QLabel("未登录")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # 二维码显示区域
        self.qr_label = QLabel()
        self.qr_label.setFixedSize(280, 280)  # 增大二维码显示尺寸
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.qr_label)
        
        # 登录按钮
        self.login_button = QPushButton("扫码登录")
        self.login_button.clicked.connect(self.start_login)
        main_layout.addWidget(self.login_button)
        
        # 公众号管理区域（初始隐藏）
        self.account_widget = QWidget()
        account_layout = QVBoxLayout(self.account_widget)
        
        # 公众号列表
        self.account_table = QTableWidget()
        self.account_table.setColumnCount(3)
        self.account_table.setHorizontalHeaderLabels(["公众号名称", "采集状态", "操作"])
        header = self.account_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.account_table.setColumnWidth(1, 100)
        self.account_table.setColumnWidth(2, 150)
        account_layout.addWidget(self.account_table)
        
        # 添加公众号按钮
        self.add_account_btn = QPushButton("添加公众号")
        self.add_account_btn.clicked.connect(self.show_add_account_dialog)
        account_layout.addWidget(self.add_account_btn)
        
        main_layout.addWidget(self.account_widget)
        self.account_widget.hide()  # 初始隐藏公众号管理区域
        
        # 添加一些底部间距
        main_layout.addStretch()
        
    def start_login(self):
        """开始登录流程"""
        try:
            self.login_button.setEnabled(False)
            self.status_label.setText("正在获取二维码...")
            QApplication.processEvents()
            
            self.uuid = self.wx_api.get_qr_uuid()
            if not self.uuid:
                raise Exception("获取二维码UUID失败")
                
            qr_data = self.wx_api.get_qr_code(self.uuid)
            if not qr_data:
                raise Exception("获取二维码图片失败")
                
            # 显示二维码
            pixmap = QPixmap()
            pixmap.loadFromData(qr_data)
            scaled_pixmap = pixmap.scaled(
                280, 280,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.qr_label.setPixmap(scaled_pixmap)
            
            # 启动状态检查
            self.status_label.setText("请使用微信扫描二维码")
            self.check_timer.start(2000)
            
        except Exception as e:
            logger.error(f"启动登录失败: {str(e)}")
            self.status_label.setText(f"登录失败: {str(e)}")
            self.login_button.setEnabled(True)
            
    def login_success(self):
        """登录成功后的处理"""
        try:
            # 更新UI状态
            self.status_label.setText("登录成功")
            self.qr_label.clear()
            self.login_button.hide()
            
            # 显示公众号管理界面
            self.account_widget.show()
            
            # 刷新公众号列表
            self.refresh_account_list()
            
            logger.info("登录成功，界面已更新")
            
        except Exception as e:
            logger.error(f"处理登录成功状态失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"更新界面失败: {str(e)}")
            
    def check_login_status(self):
        """检查登录状态"""
        try:
            status = self.wx_api.check_scan(self.uuid)
            logger.debug(f"登录状态检查: {status}")
            
            if status == 408:  # 超时
                self.status_label.setText("二维码已超时，请重新获取")
                self.check_timer.stop()
                self.login_button.setEnabled(True)
                
            elif status == 201:  # 已扫码
                self.status_label.setText("已扫码，请在手机上确认")
                
            elif status == 200:  # 确认
                self.check_timer.stop()
                self.status_label.setText("正在登录...")
                QApplication.processEvents()
                
                if self.wx_api.login(self.uuid):
                    self.login_success()
                else:
                    raise Exception("登录失败")
                    
        except Exception as e:
            logger.error(f"登录状态检查失败: {str(e)}")
            self.status_label.setText("登录失败，请重试")
            self.check_timer.stop()
            self.login_button.setEnabled(True)

    def show_add_account_dialog(self):
        """显示添加公众号对话框"""
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            account_name = dialog.name.text().strip()
            if account_name:
                self.add_account(account_name)
    
    def add_account(self, account_name):
        """添加公众号到列表"""
        if account_name not in self.accounts:
            self.accounts.append(account_name)
            self.refresh_account_list()
    
    def refresh_account_list(self):
        """刷新公众号列表"""
        self.account_table.setRowCount(len(self.accounts))
        for row, account in enumerate(self.accounts):
            # 公众号名称
            name_item = QTableWidgetItem(account)
            self.account_table.setItem(row, 0, name_item)
            
            # 状态列
            status_item = QTableWidgetItem("未采集")
            self.account_table.setItem(row, 1, status_item)
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(5, 2, 5, 2)
            
            collect_btn = QPushButton("采集文章")
            collect_btn.clicked.connect(lambda checked, a=account: self.start_collect(a))
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(lambda checked, a=account: self.delete_account(a))
            
            btn_layout.addWidget(collect_btn)
            btn_layout.addWidget(delete_btn)
            
            self.account_table.setCellWidget(row, 2, btn_widget)
    
    def delete_account(self, account_name):
        """删除公众号"""
        if account_name in self.accounts:
            self.accounts.remove(account_name)
            self.refresh_account_list()

    def start_collect(self, account_name):
        """开始采集文章"""
        try:
            self.update_account_status(account_name, "采集中...")
            QApplication.processEvents()
            
            # 调用API采集文章
            articles = self.wx_api.get_articles(account_name)
            
            if articles:
                # 保存到数据库
                self.save_articles(account_name, articles)
                self.update_account_status(account_name, f"成功 ({len(articles)}篇)")
            else:
                self.update_account_status(account_name, "无新文章")
                
        except Exception as e:
            logger.error(f"采集文章失败: {str(e)}")
            self.update_account_status(account_name, "采集失败")
            QMessageBox.warning(self, "错误", f"采集文章失败: {str(e)}")

    def update_account_status(self, account_name, status):
        """更新账号采集状态"""
        for row in range(self.account_table.rowCount()):
            if self.account_table.item(row, 0).text() == account_name:
                self.account_table.item(row, 1).setText(status)
                break

    def save_articles(self, account_name, articles):
        """保存文章到数据库"""
        try:
            # 这里需要实现数据库保存逻辑
            from database.db_manager import save_articles
            save_articles(account_name, articles)
            logger.info(f"成功保存 {len(articles)} 篇文章")
        except Exception as e:
            logger.error(f"保存文章失败: {str(e)}")
            raise

    def closeEvent(self, event):
        """窗口关闭时停止定时器"""
        self.check_timer.stop()
        super().closeEvent(event)
