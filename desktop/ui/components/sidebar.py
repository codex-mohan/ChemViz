"""
Sidebar Navigation Component
"""
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpacerItem, QSizePolicy, QWidget
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class SidebarButton(QPushButton):
    """Custom navigation button for sidebar"""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("nav_button")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        
        # Set text with icon
        display_text = f"  {icon}   {text}" if icon else text
        self.setText(display_text)
        
        self.setMinimumHeight(48)
        self.setFont(QFont("Source Sans 3", 10))


class Sidebar(QFrame):
    """Application sidebar with navigation"""
    
    navigation_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.setMinimumHeight(600)
        
        self.buttons = {}
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(4)
        
        # Logo / App title
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(8, 0, 0, 20)
        
        logo_label = QLabel("⬡")
        logo_label.setStyleSheet("""
            font-size: 28px;
            color: #00D9A5;
        """)
        
        app_title = QLabel("ChemViz")
        app_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #FFFFFF;
            letter-spacing: 1px;
        """)
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(app_title)
        title_layout.addStretch()
        
        layout.addWidget(title_container)
        
        # Navigation buttons
        nav_items = [
            ("dashboard", "Dashboard", "🏠"),
            ("upload", "Upload CSV", "📁"),
            ("data", "Data View", "📊"),
            ("charts", "Charts", "📈"),
            ("history", "History", "📜"),
            ("report", "Reports", "📄"),
        ]
        
        for key, text, icon in nav_items:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda checked, k=key: self._on_nav_click(k))
            self.buttons[key] = btn
            layout.addWidget(btn)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Divider
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        
        # User section
        layout.addSpacing(12)
        
        user_btn = SidebarButton("Account", "👤")
        user_btn.clicked.connect(lambda: self._on_nav_click("auth"))
        self.buttons["auth"] = user_btn
        layout.addWidget(user_btn)
        
        # Set default selection
        self.buttons["dashboard"].setChecked(True)
    
    def _on_nav_click(self, key: str):
        # Uncheck all buttons
        for k, btn in self.buttons.items():
            btn.setChecked(k == key)
        
        self.navigation_changed.emit(key)
    
    def set_active(self, key: str):
        """Programmatically set active navigation item"""
        if key in self.buttons:
            for k, btn in self.buttons.items():
                btn.setChecked(k == key)
