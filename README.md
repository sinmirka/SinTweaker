# 🫧 SinCleaner

### Lightweight desktop utility for image and file operations.
Built with Python + PySide6.

SinCleaner focuses on simplicity, predictability, and local-only processing.

## 💻 Development Recommendation

It is recommended to run the project using an IDE such as Visual Studio Code or any other Python-compatible IDE.

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

## ⚠ Important Notice

A standalone .exe version is planned for future releases to allow easier installation and usage without requiring a Python environment.

For now, the application must be run from source using Python 3.10+.

## ✨ Features

Image resize (aspect ratio preserved)

Format conversion (PNG, JPG, WEBP)

Compression control

Aspect ratio modification

EXIF metadata view & cleanup

Metadata export to .txt

Filename normalization

Image preview

Built-in logging system

Dry-run & overwrite support

🧠 Architecture

GUI separated from core logic

Domain-based core structure

Unified function return contracts

Centralized settings system (AppConfig)

## 📦 Requirements

Python 3.10+

Pillow

PySide6

piexif

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## 🔄 Version

Current version: v2.0.0

Major architectural milestone of the project.
