from pathlib import Path
import re

def normalize_filename(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    return name

def resolve_name_conflict(path: Path) -> Path:
    counter = 1
    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    while path.exists():
        path = parent / f"{stem}_{counter}{suffix}"
        counter += 1
    
    return path

def rename_file(
        path: Path,
        *,
        dry_run: bool = False,
) -> list[str]:
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    report = []

    normalized_stem = normalize_filename(path.stem)
    new_name = normalized_stem + path.suffix.lower()

    if new_name == path.name:
        report.append("Filename is already normalized. No actions needed")
        return report, path
    
    target_path = path.with_name(new_name)
    new_path = resolve_name_conflict(target_path)

    report.append(f"Target name: {new_path}")
    
    if dry_run:
        report.append(f"Dry-run enabled, no changes were applied")
        return report, path
    
    path.rename(new_path)

    report.append("Rename applied successfully")

    return report, new_path