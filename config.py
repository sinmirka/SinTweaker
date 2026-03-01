from dataclasses import dataclass

@dataclass
class AppConfig:
    overwrite: bool = False
    dry_run: bool = False