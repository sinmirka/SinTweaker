from dataclasses import dataclass

@dataclass
class AppConfig:
    overwrite: bool = False
    quality: int = 85
    preserve_metadata: bool = False