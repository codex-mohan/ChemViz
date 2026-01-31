"""
CSV Upload View - File selection and upload interface
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
from ..components.cards import AlertCard
from api import api_client, ApiError


class UploadWorker(QObject):
    """Worker thread for file upload"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            result = api_client.upload_csv(self.file_path)
            self.finished.emit(result)
        except ApiError as e:
            self.error.emit(e.message)
        except Exception as e:
            self.error.emit(str(e))


class DropZone(QFrame):
    """Drag and drop zone for file upload"""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFixedSize(450, 180)
        self._setup_ui()
        self._set_normal_style()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        
        # Icon
        self.icon_label = QLabel("📁")
        self.icon_label.setStyleSheet("font-size: 48px;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        # Text
        self.main_text = QLabel("Drag & Drop CSV file here")
        self.main_text.setFont(QFont("Source Sans 3", 16, QFont.DemiBold))
        self.main_text.setStyleSheet("color: #E8E8E8;")
        self.main_text.setAlignment(Qt.AlignCenter)
        
        self.sub_text = QLabel("or click to browse")
        self.sub_text.setFont(QFont("Source Sans 3", 12))
        self.sub_text.setStyleSheet("color: #888888;")
        self.sub_text.setAlignment(Qt.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.main_text)
        layout.addWidget(self.sub_text)
        layout.addStretch()
        
        self.setCursor(Qt.PointingHandCursor)
    
    def _set_normal_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border: 2px dashed #444444;
                border-radius: 16px;
            }
        """)
    
    def _set_hover_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #1F1F1F;
                border: 2px dashed #00D9A5;
                border-radius: 16px;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith('.csv'):
                event.acceptProposedAction()
                self._set_hover_style()
                return
        event.ignore()
    
    def dragLeaveEvent(self, event):
        self._set_normal_style()
    
    def dropEvent(self, event: QDropEvent):
        self._set_normal_style()
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith('.csv'):
                self.file_dropped.emit(file_path)
    
    def mousePressEvent(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.file_dropped.emit(file_path)


class UploadView(QWidget):
    """View for uploading CSV files"""
    
    upload_complete = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.upload_thread = None
        self.upload_worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)
        
        # Transparent labels
        self.setStyleSheet("QLabel { background-color: transparent; }")
        
        # Header
        header = QLabel("Upload Dataset")
        header.setObjectName("heading")
        header.setFont(QFont("Source Sans 3", 24, QFont.Bold))
        layout.addWidget(header)
        
        subtitle = QLabel("Upload a CSV file containing chemical equipment data")
        subtitle.setObjectName("muted")
        subtitle.setFont(QFont("Source Sans 3", 13))
        layout.addWidget(subtitle)
        
        layout.addSpacing(8)
        
        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.file_dropped.connect(self._on_file_selected)
        layout.addWidget(self.drop_zone, 0, Qt.AlignCenter)
        
        # Selected file info
        self.file_info = QLabel("")
        self.file_info.setFont(QFont("JetBrains Mono", 12))
        self.file_info.setStyleSheet("color: #00D9A5;")
        self.file_info.setAlignment(Qt.AlignCenter)
        self.file_info.hide()
        layout.addWidget(self.file_info)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(0)  # Indeterminate
        self.progress.setFixedHeight(8)
        self.progress.hide()
        layout.addWidget(self.progress)
        
        # Upload button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.upload_btn = QPushButton("  Upload to Server  ")
        self.upload_btn.setObjectName("primary")
        self.upload_btn.setFont(QFont("Source Sans 3", 13, QFont.DemiBold))
        self.upload_btn.setMinimumSize(180, 48)
        self.upload_btn.clicked.connect(self._start_upload)
        self.upload_btn.setEnabled(False)
        
        btn_layout.addWidget(self.upload_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Status message
        self.status_container = QWidget()
        status_layout = QVBoxLayout(self.status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_container.hide()
        layout.addWidget(self.status_container)
        
        # Required format info
        format_info = AlertCard(
            "Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature",
            "info"
        )
        layout.addWidget(format_info)
        
        layout.addStretch()
        
        self.selected_file = None
    
    def reset_state(self):
        """Reset view state when navigating to it"""
        self.selected_file = None
        self.file_info.hide()
        self.progress.hide()
        self.upload_btn.setEnabled(False)
        self.status_container.hide()
        # Clear status container
        layout = self.status_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
    
    def _on_file_selected(self, file_path: str):
        """Handle file selection"""
        self.selected_file = file_path
        file_name = file_path.split('/')[-1].split('\\')[-1]
        self.file_info.setText(f"📄 {file_name}")
        self.file_info.show()
        self.upload_btn.setEnabled(True)
        self._show_status("File selected. Click 'Upload to Server' to proceed.", "info")
    
    def _start_upload(self):
        """Start file upload in background thread"""
        if not self.selected_file:
            return
        
        self.upload_btn.setEnabled(False)
        self.progress.show()
        self._show_status("Uploading...", "info")
        
        # Create worker and thread
        self.upload_thread = QThread()
        self.upload_worker = UploadWorker(self.selected_file)
        self.upload_worker.moveToThread(self.upload_thread)
        
        # Connect signals
        self.upload_thread.started.connect(self.upload_worker.run)
        self.upload_worker.finished.connect(self._on_upload_success)
        self.upload_worker.error.connect(self._on_upload_error)
        self.upload_worker.finished.connect(self.upload_thread.quit)
        self.upload_worker.error.connect(self.upload_thread.quit)
        
        self.upload_thread.start()
    
    def _on_upload_success(self, result: dict):
        """Handle successful upload"""
        self.progress.hide()
        self._show_status("✅ Upload successful! Dataset processed.", "success")
        self.selected_file = None
        self.file_info.hide()
        self.upload_complete.emit(result)
    
    def _on_upload_error(self, error_msg: str):
        """Handle upload error"""
        self.progress.hide()
        self.upload_btn.setEnabled(True)
        self._show_status(f"❌ Error: {error_msg}", "error")
    
    def _show_status(self, message: str, status_type: str):
        """Show status message"""
        # Clear previous status properly
        layout = self.status_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        alert = AlertCard(message, status_type)
        layout.addWidget(alert)
        self.status_container.show()
