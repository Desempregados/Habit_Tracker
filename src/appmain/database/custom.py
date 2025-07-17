import sqlite3
from pathlib import Path


def _connection_boilerplate(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row


def obtain_path_db() -> Path:
    APP_NAME = "HabitTracker"
    DB_FILE = "habittracker.db"
    data_dir = Path.home() / ".local" / "share" / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / DB_FILE


def db_custom_query() -> bool:
    db_path = obtain_path_db()

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            ALTER TABLE registries
            ADD COLUMN goal_id INTEGER NOT NULL
            DEFAULT 0
            """,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


if __name__ == "__main__":
    pass
