# 🫧 SMToolkit

### Lightweight desktop toolkit for image and file operations.
Built with Python + PySide6.

SMToolkit focuses on simplicity, predictability, and local-only processing.  
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

## Install

```bash
pip install -r requirements.txt