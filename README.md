# SinCleaner

SinCleaner is a lightweight Python utility with a graphical interface for basic file and image operations.
The project focuses on simplicity, predictability, and local-only processing.

It is designed as a small but extensible tool rather than a full-featured image editor.
---
Although this project has reached its first public release, it is still under active development and expected to receive many new features, improvements, and refinements in future versions.
A command-line interface (CLI) is planned and will be integrated after the graphical interface reaches a stable and feature-complete state.
## Features

- File selection via GUI
- Detailed file information display
- Filename normalization
- Image resizing with aspect ratio preservation
- Image format conversion (PNG, JPG, WEBP)
- EXIF metadata inspection and removal
- Shared core logic usable from both GUI and CLI

---

## Requirements (requirements.txt implemented)

- Python 3.10 or newer
- Pillow
- PySide6
- piexif

---

## Installation

Clone the repository and navigate into it:

```bash
git clone https://github.com/<your-username>/SinCleaner.git
cd SinCleaner
