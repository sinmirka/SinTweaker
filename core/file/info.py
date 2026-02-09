from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from core.meta.image import get_image_metadata

IMAGE_EXTENSIONS = {".jpg", ".jpeg"}

@dataclass
class FileInfo: 
    path: Path
    name: str
    extension: str
    size_bytes: int
    created_at: datetime
    modified_at: datetime
    metadata: dict[str, any]

    def size_human(self) -> str:
        size = self.size_bytes
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

def get_file_info(path: Path) -> FileInfo:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    stat = path.stat()

    metadata = {}
    if path.suffix.lower() in IMAGE_EXTENSIONS:
        metadata = get_image_metadata(path=path)
    
    return FileInfo(
        path=path,
        name=path.name,
        extension=path.suffix,
        size_bytes=path.stat().st_size,
        created_at=datetime.fromtimestamp(stat.st_birthtime),
        modified_at=datetime.fromtimestamp(stat.st_mtime),
        metadata=metadata,
    )