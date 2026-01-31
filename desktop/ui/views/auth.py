"""
Authentication View - Login and Registration
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont
from ..components.cards import AlertCard
from api import api_client, ApiError


class AuthWorker(QObject):
    """Worker thread for authentication"""
    login_success = pyqtSignal(dict)
    register_success = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, action: str, username: str, password: str, email: str = ""):
        super().__init__()
        self.action = action
        self.username = username
        self.password = password
        self.email = email
    
    def run(self):
        try:
            if self.action == "login":
                result = api_client.login(self.username, self.password)
                self.login_success.emit(result)
            else:
                result = api_client.register(self.username, self.password, self.email)
                self.register_success.emit(result)
        except ApiError as e:
            self.error.emit(e.message)
        except Exception as e:
            self.error.emit(str(e))


class AuthView(QWidget):
    """View for user authentication"""
    
    auth_changed = pyqtSignal(bool)  # True = logged in, False = logged out
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_thread = None
        self.auth_worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(24)
        
        # Header
        header = QLabel("Account")
        header.setObjectName("heading")
        header.setFont(QFont("Source Sans 3", 24, QFont.Bold))
        layout.addWidget(header)
        
        # Stacked widget for login/register/logged-in states
        self.stack = QStackedWidget()
        
        # Login form
        self.login_widget = self._create_login_form()
        self.stack.addWidget(self.login_widget)
        
        # Register form
        self.register_widget = self._create_register_form()
        self.stack.addWidget(self.register_widget)
        
        # Logged in state
        self.logged_in_widget = self._create_logged_in_view()
        self.stack.addWidget(self.logged_in_widget)
        
        layout.addWidget(self.stack)
        layout.addStretch()
        
        # Check initial auth state
        self._update_auth_state()
    
    def _create_login_form(self) -> QWidget:
        """Create login form widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Card container
        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(20)
        
        title = QLabel("Sign In")
        title.setFont(QFont("Source Sans 3", 18, QFont.DemiBold))
        title.setStyleSheet("color: #FFFFFF;")
        card_layout.addWidget(title)
        
        # Username
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username")
        self.login_username.setMinimumHeight(44)
        card_layout.addWidget(self.login_username)
        
        # Password
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(44)
        card_layout.addWidget(self.login_password)
        
        # Login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("primary")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.clicked.connect(self._do_login)
        card_layout.addWidget(self.login_btn)
        
        # Login status
        self.login_status = QWidget()
        login_status_layout = QVBoxLayout(self.login_status)
        login_status_layout.setContentsMargins(0, 0, 0, 0)
        self.login_status.hide()
        card_layout.addWidget(self.login_status)
        
        # Switch to register
        switch_row = QHBoxLayout()
        switch_label = QLabel("Don't have an account?")
        switch_label.setStyleSheet("color: #888888;")
        switch_btn = QPushButton("Create Account")
        switch_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #00D9A5;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #00F5BA;
            }
        """)
        switch_btn.setCursor(Qt.PointingHandCursor)
        switch_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        switch_row.addWidget(switch_label)
        switch_row.addWidget(switch_btn)
        switch_row.addStretch()
        card_layout.addLayout(switch_row)
        
        layout.addWidget(card, 0, Qt.AlignTop)
        return widget
    
    def _create_register_form(self) -> QWidget:
        """Create registration form widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(20)
        
        title = QLabel("Create Account")
        title.setFont(QFont("Source Sans 3", 18, QFont.DemiBold))
        title.setStyleSheet("color: #FFFFFF;")
        card_layout.addWidget(title)
        
        # Username
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Username")
        self.reg_username.setMinimumHeight(44)
        card_layout.addWidget(self.reg_username)
        
        # Email
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Email (optional)")
        self.reg_email.setMinimumHeight(44)
        card_layout.addWidget(self.reg_email)
        
        # Password
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Password")
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_password.setMinimumHeight(44)
        card_layout.addWidget(self.reg_password)
        
        # Confirm password
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setPlaceholderText("Confirm Password")
        self.reg_confirm.setEchoMode(QLineEdit.Password)
        self.reg_confirm.setMinimumHeight(44)
        card_layout.addWidget(self.reg_confirm)
        
        # Register button
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setObjectName("primary")
        self.register_btn.setMinimumHeight(48)
        self.register_btn.clicked.connect(self._do_register)
        card_layout.addWidget(self.register_btn)
        
        # Register status
        self.register_status = QWidget()
        register_status_layout = QVBoxLayout(self.register_status)
        register_status_layout.setContentsMargins(0, 0, 0, 0)
        self.register_status.hide()
        card_layout.addWidget(self.register_status)
        
        # Switch to login
        switch_row = QHBoxLayout()
        switch_label = QLabel("Already have an account?")
        switch_label.setStyleSheet("color: #888888;")
        switch_btn = QPushButton("Sign In")
        switch_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #00D9A5;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #00F5BA;
            }
        """)
        switch_btn.setCursor(Qt.PointingHandCursor)
        switch_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        switch_row.addWidget(switch_label)
        switch_row.addWidget(switch_btn)
        switch_row.addStretch()
        card_layout.addLayout(switch_row)
        
        layout.addWidget(card, 0, Qt.AlignTop)
        return widget
    
    def _create_logged_in_view(self) -> QWidget:
        """Create logged-in state view"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(20)
        
        # User icon
        icon = QLabel("👤")
        icon.setStyleSheet("font-size: 48px;")
        icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon)
        
        # Welcome message
        self.welcome_label = QLabel("Welcome!")
        self.welcome_label.setFont(QFont("Source Sans 3", 18, QFont.DemiBold))
        self.welcome_label.setStyleSheet("color: #FFFFFF;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.welcome_label)
        
        # Username display
        self.user_label = QLabel("")
        self.user_label.setStyleSheet("color: #00D9A5; font-size: 14px;")
        self.user_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.user_label)
        
        card_layout.addSpacing(16)
        
        # Logout button
        logout_btn = QPushButton("Sign Out")
        logout_btn.setMinimumHeight(44)
        logout_btn.clicked.connect(self._do_logout)
        card_layout.addWidget(logout_btn)
        
        layout.addWidget(card, 0, Qt.AlignTop)
        return widget
    
    def _do_login(self):
        """Perform login"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            self._show_login_status("Please enter username and password", "error")
            return
        
        self.login_btn.setEnabled(False)
        self._show_login_status("Signing in...", "info")
        
        self.auth_thread = QThread()
        self.auth_worker = AuthWorker("login", username, password)
        self.auth_worker.moveToThread(self.auth_thread)
        
        self.auth_thread.started.connect(self.auth_worker.run)
        self.auth_worker.login_success.connect(self._on_login_success)
        self.auth_worker.error.connect(self._on_login_error)
        self.auth_worker.login_success.connect(self.auth_thread.quit)
        self.auth_worker.error.connect(self.auth_thread.quit)
        
        self.auth_thread.start()
    
    def _do_register(self):
        """Perform registration"""
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()
        
        if not username or not password:
            self._show_register_status("Please fill in required fields", "error")
            return
        
        if password != confirm:
            self._show_register_status("Passwords do not match", "error")
            return
        
        self.register_btn.setEnabled(False)
        self._show_register_status("Creating account...", "info")
        
        self.auth_thread = QThread()
        self.auth_worker = AuthWorker("register", username, password, email)
        self.auth_worker.moveToThread(self.auth_thread)
        
        self.auth_thread.started.connect(self.auth_worker.run)
        self.auth_worker.register_success.connect(self._on_register_success)
        self.auth_worker.error.connect(self._on_register_error)
        self.auth_worker.register_success.connect(self.auth_thread.quit)
        self.auth_worker.error.connect(self.auth_thread.quit)
        
        self.auth_thread.start()
    
    def _do_logout(self):
        """Perform logout"""
        api_client.logout()
        self._update_auth_state()
        self.auth_changed.emit(False)
    
    def _on_login_success(self, result: dict):
        """Handle successful login"""
        self.login_btn.setEnabled(True)
        self.login_password.clear()
        self.login_status.hide()
        self._update_auth_state()
        self.auth_changed.emit(True)
    
    def _on_login_error(self, error_msg: str):
        """Handle login error"""
        self.login_btn.setEnabled(True)
        self._show_login_status(error_msg, "error")
    
    def _on_register_success(self, result: dict):
        """Handle successful registration"""
        self.register_btn.setEnabled(True)
        self._show_register_status("Account created! You can now sign in.", "success")
        
        # Clear fields and switch to login
        self.reg_username.clear()
        self.reg_email.clear()
        self.reg_password.clear()
        self.reg_confirm.clear()
        
        # Switch to login after short delay
        self.stack.setCurrentIndex(0)
    
    def _on_register_error(self, error_msg: str):
        """Handle registration error"""
        self.register_btn.setEnabled(True)
        self._show_register_status(error_msg, "error")
    
    def _update_auth_state(self):
        """Update UI based on authentication state"""
        if api_client.is_logged_in:
            self.welcome_label.setText(f"Welcome, {api_client.username}!")
            self.user_label.setText(f"User ID: {api_client.user_id}")
            self.stack.setCurrentIndex(2)
        else:
            self.stack.setCurrentIndex(0)
    
    def _show_login_status(self, message: str, status_type: str):
        """Show login status message"""
        layout = self.login_status.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        alert = AlertCard(message, status_type)
        layout.addWidget(alert)
        self.login_status.show()
    
    def _show_register_status(self, message: str, status_type: str):
        """Show register status message"""
        layout = self.register_status.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        alert = AlertCard(message, status_type)
        layout.addWidget(alert)
        self.register_status.show()
