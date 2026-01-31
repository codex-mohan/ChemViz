"""
Reusable Card Components
"""
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QGraphicsDropShadowEffect, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


class StatCard(QFrame):
    """Statistics display card with value and label"""
    
    def __init__(self, label: str, value: str = "0", icon: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self._setup_ui(label, value, icon)
        self._add_shadow()
    
    def _setup_ui(self, label: str, value: str, icon: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)
        
        # Header with icon
        header = QHBoxLayout()
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 14px;")
            header.addWidget(icon_label)
        
        label_widget = QLabel(label.upper())
        label_widget.setObjectName("stat_label")
        label_widget.setStyleSheet("background-color: transparent;")
        label_widget.setFont(QFont("Source Sans 3", 8))
        header.addWidget(label_widget)
        header.addStretch()
        
        layout.addLayout(header)
        layout.addStretch()
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setObjectName("stat_value")
        self.value_label.setStyleSheet("background-color: transparent;")
        self.value_label.setFont(QFont("JetBrains Mono", 20, QFont.Bold))
        layout.addWidget(self.value_label)
    
    def _add_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
    
    def set_value(self, value: str):
        """Update the displayed value"""
        self.value_label.setText(value)


class InfoCard(QFrame):
    """Information card with title and content"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 10, 12, 10)
        self.main_layout.setSpacing(8)
        
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("subheading")
            title_label.setStyleSheet("background-color: transparent;")
            title_label.setFont(QFont("Source Sans 3", 14, QFont.DemiBold))
            self.main_layout.addWidget(title_label)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(8)
        self.main_layout.addLayout(self.content_layout)
        
        self._add_shadow()
    
    def _add_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
    
    def add_widget(self, widget: QWidget):
        """Add widget to card content"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add layout to card content"""
        self.content_layout.addLayout(layout)


class AlertCard(QFrame):
    """Alert/notification card with colored accent"""
    
    TYPES = {
        'info': '#00D9A5',
        'warning': '#FF6B35',
        'error': '#FF4757',
        'success': '#00D9A5',
    }
    
    def __init__(self, message: str, alert_type: str = "info", parent=None):
        super().__init__(parent)
        
        color = self.TYPES.get(alert_type, self.TYPES['info'])
        
        # Simple clean background style
        self.setStyleSheet(f"""
            AlertCard {{
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 6px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)
        
        icon_map = {'info': 'ℹ️', 'warning': '⚠️', 'error': '❌', 'success': '✅'}
        icon = QLabel(icon_map.get(alert_type, 'ℹ️'))
        icon.setStyleSheet("font-size: 14px;")
        icon.setFixedWidth(24)
        
        msg = QLabel(message)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        
        layout.addWidget(icon)
        layout.addWidget(msg, 1)
