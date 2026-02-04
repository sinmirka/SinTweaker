from pathlib import Path

from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MetadataWindow():
    def __init__(self, text: str, parent=None):
        loader = QUiLoader()

        ui_path = Path(__file__).parent / "ui_files" / "metadata_win.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QFile.ReadOnly)

        self.dialog = loader.load(ui_file, parent)
        ui_file.close()

        self.dialog.textMetadata.setPlainText(text)

        self._connect_signals()

    def _connect_signals(self):
        self.ui.btnClose.clicked.connect(self.close)
        self.ui.btnCopy.clicked.connect(self._copy_to_clipboard)

        # these are not working for now 04.02.2026
        # logic will be connected soon 
        self.ui.btnExport.clicked.connect(self._export_metadata)
        self.ui.btnSelectiveClean.clicked.connect(self._selective_clean)
        self.ui.btnRefresh.clicked.connect(self._refresh_metadata)

    def _connect_signals(self):
        self.dialog.btnClose.clicked.connect(self.dialog.close)
        self.dialog.btnCopy.clicked.connect(self._copy_to_clipboard)

    def _copy_to_clipboard(self):
        clipboard = self.dialog.textMetadata.clipboard()
        clipboard.setText(self.dialog.textMetadata.toPlainText())

    def exec(self):
        self.dialog.exec()