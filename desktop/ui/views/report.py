"""
Report View - PDF report generation and download
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont
from ..components.cards import AlertCard
from api import api_client, ApiError


class ReportDownloadWorker(QObject):
    """Worker thread for downloading report"""
    finished = pyqtSignal(bytes, str)
    error = pyqtSignal(str)
    
    def __init__(self, dataset_id: int, dataset_name: str):
        super().__init__()
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
    
    def run(self):
        try:
            pdf_data = api_client.download_report(self.dataset_id)
            self.finished.emit(pdf_data, self.dataset_name)
        except ApiError as e:
            self.error.emit(e.message)
        except Exception as e:
            self.error.emit(str(e))


class DetailBox(QFrame):
    """Simple container with title and content"""
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Source Sans 3", 14, QFont.DemiBold))
        title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        layout.addWidget(title_label)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(8)
        layout.addLayout(self.content_layout)
        layout.addStretch()
        
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)


class ReportView(QWidget):
    """View for generating and downloading PDF reports"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_dataset_id = None
        self.current_dataset_name = None
        self.summary_data = {}
        self.download_thread = None
        self.download_worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header_container = QWidget()
        header_container.setStyleSheet("background-color: transparent;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header = QLabel("Generate Report")
        header.setObjectName("heading")
        header.setFont(QFont("Source Sans 3", 24, QFont.Bold))
        header.setStyleSheet("background-color: transparent;")
        
        subtitle = QLabel("Download a comprehensive PDF report of the current dataset")
        subtitle.setObjectName("muted")
        subtitle.setFont(QFont("Source Sans 3", 12))
        subtitle.setStyleSheet("background-color: transparent;")
        
        header_layout.addWidget(header)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_container)
        
        # Main Content Grid (Two Columns)
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(20)
        
        # Col 1: Current Dataset
        self.dataset_box = DetailBox("Current Dataset")
        self.dataset_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.dataset_name_label = QLabel("No dataset selected")
        self.dataset_name_label.setFont(QFont("Source Sans 3", 16, QFont.DemiBold))
        # Use simple text styling
        self.dataset_name_label.setStyleSheet("color: #00D9A5; background-color: transparent; border: none;")
        self.dataset_name_label.setWordWrap(True)
        
        self.dataset_info_label = QLabel("—")
        self.dataset_info_label.setStyleSheet("color: #888888; background-color: transparent; border: none; font-size: 12px;")
        
        self.dataset_box.add_widget(self.dataset_name_label)
        self.dataset_box.add_widget(self.dataset_info_label)
        
        grid_layout.addWidget(self.dataset_box)
        
        # Col 2: Report Contents
        self.preview_box = DetailBox("Report Includes")
        self.preview_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        contents = [
            "  •  Executive summary metrics",
            "  •  Statistical analysis",
            "  •  Detailed equipment tables",
            "  •  Distribution charts"
        ]
        
        for item in contents:
            lbl = QLabel(item)
            lbl.setStyleSheet("color: #CCCCCC; background-color: transparent; border: none; font-size: 12px;")
            self.preview_box.add_widget(lbl)
            
        grid_layout.addWidget(self.preview_box)
        
        layout.addLayout(grid_layout)
        
        # Download Action Area
        action_container = QWidget()
        action_container.setMinimumHeight(60)
        action_container.setStyleSheet("background-color: transparent;")
        action_layout = QHBoxLayout(action_container)
        action_layout.setContentsMargins(0, 0, 0, 0)
        
        self.download_btn = QPushButton("  Download PDF Report  ")
        self.download_btn.setObjectName("primary")
        self.download_btn.setFont(QFont("Source Sans 3", 13, QFont.DemiBold))
        self.download_btn.setMinimumSize(200, 48)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self._start_download)
        
        # Explicit styling to ensure visibility
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #00D9A5;
                color: #0D0D0D;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #00F5BA;
            }
            QPushButton:pressed {
                background-color: #00A87D;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #666666;
            }
        """)
        
        self.download_btn.setEnabled(False)
        
        action_layout.addStretch()
        action_layout.addWidget(self.download_btn)
        
        layout.addWidget(action_container)
        
        # Status & Alerts
        self.status_container = QWidget()
        self.status_container.setStyleSheet("background-color: transparent;")
        status_layout = QVBoxLayout(self.status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_container.hide()
        layout.addWidget(self.status_container)
        
        # No dataset alert
        self.no_data_alert = AlertCard(
            "Upload a dataset first to generate reports.",
            "info"
        )
        layout.addWidget(self.no_data_alert)
        
        layout.addStretch()
        
    def set_dataset(self, dataset_id: int, dataset_name: str, summary: dict):
        """Set current dataset for report generation"""
        self.current_dataset_id = dataset_id
        self.current_dataset_name = dataset_name
        self.summary_data = summary
        
        self.dataset_name_label.setText(dataset_name)
        count = summary.get('total_count', 0)
        self.dataset_info_label.setText(f"{count} equipment records found")
        
        self.download_btn.setEnabled(True)
        self.no_data_alert.hide()
    
    def _start_download(self):
        """Start PDF download"""
        if not self.current_dataset_id:
            return
        
        self.download_btn.setEnabled(False)
        self._show_status("Generating report...", "info")
        
        self.download_thread = QThread()
        self.download_worker = ReportDownloadWorker(
            self.current_dataset_id, 
            self.current_dataset_name
        )
        self.download_worker.moveToThread(self.download_thread)
        
        self.download_thread.started.connect(self.download_worker.run)
        self.download_worker.finished.connect(self._on_download_success)
        self.download_worker.error.connect(self._on_download_error)
        self.download_worker.finished.connect(self.download_thread.quit)
        self.download_worker.error.connect(self.download_thread.quit)
        
        self.download_thread.start()
    
    def _on_download_success(self, pdf_data: bytes, dataset_name: str):
        """Handle successful download"""
        self.download_btn.setEnabled(True)
        
        # Open save dialog
        default_name = f"{dataset_name.replace('.csv', '')}_report.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", default_name, "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    f.write(pdf_data)
                self._show_status(f"✅ Report saved to {file_path}", "success")
            except Exception as e:
                self._show_status(f"❌ Failed to save: {str(e)}", "error")
        else:
            self._show_status("Download cancelled", "info")
    
    def _on_download_error(self, error_msg: str):
        """Handle download error"""
        self.download_btn.setEnabled(True)
        self._show_status(f"❌ Error: {error_msg}", "error")
    
    def _show_status(self, message: str, status_type: str):
        """Show status message"""
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
