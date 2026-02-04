def format_metadata(meta: dict) -> str:
    if not meta:
        return "No metadata found."
    
    lines = []

    # meta is a dict:
    # { "0th": {...}, "Exif": {...}, "GPS": {...}, "thumbnail": bytes }

    for section, data in meta.items():
        lines.append(f"[{section}]")

        #thumbnail is a binary data and we should not fully display it

        if section == "thumbnail":
            lines.append(f"<{len(data)} bytes")
        else:
            for tag, value in data.items():
                lines.append(f"{tag}: {value}")
        
        lines.append("")
    
    return "\n".join(lines)