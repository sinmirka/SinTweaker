from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from core.rename import rename_file
from core.meta.meta_handler import get_metadata, clear_metadata
from core.info import get_file_info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file: Path | None = None

        self._load_ui()
        self._connect_signals()

        self.setFixedSize(self.size())
    
    def _load_ui(self):
        loader = QUiLoader()

        ui_path = Path(__file__).parent / "sincleaner.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QFile.ReadOnly)

        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(self.ui.centralWidget())
        self.setWindowTitle(self.ui.windowTitle())


    def _connect_signals(self):
        # File tab
        self.ui.btnSelectFile.clicked.connect(self.choose_file)
        self.ui.btnRenameFile.clicked.connect(self.rename_file)

        # Metadata tab
        self.ui.btnClearMetadata.clicked.connect(self.clear_file_metadata)
        # self.ui.btnOpenMetadataFull.clicked.connect(self.open_metadata_full) ill make ts work soon cuz it pmo so harddddddd


    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose file",
            "",
            "All files (*.*)",
        )

        if not file_path:
            return
        
        self.current_file = Path(file_path)
        self.ui.labelCurrentFile.setText(file_path)
        self.update_metadata_view()
        self.show_file_info()

    def rename_file(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected")
            return
        
        try:
            report = rename_file(self.current_file)
        except Exception as e:
            QMessageBox.critical(self, "Rename failed", str(e))
            return
        
        self.ui.textInfo.setPlainText("\n".join(report))

    def update_metadata_view(self):
        if not self.current_file:
            self.ui.textMetadata.clear()
            return
        
        metadata = get_metadata(self.current_file)

        if not metadata:
            self.ui.textMetadata.setPlainText(
                "Metadata is not supported for this file type\n"
                "or no metadata found."
            )
            return
    
        lines: list[str] = []

        for section, data in metadata.items():
            if section == "thumbnail":
                lines.append(f"{section}: {len(data)} bytes")
            else:
                lines.append(f"{section}: {len(data)} tags")

        self.ui.textMetadata.setPlainText("\n".join(lines))

    def clear_file_metadata(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return
        
        try:
            report = clear_metadata(self.current_file)
        except Exception as e:
            QMessageBox.critical(self, "Clear failed", str(e))
        
        self.ui.textMetadata.setPlainText("\n".join(report))
        self.update_metadata_view()

    def show_file_info(self):
        if not self.current_file:
            self.ui.textInfo.setPlainText("No file selected or file info is unavailable.")
            return
        
        try:
            info = get_file_info(self.current_file)
        except Exception as e:
            QMessageBox.critical(self, "get_file_info() failed", str(e))
            return

        lines = [
                    f"Name: {info.name}",
                    f"Extension: {info.extension}",
                    f"Size: {info.size_human()}",
                    f"Created: {info.created_at}",
                    f"Modified: {info.modified_at}",
                ]

        self.ui.textInfo.setPlainText("\n".join(lines))