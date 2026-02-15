from pathlib import Path
from datetime import datetime

EXPORT_PATH = Path(__file__).parent.parent.parent / "export"

def export_data(name: str, data: str):
    from core.meta.export import EXPORT_PATH
    path = EXPORT_PATH
    time = datetime.now().strftime("%H.%M.%S")
    with open(f"{path}//{name}.txt", "w+") as file:
        file.write(data)