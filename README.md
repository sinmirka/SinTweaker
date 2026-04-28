![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![Pillow](https://img.shields.io/badge/Image-Pillow-orange)
![piexif](https://img.shields.io/badge/EXIF-piexif-blue)
![Architecture](https://img.shields.io/badge/architecture-layered-blueviolet)
![GUI](https://img.shields.io/badge/interface-CLI%20%2B%20GUI-informational)
![Local-only](https://img.shields.io/badge/data-local--only-success)

# 🫧 SinTweaker

### SinTweaker (formerly SinCleaner) is a lightweight desktop toolkit for image and file operations.
Built with Python + PySide6.

SinTweaker focuses on simplicity, predictability, and local-only processing.  
It provides a small set of practical tools for working with images and files without unnecessary complexity.

---

## ✨ Features

- Image resizing (aspect ratio preserved)
- Format conversion (PNG, JPG, WEBP)
- Compression control
- Aspect ratio adjustment
- EXIF metadata viewing & cleanup
- Metadata export to `.txt`
- Filename normalization
- Image preview
- Built-in logging system
- Dry-run & overwrite support

---

## 🧠 Architecture

- GUI separated from core logic
- Domain-based core structure
- Unified function return contracts
- Centralized settings system (`AppConfig`)

---

## 📦 Requirements

- Python 3.10+
- Pillow
- PySide6
- piexif

---

## 💻 Development Recommendation / Source Running

It is recommended to run the project using an IDE such as Visual Studio Code or any other Python-compatible IDE because it is more stable and easier to debug.

For a cleaner and safer setup, it is also recommended to use a virtual environment.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate (Windows):

```bash
venv\Scripts\activate
```

Activate (macOS/Linux):

```bash
source venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```
