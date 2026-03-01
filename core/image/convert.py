from pathlib import Path
from PIL import Image
from config import AppConfig

def convert_image(
        path: Path,
        *,
        to_format: str,
        config: AppConfig,
) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    to_format = to_format.lower().lstrip(".")

    report = []

    src_ext = path.suffix.lower().lstrip(".")

    if src_ext == to_format:
        return report
    
    new_path = path.with_suffix(f".{to_format}")

    report.append(
        f"Convert {path.name} to {new_path.name}"
    )

    if config.dry_run:
        report.append(f"Dry-run enabled, no changes were applied")
        return report
    try:
        image = Image.open(path)
        image.save(new_path)
        report.append("Conversion applied successfully.")
    except Exception as e:
       report.append(f"Conversion failed: {e}") 

    return report, new_path