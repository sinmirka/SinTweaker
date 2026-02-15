from pathlib import Path

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMessageBox

from core.meta.export import export_data

class MetadataWindow():
    def __init__(self, text: str, current_file: Path, parent=None):
        loader = QUiLoader()

        ui_path = Path(__file__).parent / "ui_files" / "metadata_win.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QFile.ReadOnly)

        self.dialog = loader.load(ui_file, parent)
        ui_file.close()

        self.current_file = current_file

        if self.dialog is None:
            raise RuntimeError("Failed to load metadata_win.ui")

        self.dialog.textMetadata.setPlainText(text)

        self._connect_signals()

    def _connect_signals(self):
        self.dialog.btnClose.clicked.connect(self.dialog.close)
        self.dialog.btnCopy.clicked.connect(self._copy_to_clipboard)
        self.dialog.btnExport.clicked.connect(self._export_metadata)
        self.dialog.btnSelectiveClean.clicked.connect(self._selective_clean) # I promise i will do it... one day i will wake up... and do this...
        self.dialog.btnRefresh.clicked.connect(self._refresh_metadata)

    def _copy_to_clipboard(self):
        metadata = self.dialog.textMetadata
        if metadata.toPlainText() == "No metadata found.":
            QMessageBox.warning(self.dialog, "Error", "No metadata to copy!")
            return
        QApplication.clipboard().setText(f"{self.dialog.textMetadata.toPlainText()}") #i found this fucking method on stack overflow 16 YEARS old question

    def _export_metadata(self):
        metadata = self.dialog.textMetadata.toPlainText()
        if metadata == "No metadata found.":
            QMessageBox.warning(self.dialog, "Error", "No metadata to export!")
            return
        name = self.current_file.stem
        export_data(name, metadata)

    def _selective_clean(self): #TODO: make ts
        pass

    def _refresh_metadata(self): #does this even work?
        from core.meta.formatter import format_metadata
        from core.meta.meta_handler import get_metadata

        meta = get_metadata(self.current_file)
        text = format_metadata(meta=meta)

        self.dialog.textMetadata.setPlainText(text) #it did work tho

    def exec(self):
        self.dialog.exec()