![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

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
