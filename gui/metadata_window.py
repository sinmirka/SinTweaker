from pathlib import Path

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMessageBox

class MetadataWindow(): # god help this code work
    def __init__(self, text: str, parent=None):
        loader = QUiLoader()

        ui_path = Path(__file__).parent / "ui_files" / "metadata_win.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QFile.ReadOnly)

        self.dialog = loader.load(ui_file, parent)
        ui_file.close()

        if self.dialog is None:
            raise RuntimeError("Failed to load metadata_win.ui")

        self.dialog.textMetadata.setPlainText(text)

        self._connect_signals()

    def _connect_signals(self):
        self.dialog.btnClose.clicked.connect(self.dialog.close)
        self.dialog.btnCopy.clicked.connect(self._copy_to_clipboard)

        # these are not working for now 04.02.2026
        # logic will be connected soon 
        self.dialog.btnExport.clicked.connect(self._export_metadata)
        self.dialog.btnSelectiveClean.clicked.connect(self._selective_clean)
        self.dialog.btnRefresh.clicked.connect(self._refresh_metadata)

    def _copy_to_clipboard(self):
        metadata = self.dialog.textMetadata
        if metadata.toPlainText() == "No metadata found.":
            return
        QApplication.clipboard().setText(f"{self.dialog.textMetadata.toPlainText()}") #i found this fucking method on stackoverflow 16 YEARS old question

    def _export_metadata(self): #TODO: implement these 3 features
        pass

    def _selective_clean(self):
        pass

    def _refresh_metadata(self):
        pass

    def exec(self):
        self.dialog.exec()