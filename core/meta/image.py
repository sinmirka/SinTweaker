from pathlib import Path
from PIL import Image
import piexif

def get_image_metadata(path: Path) -> dict:
    try:
        image = Image.open(path)
    except Exception:
        return {}

    exif_bytes = image.info.get("exif")
    if not exif_bytes:  
        return {}
    
    exif_dict = piexif.load(exif_bytes)
    return exif_dict


def clean_image_metadata(
        path: Path,
        *,
        dry_run: bool = False
    ) -> list[str]:
    meta = get_image_metadata(path)

    if not meta:
        return ["No metadata found. Nothing to clean."]

    report: list[str] = []

    for section, data in meta.items():
        if section == "thumbnail":
            report.append(f"{section}: {len(data)} bytes")
        else:
            report.append(f"{section}: {len(data)} tags")

    if dry_run:
        report.append(f"Dry-run enabled, no changes were applied")
        return report
    
    image = Image.open(path)
    image.save(path)

    return report # you cant normally extract this report into logs because this function is a part of a bigger function which is a part of bigger function so fuck it