from pathlib import Path
from PIL import Image

def define_new_size(
        path: Path,
        ratio_w: int,
        ratio_h: int,
):
    if not path.exists():
        return
    
    image = Image.open(path)

    src_width, src_height = image.size
    src_ratio = src_width / src_height
    new_ratio = ratio_w / ratio_h

    if src_ratio > new_ratio: # width > height
        new_width = src_height * new_ratio
        new_height = src_height
        return new_width, new_height
    elif src_ratio < new_ratio: # width < height
        new_height = src_width / new_ratio
        new_width = src_width
        return new_width, new_height
    else:
        return src_width, src_height

def change_image_aspect_ratio(
        path: Path,
        ratio_w: int,
        ratio_h: int,
) -> list[str]:
    if not path.exists():
        raise ValueError(f"File not found: {path}")
    image = Image.open(path)

    new_width, new_height = define_new_size(path=path, ratio_w=ratio_w, ratio_h=ratio_h)

    report = []

    try:
        resized = image.resize((int(new_width), int(new_height)), Image.LANCZOS)
        report.append(f"Successfully changed aspect ratio. New dimensions: {new_width}:{new_height}")
        resized.save(path)
    except Exception as e:
        report.append(f"Error changing aspect ratio: {e}")
    
    return report