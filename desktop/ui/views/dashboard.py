"""
Dashboard View - Home screen with overview and quick actions
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGridLayout, QScrollArea, QFrame, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from ..components.cards import StatCard, InfoCard, AlertCard


class DashboardView(QWidget):
    """Main dashboard view showing overview and quick actions"""
    
    navigate_to = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)
        
        # Transparent labels for main view (card labels handled separately)
        content.setStyleSheet("QLabel { background-color: transparent; }")
        
        # Header
        header = QVBoxLayout()
        header.setSpacing(8)
        
        welcome = QLabel("Chemical Equipment Visualizer")
        welcome.setObjectName("heading")
        welcome.setFont(QFont("Source Sans 3", 26, QFont.Bold))
        
        subtitle = QLabel("Upload, analyze, and visualize chemical equipment data")
        subtitle.setObjectName("muted")
        subtitle.setFont(QFont("Source Sans 3", 14))
        
        header.addWidget(welcome)
        header.addWidget(subtitle)
        layout.addLayout(header)
        
        # Quick actions section
        actions_header = QLabel("Quick Actions")
        actions_header.setObjectName("subheading")
        actions_header.setFont(QFont("Source Sans 3", 16, QFont.DemiBold))
        layout.addWidget(actions_header)
        
        actions_row = QHBoxLayout()
        actions_row.setSpacing(12)
        
        # Upload action card
        upload_card = self._create_action_card(
            "📁", "Upload CSV", 
            "Upload a new dataset for analysis",
            "upload"
        )
        actions_row.addWidget(upload_card)
        
        # View data action
        data_card = self._create_action_card(
            "📊", "View Data",
            "Browse equipment data tables",
            "data"
        )
        actions_row.addWidget(data_card)
        
        # Charts action
        charts_card = self._create_action_card(
            "📈", "Visualize",
            "View charts and analytics",
            "charts"
        )
        actions_row.addWidget(charts_card)
        
        actions_row.addStretch()
        layout.addLayout(actions_row)
        
        # Statistics section
        stats_header = QLabel("Current Dataset Overview")
        stats_header.setObjectName("subheading")
        stats_header.setFont(QFont("Source Sans 3", 16, QFont.DemiBold))
        layout.addWidget(stats_header)
        
        # Stat cards grid
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(12)
        
        self.total_card = StatCard("Total Equip.", "—", "🔧")
        self.avg_flow_card = StatCard("Avg Flow", "—", "💧")
        self.avg_pressure_card = StatCard("Avg Pressure", "—", "⚡")
        self.avg_temp_card = StatCard("Avg Temp.", "—", "🌡️")
        
        stats_grid.addWidget(self.total_card)
        stats_grid.addWidget(self.avg_flow_card)
        stats_grid.addWidget(self.avg_pressure_card)
        stats_grid.addWidget(self.avg_temp_card)
        stats_grid.addStretch()
        
        layout.addLayout(stats_grid)
        
        # Info alert
        self.status_alert = AlertCard(
            "No dataset loaded. Upload a CSV file to get started.",
            "info"
        )
        layout.addWidget(self.status_alert)
        
        layout.addStretch()
        
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_action_card(self, icon: str, title: str, description: str, nav_key: str) -> QFrame:
        """Create clickable action card"""
        card = QFrame()
        card.setObjectName("card")
        card.setCursor(Qt.PointingHandCursor)
        card.setMinimumWidth(160)
        card.setMinimumHeight(110)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setStyleSheet("""
            QFrame#card {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 12px;
            }
            QFrame#card:hover {
                border-color: #00D9A5;
                background-color: #1F1F1F;
            }
            QLabel {
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Source Sans 3", 12, QFont.DemiBold))
        title_label.setStyleSheet("color: #FFFFFF;")
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Source Sans 3", 11))
        desc_label.setStyleSheet("color: #888888;")
        desc_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        # Make card clickable
        card.mousePressEvent = lambda e: self.navigate_to.emit(nav_key)
        
        return card
    
    def update_stats(self, summary: dict):
        """Update dashboard statistics from summary data"""
        self.total_card.set_value(str(summary.get('total_count', 0)))
        self.avg_flow_card.set_value(f"{summary.get('avg_flowrate', 0):.1f}")
        self.avg_pressure_card.set_value(f"{summary.get('avg_pressure', 0):.1f}")
        self.avg_temp_card.set_value(f"{summary.get('avg_temperature', 0):.1f}")
        
        # Update status alert
        self.status_alert.hide()
