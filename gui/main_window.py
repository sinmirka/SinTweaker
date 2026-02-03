from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from core.rename import rename_file
from core.meta.meta_handler import get_metadata, clear_metadata
from core.info import get_file_info
from core.resize import resize_image
from core.convert import convert_image
from core.compress import compress_image
from core.aspect_ratio import change_image_aspect_ratio

from core.logging.logger import Logger

logger = Logger()

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

        self.ui.textInfo.setPlainText("No file selected")
        
        self.log("UI loaded successfully")


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

        self.log("UI signals connected")


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
        self._update_image_preview()
        self.log(f"File chosen. Path: {self.current_file}")

    def rename_file(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected")
            return
        
        try:
            report = rename_file(self.current_file)
            self.log(report=report)
        except Exception as e:
            QMessageBox.critical(self, "Rename failed", str(e))
            self.log(f"Rename failed: {str(e)}")
            return
        

    def update_metadata_view(self):
        if not self.current_file:
            self.ui.textMetadata.clear()
            self.log("update_metadata_view called with no selected file")
            return
        
        metadata = get_metadata(self.current_file)

        if not metadata:
            self.ui.textMetadata.setPlainText(
                "Metadata is not supported for this file type\n"
                "or no metadata found."
            )
            self.log(f"No metadata found for {self.current_file.name}")
            return
    
        lines: list[str] = []

        for section, data in metadata.items():
            if section == "thumbnail":
                lines.append(f"{section}: {len(data)} bytes")
            else:
                lines.append(f"{section}: {len(data)} tags")

        self.ui.textMetadata.setPlainText("\n".join(lines))
        self.log(f"Metadata loaded for {self.current_file.name}")

    def clear_file_metadata(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return
        
        try:
            report = clear_metadata(self.current_file)
            self.log(f"Cleared metadata for {self.current_file.name}", report=report)
        except Exception as e:
            QMessageBox.critical(self, "Clear failed", str(e))
        
        self.ui.textMetadata.setPlainText("\n".join(report))
        self.update_metadata_view()

    def show_file_info(self):
        if not self.current_file:
            self.ui.textInfo.setPlainText("No file selected or file info is unavailable.")
            self.log("show_file_info called with no selected file")
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
        self.log(f"File info loaded for {self.current_file.name}")

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
            report = resize_image(
                self.current_file,
                max_width=max_width,
                max_height=max_height,
                dry_run=False,
            )
            self.log(text=None, report=report)
            self._update_image_preview(self)
        
        except Exception as e:
            QMessageBox.critical(self, "resize_current_image() failed", str(e))
            return
        
    def convert_current_image(self):
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No file selected, go to File tab")
            return
        
        to_format = str(self.ui.comboFormat.currentText()).lower()
        
        if to_format == self.current_file.suffix.lower().strip("."):
            QMessageBox.warning(self, "Error", "Format already matches!")
            return
        
        try:
            report = convert_image(
                self.current_file,
                to_format=to_format,
                dry_run=False,
            )
            self.log(text=None, report=report)
            self._update_image_preview(self)
        
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
            report = compress_image(
                path=self.current_file,
                quality=quality,
                dry_run=False
            )
            self.log(report)
            self._update_image_preview(self)

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
            report = change_image_aspect_ratio(
                path=self.current_file,
                ratio_w=ratio_w,
                ratio_h=ratio_h,
            )
            self.log(
                f"Changed aspect ratio for {self.current_file.name} "
                f"to {ratio_w}:{ratio_h}",
                report=report
            )
            self._update_image_preview(self)
        except Exception as e:
            QMessageBox.critical(self, "change_current_image_aspect_ratio() failed", str(e))
            return
        

        # UI elements states, updates and other utils

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

    
    def _update_image_preview(self, *_):
        if not self.current_file:
            self.ui.labelImagePreview.setText("Image only")
            return
        
        if self.current_file.suffix.lower() not in {'.jpg', ".jpeg", ".png", ".webp"}:
            self.ui.labelImagePreview.setText("Image only")
            return
        
        pixmap = QPixmap(str(self.current_file))

        if pixmap.isNull():
            self.ui.labelImagePreview.setText("Failed to load image")
            return
        
        scaled_pixmap = pixmap.scaled(
            self.ui.labelImagePreview.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.ui.labelImagePreview.setPixmap(scaled_pixmap)

    def log(self, text = None, report = None): #i fixed it boi
        time = datetime.now().strftime("%H:%M:%S")
        lat = self.ui.labelLastAction

        if text:
            lat.setText(f"{text} [{time}]")
            logger.log(text=text)

        if report:
            for line in report:
                logger.log(text=line)
            lat.setText(f"{report[-1]} [{time}]")

        self.ui.textLogs.setText(logger.flush())