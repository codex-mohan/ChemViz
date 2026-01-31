"""
Main Application Window
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QStatusBar, QLabel, QMessageBox, QSizeGrip
)
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont

from .components import Sidebar, TitleBar
from .views import (
    DashboardView, UploadView, DataTableView, 
    ChartsView, HistoryView, ReportView, AuthView
)
from api import api_client, ApiError


class DataLoadWorker(QObject):
    """Worker for loading dataset data"""
    finished = pyqtSignal(dict, list)
    error = pyqtSignal(str)
    
    def __init__(self, dataset_id: int):
        super().__init__()
        self.dataset_id = dataset_id
    
    def run(self):
        try:
            summary = api_client.get_summary(self.dataset_id)
            equipment = api_client.get_equipment(self.dataset_id)
            self.finished.emit(summary, equipment)
        except ApiError as e:
            self.error.emit(e.message)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation"""
    
    def __init__(self):
        super().__init__()
        self.current_dataset_id = None
        self.current_dataset_name = None
        self.load_thread = None
        self.load_worker = None
        
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
    
    def _setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("ChemViz - Chemical Equipment Visualizer")
        self.setMinimumSize(750, 500)
        self.resize(900, 550)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Center on screen
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def _setup_ui(self):
        """Set up the main UI layout"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        
        # Main vertical layout (TitleBar + Content)
        window_layout = QVBoxLayout(central)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        
        # Title Bar
        self.title_bar = TitleBar(self)
        window_layout.addWidget(self.title_bar)
        
        # Content horizontal layout
        content_wrapper = QWidget()
        main_layout = QHBoxLayout(content_wrapper)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        window_layout.addWidget(content_wrapper, 1)
        
        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Content area
        content_container = QWidget()
        content_container.setStyleSheet("background-color: #0D0D0D;")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for views
        self.stack = QStackedWidget()
        
        # Create views
        self.dashboard_view = DashboardView()
        self.upload_view = UploadView()
        self.data_view = DataTableView()
        self.charts_view = ChartsView()
        self.history_view = HistoryView()
        self.report_view = ReportView()
        self.auth_view = AuthView()
        
        # Add views to stack
        self.stack.addWidget(self.dashboard_view)  # 0
        self.stack.addWidget(self.upload_view)     # 1
        self.stack.addWidget(self.data_view)       # 2
        self.stack.addWidget(self.charts_view)     # 3
        self.stack.addWidget(self.history_view)    # 4
        self.stack.addWidget(self.report_view)     # 5
        self.stack.addWidget(self.auth_view)       # 6
        
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_container, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.connection_label = QLabel("⚪ Checking server...")
        self.status_bar.addPermanentWidget(self.connection_label)
        
        # Size Grip for resizing
        self.size_grip = QSizeGrip(self)
        self.status_bar.addPermanentWidget(self.size_grip)
        
        # Check server connection
        self._check_server_connection()
        
        # Set initial view based on auth state
        if api_client.is_logged_in:
            self.sidebar.set_active('dashboard')
            self.stack.setCurrentIndex(0)
        else:
            self.sidebar.set_active('') # No active sidebar item
            self.stack.setCurrentIndex(6) # Auth view
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Sidebar navigation
        self.sidebar.navigation_changed.connect(self._on_navigation)
        
        # Dashboard quick actions
        self.dashboard_view.navigate_to.connect(self._navigate_to)
        
        # Upload complete
        self.upload_view.upload_complete.connect(self._on_upload_complete)
        
        # History selection
        self.history_view.dataset_selected.connect(self._on_dataset_selected)
        
        # Auth changes
        self.auth_view.auth_changed.connect(self._on_auth_changed)
    
    def _on_navigation(self, key: str):
        """Handle navigation changes"""
        index_map = {
            'dashboard': 0,
            'upload': 1,
            'data': 2,
            'charts': 3,
            'history': 4,
            'report': 5,
            'auth': 6,
        }
        
        index = index_map.get(key, 0)
        self.stack.setCurrentIndex(index)
        
        # Reset view states when navigating
        if key == 'history':
            self.history_view.load_history()
        elif key == 'upload':
            self.upload_view.reset_state()
    
    def _navigate_to(self, key: str):
        """Navigate to a specific view"""
        self.sidebar.set_active(key)
        self._on_navigation(key)
    
    def _on_upload_complete(self, result: dict):
        """Handle successful upload"""
        dataset_id = result.get('id')
        dataset_name = result.get('name', 'Unnamed')
        
        self.current_dataset_id = dataset_id
        self.current_dataset_name = dataset_name
        
        # Load the new dataset
        self._load_dataset(dataset_id)
        
        # Update status
        self.status_bar.showMessage(f"Loaded: {dataset_name}", 5000)
    
    def _on_dataset_selected(self, dataset_id: int):
        """Handle dataset selection from history"""
        self.current_dataset_id = dataset_id
        self._load_dataset(dataset_id)
        
        # Navigate to dashboard
        self._navigate_to('dashboard')
    
    def _load_dataset(self, dataset_id: int):
        """Load dataset data from API"""
        self.load_thread = QThread()
        self.load_worker = DataLoadWorker(dataset_id)
        self.load_worker.moveToThread(self.load_thread)
        
        self.load_thread.started.connect(self.load_worker.run)
        self.load_worker.finished.connect(self._on_data_loaded)
        self.load_worker.error.connect(self._on_data_load_error)
        self.load_worker.finished.connect(self.load_thread.quit)
        self.load_worker.error.connect(self.load_thread.quit)
        
        self.load_thread.start()
    
    def _on_data_loaded(self, summary: dict, equipment: list):
        """Handle loaded data"""
        # Get dataset info
        try:
            dataset = api_client.get_dataset(self.current_dataset_id)
            self.current_dataset_name = dataset.get('name', 'Unnamed')
        except:
            pass
        
        # Update all views with data
        self.dashboard_view.update_stats(summary)
        self.data_view.set_data(equipment)
        self.charts_view.set_data(summary, equipment)
        self.report_view.set_dataset(
            self.current_dataset_id, 
            self.current_dataset_name, 
            summary
        )
        
        self.status_bar.showMessage(
            f"Dataset loaded: {self.current_dataset_name} ({summary.get('total_count', 0)} records)", 
            5000
        )
    
    def _on_data_load_error(self, error_msg: str):
        """Handle data load error"""
        self.status_bar.showMessage(f"Error loading data: {error_msg}", 5000)
    
    def _on_auth_changed(self, is_logged_in: bool):
        """Handle authentication state change"""
        if is_logged_in:
            self.status_bar.showMessage(f"Logged in as {api_client.username}", 3000)
            self._navigate_to('dashboard')
        else:
            self.status_bar.showMessage("Logged out", 3000)
            self._navigate_to('auth')
    
    def _check_server_connection(self):
        """Check if backend server is reachable"""
        try:
            # Try to get history as a simple health check
            api_client.get_history()
            self.connection_label.setText("🟢 Server Connected")
            self.connection_label.setStyleSheet("color: #00D9A5;")
        except ApiError as e:
            if e.status_code == 401:
                # 401 means server is up but we are not authenticated
                self.connection_label.setText("🟢 Server Connected")
                self.connection_label.setStyleSheet("color: #00D9A5;")
                return
            self.connection_label.setText("🔴 Server Status Error")
            self.connection_label.setStyleSheet("color: #FF4757;")
        except Exception:
            self.connection_label.setText("🔴 Server Offline")
            self.connection_label.setStyleSheet("color: #FF4757;")
