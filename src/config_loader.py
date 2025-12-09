import yaml

from src.config import Settings


def load_settings_from_file(path: str) -> Settings:
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    # YAML keys should map to Settings field names
    return Settings(**data)
