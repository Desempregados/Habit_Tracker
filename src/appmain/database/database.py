from pathlib import Path
import sqlite3

def _connection_boilerplate(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row


def obtain_path_db() -> Path:
    APP_NAME = "HabitTracker"
    DB_FILE = "habittracker.db"
    data_dir = Path.home() / ".local" / "share" / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / DB_FILE
