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
from core.resize import resize_image
from core.convert import convert_image
from core.compress import compress_image
from core.aspect_ratio import change_image_aspect_ratio

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file: Path | None = None

        self._load_ui()
        self._connect_signals()

        self.setFixedSize(self.size())
    
    def _load_ui(self): # Base loading
        loader = QUiLoader()

        ui_path = Path(__file__).parent / "sincleanerV2.ui" #ui file
        ui_file = QFile(str(ui_path))
        ui_file.open(QFile.ReadOnly)

        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(self.ui.centralWidget())
        self.setWindowTitle(self.ui.windowTitle())


    def _connect_signals(self): # Signals from UI to connect with logic
        # UI states
        self.ui.comboAspectRatio.currentTextChanged.connect(self._on_aspect_ratio_changed)

        # File tab
        self.ui.btnSelectFile.clicked.connect(self.choose_file)
        self.ui.btnRenameFile.clicked.connect(self.rename_file)

        # Metadata tab
        self.ui.btnClearMetadata.clicked.connect(self.clear_file_metadata)
        # self.ui.btnOpenMetadataFull.clicked.connect(self.open_metadata_full) ill make ts work soon cuz it pmo so harddddddd

        # Image tab
        self.ui.btnResize.clicked.connect(self.resize_current_image)
        self.ui.btnConvert.clicked.connect(self.convert_current_image)
        self.ui.btnCompress.clicked.connect(self.compress_current_image)
        self.ui.btnChangeAspectRatio.clicked.connect(self.change_current_image_aspect_ratio)


    # GUI logic down there


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

    def resize_current_image(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return

        max_width = self.ui.spinWidth.value()
        if max_width == 0:
            max_width = None
        max_height = self.ui.spinHeight.value()
        if max_height == 0:
            max_height = None

        try:
            resize_image(
                self.current_file,
                max_width=max_width,
                max_height=max_height,
                dry_run=False,
            )
        
        except Exception as e:
            QMessageBox.critical(self, "resize_current_image() failed", str(e))
            return
        
    def convert_current_image(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return
        
        to_format = str(self.ui.comboFormat.currentText()).lower()
        
        try:
            convert_image(
                self.current_file,
                to_format=to_format,
                dry_run=False,
            )
        
        except Exception as e:
            QMessageBox.critical(self, "convert_current_image() failed", str(e))
            return
        
    def compress_current_image(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return
        
        quality = int(self.ui.spinQuality.value())

        if quality <= 0:
            QMessageBox.warning(self, "Error", "Wrong quality input")
            return
        
        try:
            compress_image(
                path=self.current_file,
                quality=quality,
                dry_run=False
            )

        except Exception as e:
            QMessageBox.critical(self, "compress_current_image() failed", str(e))
            return
    
    def change_current_image_aspect_ratio(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return
        
        text = self.ui.comboAspectRatio.currentText()

        if ":" in text:
            ratio_w, ratio_h = map(int, text.split(":"))
        elif text == "Custom":
            ratio_w = self.ui.spinAspectW.value()
            ratio_h = self.ui.spinAspectH.value()
        else:
            return
        
        try:
            change_image_aspect_ratio(
                path=self.current_file,
                ratio_w=ratio_w,
                ratio_h=ratio_h,
            )
        except Exception as e:
            QMessageBox.critical(self, "change_current_image_aspect_ratio() failed", str(e))
            return
        

        # UI elements states and utils

    def _on_aspect_ratio_changed(self):
        combo = self.ui.comboAspectRatio
        if combo.currentText() == "Custom":
            self.ui.labelAspectCustom.setVisible(True)
            self.ui.spinAspectW.setVisible(True)
            self.ui.spinAspectH.setVisible(True)
            self.ui.labelAspectColon.setVisible(True)
        else:
            self.ui.labelAspectCustom.setVisible(False)
            self.ui.spinAspectW.setVisible(False)
            self.ui.spinAspectH.setVisible(False)
            self.ui.labelAspectColon.setVisible(False)

    def _last_action_text(self, text):
        lat = self.ui.labelLastAcion
        lat.setText(text)