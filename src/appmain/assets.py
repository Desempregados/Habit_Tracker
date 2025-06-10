import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys._MEIPASS)
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = PROJECT_ROOT / "assets"


def get_path_asset(relative_path: str) -> Path:
    final_path = ASSETS_DIR / relative_path
    if not final_path.exists():
        raise FileNotFoundError(f"Required path not found {final_path}")

    return final_path
