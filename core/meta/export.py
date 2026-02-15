from pathlib import Path
from datetime import datetime
import os
import platform
import subprocess

EXPORT_PATH = Path(__file__).parent.parent.parent / "export"

def resolve_name_conflict(path: Path) -> Path:
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1

    while path.exists():
        path = parent / f"{stem}_{counter}{suffix}"
        counter += 1
    
    return path

def open_file_manager(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin": # macOS
        subprocess.Popen(["open", path])
    else: # Linux
        subprocess.Popen(["xdg-open", path])

def export_data(name: str, data: str):
    from core.meta.export import EXPORT_PATH
    path = EXPORT_PATH / f"{name}.txt"
    if path.exists():
        path = resolve_name_conflict(path=path)
    with open(path, "w+") as file:
        file.write(data)
    open_file_manager(EXPORT_PATH)