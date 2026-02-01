import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from pathlib import Path

very_important_file = Path(__file__).parent / "gui" / "very_important_file.jpg" #fucking never delete it

def main():
    if not very_important_file.exists():
        return
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
