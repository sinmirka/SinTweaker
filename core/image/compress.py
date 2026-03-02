from pathlib import Path
from PIL import Image
from config import AppConfig

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".webp", ".png"}

def compress_image(
        path: Path,
        *,
        quality: int,
        config: AppConfig,
) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    extension = path.suffix.lower()
    if extension not in SUPPORTED_FORMATS:
        raise ValueError(f"Compression is not supported for {extension}")
    
    report = []

    image = Image.open(path)

    save_kwargs = {}

    if extension in {".jpg", ".jpeg", ".webp"}:
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True
        report.append(f"Compression → quality={quality}")
    elif extension == ".png":
        compress_level = max(0, min(9, 9 - quality // 11))
        save_kwargs["compress_level"] = compress_level
        save_kwargs["optimize"] = True
        report.append(f"Compression → level={compress_level}")

    if config.dry_run:
        report.append("Dry-run enabled, no changes were applied")
        return report
    
    image.save(path, **save_kwargs)
    report.append("Compression applied successfully")

    return report