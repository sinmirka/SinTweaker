from pathlib import Path

from core.meta.image import get_image_metadata, clean_image_metadata

_METADATA_READERS = {
    ".jpg": get_image_metadata,
    ".jpeg": get_image_metadata,
    ".png": get_image_metadata,
    ".webp": get_image_metadata,
}

_METADATA_CLEANERS = {
    ".jpg": clean_image_metadata,
    ".jpeg": clean_image_metadata,
    ".png": clean_image_metadata,
    ".webp": clean_image_metadata,
}

def get_metadata(path: Path) -> dict:
    handler = _METADATA_READERS.get(path.suffix.lower())
    if not handler:
        return {}
    
    return handler(path)

def clear_metadata(path: Path, *, dry_run: bool = False) -> list[str]:
    handler = _METADATA_CLEANERS.get(path.suffix.lower())
    if not handler:
        return {}
    
    return handler(path=path, dry_run=dry_run)