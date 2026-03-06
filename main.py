import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.main_window import MainWindow
from pathlib import Path

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()