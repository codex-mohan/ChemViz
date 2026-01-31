"""
History View - Display past uploaded datasets
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QListWidgetItem, QPushButton, QFrame,
    QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont
from ..components.cards import InfoCard, AlertCard
from api import api_client, ApiError


class HistoryLoadWorker(QObject):
    """Worker thread for loading history"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            result = api_client.get_history()
            self.finished.emit(result)
        except ApiError as e:
            self.error.emit(e.message)
        except Exception as e:
            self.error.emit(str(e))


class DatasetCard(QFrame):
    """Card representing a single dataset in history"""
    
    clicked = pyqtSignal(int)
    
    def __init__(self, dataset: dict, parent=None):
        super().__init__(parent)
        self.dataset_id = dataset.get('id')
        self.setObjectName("card")
        self.setCursor(Qt.PointingHandCursor)
        self._setup_ui(dataset)
    
    def _setup_ui(self, dataset: dict):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Icon
        icon = QLabel("📁")
        icon.setStyleSheet("font-size: 28px;")
        layout.addWidget(icon)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name = QLabel(dataset.get('name', 'Unnamed'))
        name.setFont(QFont("Source Sans 3", 14, QFont.DemiBold))
        name.setStyleSheet("color: #FFFFFF;")
        
        meta = QLabel(f"{dataset.get('row_count', 0)} records • {dataset.get('created_at', '')[:10]}")
        meta.setFont(QFont("Source Sans 3", 11))
        meta.setStyleSheet("color: #888888;")
        
        info_layout.addWidget(name)
        info_layout.addWidget(meta)
        layout.addLayout(info_layout, 1)
        
        # Arrow indicator
        arrow = QLabel("→")
        arrow.setStyleSheet("color: #00D9A5; font-size: 20px;")
        layout.addWidget(arrow)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.dataset_id)


class HistoryView(QWidget):
    """View for browsing uploaded dataset history"""
    
    dataset_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_thread = None
        self.load_worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(20)
        
        # Header
        header_row = QHBoxLayout()
        
        header = QLabel("Dataset History")
        header.setObjectName("heading")
        header.setFont(QFont("Source Sans 3", 24, QFont.Bold))
        header_row.addWidget(header)
        
        header_row.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄  Refresh")
        refresh_btn.clicked.connect(self.load_history)
        header_row.addWidget(refresh_btn)
        
        layout.addLayout(header_row)
        
        subtitle = QLabel("Last 5 uploaded datasets are stored")
        subtitle.setObjectName("muted")
        subtitle.setFont(QFont("Source Sans 3", 13))
        layout.addWidget(subtitle)
        
        # Scroll area for dataset list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(12)
        self.list_layout.addStretch()
        
        scroll.setWidget(self.list_container)
        layout.addWidget(scroll)
        
        # Loading indicator
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #888888; font-size: 14px;")
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        self.setStyleSheet("QLabel { background-color: transparent; }")
        
        # No data placeholder
        self.no_data_alert = AlertCard(
            "No datasets in history. Upload a CSV file to get started.",
            "info"
        )
        layout.addWidget(self.no_data_alert)
    
    def load_history(self):
        """Load dataset history from API"""
        self._clear_list()
        self.loading_label.show()
        self.no_data_alert.hide()
        
        self.load_thread = QThread()
        self.load_worker = HistoryLoadWorker()
        self.load_worker.moveToThread(self.load_thread)
        
        self.load_thread.started.connect(self.load_worker.run)
        self.load_worker.finished.connect(self._on_load_success)
        self.load_worker.error.connect(self._on_load_error)
        self.load_worker.finished.connect(self.load_thread.quit)
        self.load_worker.error.connect(self.load_thread.quit)
        
        self.load_thread.start()
    
    def _on_load_success(self, datasets: list):
        """Handle successful history load"""
        self.loading_label.hide()
        
        if not datasets:
            self.no_data_alert.show()
            return
        
        self.no_data_alert.hide()
        
        for dataset in datasets:
            card = DatasetCard(dataset)
            card.clicked.connect(self._on_dataset_clicked)
            # Insert before the stretch
            self.list_layout.insertWidget(self.list_layout.count() - 1, card)
    
    def _on_load_error(self, error_msg: str):
        """Handle history load error"""
        self.loading_label.hide()
        
        error_alert = AlertCard(f"Failed to load history: {error_msg}", "error")
        self.list_layout.insertWidget(0, error_alert)
    
    def _clear_list(self):
        """Clear the dataset list"""
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _on_dataset_clicked(self, dataset_id: int):
        """Handle dataset selection"""
        self.dataset_selected.emit(dataset_id)
