from pathlib import Path

def create_directory(directory: Path):
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
