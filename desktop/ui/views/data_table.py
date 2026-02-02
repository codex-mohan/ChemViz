"""
Data Table View - Display equipment data in a table format
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QComboBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from ..components.cards import AlertCard


class DataTableView(QWidget):
    """View for displaying equipment data in table format"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.equipment_data = []
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(20)
        
        # Header row
        header_row = QHBoxLayout()
        
        header = QLabel("Equipment Data")
        header.setObjectName("heading")
        header.setFont(QFont("Source Sans 3", 20, QFont.Bold))
        header_row.addWidget(header)
        
        header_row.addStretch()
        
        # Record count
        self.count_label = QLabel("0 records")
        self.count_label.setStyleSheet("color: #888888; font-size: 14px;")
        header_row.addWidget(self.count_label)
        
        layout.addLayout(header_row)
        
        # Transparent labels style
        self.setStyleSheet("QLabel { background-color: transparent; }")
        
        # Filter row
        filter_row = QHBoxLayout()
        filter_row.setSpacing(16)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search by name or type...")
        self.search_input.setMinimumWidth(350)
        self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search_input.textChanged.connect(self._filter_data)
        filter_row.addWidget(self.search_input, 1)
        
        # Type filter
        filter_label = QLabel("Filter by Type:")
        filter_label.setStyleSheet("color: #888888;")
        filter_row.addWidget(filter_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.setMinimumWidth(150)
        self.type_filter.currentTextChanged.connect(self._filter_data)
        filter_row.addWidget(self.type_filter)
        
        filter_row.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄  Refresh")
        refresh_btn.clicked.connect(lambda: self.refresh_requested.emit() if hasattr(self, 'refresh_requested') else None)
        filter_row.addWidget(refresh_btn)
        
        layout.addLayout(filter_row)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        # Configure header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # No data placeholder
        self.no_data_alert = AlertCard(
            "No equipment data available. Upload a CSV file to view data.",
            "info"
        )
        layout.addWidget(self.no_data_alert)
    
    def set_data(self, equipment_list: list):
        """Set table data from equipment list"""
        self.equipment_data = equipment_list
        self._populate_table(equipment_list)
        self._update_type_filter(equipment_list)
        
        # Show/hide elements based on data
        has_data = len(equipment_list) > 0
        self.table.setVisible(has_data)
        self.no_data_alert.setVisible(not has_data)
        self.count_label.setText(f"{len(equipment_list)} records")
    
    def _populate_table(self, data: list):
        """Populate table with data"""
        self.table.setRowCount(len(data))
        
        for row, equipment in enumerate(data):
            name_item = QTableWidgetItem(equipment.get('equipment_name', ''))
            type_item = QTableWidgetItem(equipment.get('equipment_type', ''))
            
            flowrate = equipment.get('flowrate', 0)
            pressure = equipment.get('pressure', 0)
            temperature = equipment.get('temperature', 0)
            
            flow_item = QTableWidgetItem(f"{flowrate:.2f}")
            flow_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            flow_item.setFont(QFont("JetBrains Mono", 11))
            
            pres_item = QTableWidgetItem(f"{pressure:.2f}")
            pres_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            pres_item.setFont(QFont("JetBrains Mono", 11))
            
            temp_item = QTableWidgetItem(f"{temperature:.2f}")
            temp_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            temp_item.setFont(QFont("JetBrains Mono", 11))
            
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, type_item)
            self.table.setItem(row, 2, flow_item)
            self.table.setItem(row, 3, pres_item)
            self.table.setItem(row, 4, temp_item)
    
    def _update_type_filter(self, data: list):
        """Update type filter dropdown with available types"""
        current = self.type_filter.currentText()
        self.type_filter.clear()
        self.type_filter.addItem("All Types")
        
        types = sorted(set(eq.get('equipment_type', '') for eq in data))
        for t in types:
            if t:
                self.type_filter.addItem(t)
        
        # Restore selection if possible
        idx = self.type_filter.findText(current)
        if idx >= 0:
            self.type_filter.setCurrentIndex(idx)
    
    def _filter_data(self):
        """Filter table based on search and type filter"""
        search_text = self.search_input.text().lower()
        selected_type = self.type_filter.currentText()
        
        filtered = []
        for eq in self.equipment_data:
            name = eq.get('equipment_name', '').lower()
            eq_type = eq.get('equipment_type', '')
            
            # Search filter
            if search_text and search_text not in name and search_text not in eq_type.lower():
                continue
            
            # Type filter
            if selected_type != "All Types" and eq_type != selected_type:
                continue
            
            filtered.append(eq)
        
        self._populate_table(filtered)
        self.count_label.setText(f"{len(filtered)} of {len(self.equipment_data)} records")
