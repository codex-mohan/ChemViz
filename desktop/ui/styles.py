"""
QSS Stylesheet Definitions for Dark Theme
"""

# Color Palette
COLORS = {
    'bg_primary': '#0D0D0D',
    'bg_secondary': '#1A1A1A', 
    'bg_tertiary': '#252525',
    'bg_hover': '#2D2D2D',
    'accent': '#00D9A5',
    'accent_hover': '#00F5BA',
    'accent_dim': '#00A87D',
    'warning': '#FF6B35',
    'error': '#FF4757',
    'success': '#00D9A5',
    'text_primary': '#E8E8E8',
    'text_secondary': '#888888',
    'text_muted': '#555555',
    'border': '#333333',
    'border_light': '#444444',
}

MAIN_STYLESHEET = """
/* ============ Global ============ */
QMainWindow {
    background-color: #0D0D0D;
}

QWidget {
    background-color: transparent;
    color: #E8E8E8;
    font-family: "Source Sans 3", "Segoe UI", sans-serif;
    font-size: 12px;
}

/* ============ Scroll Areas ============ */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #1A1A1A;
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background-color: #444444;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00D9A5;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1A1A1A;
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background-color: #444444;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #00D9A5;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ============ Labels ============ */
QLabel {
    color: #E8E8E8;
    background-color: transparent;
}

QLabel#heading {
    font-size: 18px;
    font-weight: 600;
    color: #FFFFFF;
    padding: 6px 0;
}

QLabel#subheading {
    font-size: 15px;
    font-weight: 500;
    color: #CCCCCC;
}

QLabel#muted {
    color: #888888;
    font-size: 12px;
}

QLabel#stat_value {
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 24px;
    font-weight: 600;
    color: #00D9A5;
}

QLabel#stat_label {
    font-size: 12px;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ============ Buttons ============ */
QPushButton {
    background-color: #252525;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2D2D2D;
    border-color: #444444;
}

QPushButton:pressed {
    background-color: #1A1A1A;
}

QPushButton:disabled {
    background-color: #1A1A1A;
    color: #555555;
    border-color: #252525;
}

QPushButton#primary {
    background-color: #00D9A5;
    color: #0D0D0D;
    border: none;
    font-weight: 600;
}

QPushButton#primary:hover {
    background-color: #00F5BA;
}

QPushButton#primary:pressed {
    background-color: #00A87D;
}

QPushButton#primary:disabled {
    background-color: #333333;
    color: #666666;
}

QPushButton#danger {
    background-color: #FF4757;
    color: #FFFFFF;
    border: none;
}

QPushButton#danger:hover {
    background-color: #FF6B7A;
}

QPushButton#nav_button {
    background-color: transparent;
    border: none;
    border-radius: 10px;
    padding: 14px 18px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#nav_button:hover {
    background-color: #252525;
}

QPushButton#nav_button:checked {
    background-color: #00D9A5;
    color: #0D0D0D;
    font-weight: 600;
}

/* ============ Line Edits ============ */
QLineEdit {
    background-color: #1A1A1A;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    selection-background-color: #00D9A5;
    selection-color: #0D0D0D;
}

QLineEdit:focus {
    border-color: #00D9A5;
    background-color: #252525;
}

QLineEdit:disabled {
    background-color: #151515;
    color: #555555;
}

QLineEdit::placeholder {
    color: #666666;
}

/* ============ Text Edit ============ */
QTextEdit, QPlainTextEdit {
    background-color: #1A1A1A;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 12px;
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 12px;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #00D9A5;
}

/* ============ Combo Box ============ */
QComboBox {
    background-color: #1A1A1A;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 13px;
}

QComboBox:hover {
    border-color: #444444;
}

QComboBox:focus {
    border-color: #00D9A5;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #888888;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #1A1A1A;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    selection-background-color: #00D9A5;
    selection-color: #0D0D0D;
    padding: 4px;
}

/* ============ Tables ============ */
QTableWidget, QTableView {
    background-color: #1A1A1A;
    alternate-background-color: #1F1F1F;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    gridline-color: #2A2A2A;
    selection-background-color: #00D9A5;
    selection-color: #0D0D0D;
}

QTableWidget::item, QTableView::item {
    padding: 8px 12px;
    border: none;
}

QTableWidget::item:hover, QTableView::item:hover {
    background-color: #2D2D2D;
}

QTableWidget::item:selected, QTableView::item:selected {
    background-color: #00D9A5;
    color: #0D0D0D;
}

QHeaderView::section {
    background-color: #252525;
    color: #AAAAAA;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 12px 16px;
    border: none;
    border-bottom: 2px solid #333333;
}

QHeaderView::section:hover {
    background-color: #2D2D2D;
    color: #E8E8E8;
}

/* ============ Progress Bar ============ */
QProgressBar {
    background-color: #1A1A1A;
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
    font-size: 10px;
    color: #888888;
}

QProgressBar::chunk {
    background-color: #00D9A5;
    border-radius: 6px;
}

/* ============ Frames & Cards ============ */
QFrame#card {
    background-color: #1A1A1A;
    border: 1px solid #333333;
    border-radius: 12px;
    padding: 20px;
}

QFrame#card:hover {
    border-color: #444444;
}

QFrame#sidebar {
    background-color: #151515;
    border-right: 1px solid #252525;
}

QFrame#divider {
    background-color: #333333;
    max-height: 1px;
    min-height: 1px;
}

/* ============ Tool Tips ============ */
QToolTip {
    background-color: #252525;
    color: #E8E8E8;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
}

/* ============ Message Box ============ */
QMessageBox {
    background-color: #1A1A1A;
}

QMessageBox QLabel {
    color: #E8E8E8;
    font-size: 13px;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 16px;
}

/* ============ File Dialog ============ */
QFileDialog {
    background-color: #1A1A1A;
}

/* ============ Tab Widget ============ */
QTabWidget::pane {
    background-color: #1A1A1A;
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: -1px;
}

QTabBar::tab {
    background-color: #1A1A1A;
    color: #888888;
    border: 1px solid #333333;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 20px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #252525;
    color: #E8E8E8;
    border-color: #00D9A5;
}

QTabBar::tab:hover:!selected {
    background-color: #212121;
}

/* ============ Group Box ============ */
QGroupBox {
    background-color: #1A1A1A;
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #AAAAAA;
    background-color: #1A1A1A;
}

/* ============ Spin Box ============ */
QSpinBox, QDoubleSpinBox {
    background-color: #1A1A1A;
    color: #E8E8E8;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 8px 12px;
    font-family: "JetBrains Mono", monospace;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #00D9A5;
}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background-color: #252525;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #333333;
}

/* ============ Check Box ============ */
QCheckBox {
    color: #E8E8E8;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #444444;
    border-radius: 4px;
    background-color: #1A1A1A;
}

QCheckBox::indicator:hover {
    border-color: #00D9A5;
}

QCheckBox::indicator:checked {
    background-color: #00D9A5;
    border-color: #00D9A5;
}

/* ============ Radio Button ============ */
QRadioButton {
    color: #E8E8E8;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #444444;
    border-radius: 9px;
    background-color: #1A1A1A;
}

QRadioButton::indicator:hover {
    border-color: #00D9A5;
}

QRadioButton::indicator:checked {
    background-color: #00D9A5;
    border-color: #00D9A5;
}

/* ============ Slider ============ */
QSlider::groove:horizontal {
    background-color: #333333;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #00D9A5;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background-color: #00F5BA;
}

QSlider::sub-page:horizontal {
    background-color: #00D9A5;
    border-radius: 3px;
}

/* ============ Status Bar ============ */
QStatusBar {
    background-color: #151515;
    color: #888888;
    border-top: 1px solid #252525;
    padding: 4px 12px;
    font-size: 11px;
}

QStatusBar::item {
    border: none;
}
"""
