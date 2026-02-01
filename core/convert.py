from pathlib import Path
from PIL import Image

def convert_image(
        path: Path,
        *,
        to_format: str,
        dry_run: bool = False,
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

    if dry_run:
        report.append(f"Dry-run enabled, no changes were applied")
        return report
    
    image = Image.open(path)
    image.save(new_path)
    report.append("Conversion applied successfully.")

    return report