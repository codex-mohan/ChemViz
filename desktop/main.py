"""
Chemical Equipment Parameter Visualizer - PyQt5 Desktop Application
Main entry point
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from ui.styles import MAIN_STYLESHEET


def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    
    # Load custom fonts
    font_db = QFontDatabase()
    font_db.addApplicationFont("resources/fonts/SourceSans3-Regular.ttf")
    font_db.addApplicationFont("resources/fonts/SourceSans3-SemiBold.ttf")
    font_db.addApplicationFont("resources/fonts/SourceSans3-Bold.ttf")
    font_db.addApplicationFont("resources/fonts/JetBrainsMono-Regular.ttf")
    
    # Set default font
    app.setFont(QFont("Source Sans 3", 11))
    
    # Apply stylesheet
    app.setStyleSheet(MAIN_STYLESHEET)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
