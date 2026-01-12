from pathlib import Path
from PIL import Image
import math

def calculate_new_size(
        orig_width: int,
        orig_height: int,
        *,
        max_width: int | None,
        max_height: int | None,
) -> tuple[int, int]:
    scale_w = max_width / orig_width if max_width else 1
    scale_h = max_height / orig_height if max_height else 1

    scale = min(scale_h, scale_w)

    if scale >=1:
        return orig_width, orig_height
    
    new_width = math.ceil(int(orig_width * scale))
    new_height = math.ceil(int(orig_height * scale))

    return new_width, new_height

def resize_image(
        path: Path,
        *,
        max_width: int | None,
        max_height: int | None,
        dry_run: bool = False
) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if max_width is None and max_height is None:
        raise ValueError("Either max_width or max_height must be provided.")
    
    report = []

    image = Image.open(path)
    orig_width, orig_height = image.size

    new_width, new_height = calculate_new_size(
        orig_width=orig_width,
        orig_height=orig_height,
        max_width=max_width,
        max_height=max_height,
    )
    

    if (new_width, new_height) == (orig_width, orig_height):
        report.append("The image size already matches, no further resizing actions are required")
        return report
    
    if dry_run:
        report.append(f"The resizing was successful. New dimensions: {new_width}, {new_height}")
        report.append(f"Dry-run enabled, no changes were applied")
        return report
    
    resized = image.resize((new_width, new_height), Image.LANCZOS)
    report.append(f"The resizing was successful. New dimensions: {new_width}, {new_height}")
    resized.save(path)
    report.append(f"The new dimensions are applied to the image")
    return report