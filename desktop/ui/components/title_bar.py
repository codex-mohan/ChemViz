"""
Custom Title Bar Component
"""
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, 
    QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QPoint

class TitleBar(QFrame):
    """Custom title bar for the application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("title_bar")
        self.setFixedHeight(32)
        self.setStyleSheet("""
            QFrame#title_bar {
                background-color: #0B0B0B;
                border-bottom: 1px solid #252525;
            }
            QLabel {
                color: #AAAAAA;
                font-family: "Source Sans 3";
                font-size: 13px;
                background-color: transparent;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                color: #AAAAAA;
                font-size: 13px;
                max-width: 32px;
                max-height: 32px;
                min-width: 32px;
                min-height: 32px;
                margin: 0px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #252525;
                color: #FFFFFF;
            }
            QPushButton#close_btn:hover {
                background-color: #E81123;
                color: #FFFFFF;
            }
        """)
        
        self.clicking = False
        self.click_pos = QPoint()
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)
        
        # Icon
        icon_label = QLabel("⬡")
        icon_label.setStyleSheet("color: #00D9A5; font-size: 16px; margin-right: 8px;")
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel("ChemViz")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Window controls
        self.min_btn = QPushButton("─")
        self.min_btn.setFixedSize(32, 32)
        self.min_btn.clicked.connect(self._minimize_window)
        layout.addWidget(self.min_btn)
        
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(32, 32)
        self.max_btn.clicked.connect(self._maximize_window)
        layout.addWidget(self.max_btn)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.clicked.connect(self._close_window)
        layout.addWidget(self.close_btn)
        
    def _minimize_window(self):
        if self.window():
            self.window().showMinimized()
            
    def _maximize_window(self):
        if self.window():
            if self.window().isMaximized():
                self.window().showNormal()
                self.max_btn.setText("□")
            else:
                self.window().showMaximized()
                self.max_btn.setText("❐")
                
    def _close_window(self):
        if self.window():
            self.window().close()
            
    # Window dragging logic
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicking = True
            self.click_pos = event.globalPos() - self.window().pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.clicking and event.buttons() & Qt.LeftButton:
            if self.window().isMaximized():
                # Handling dragging from maximized state is complex, skipping for simplicity
                # Or we can just restore and move
                pass 
            else:
                self.window().move(event.globalPos() - self.click_pos)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        self.clicking = False
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._maximize_window()
