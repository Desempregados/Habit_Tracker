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


def db_delete_skill(skill_id: int) -> bool:
    db_path = obtain_path_db()
    param = (skill_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            DELETE FROM skills WHERE id = ?
            """,
                param,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_delete_goal(goal_id: int) -> bool:
    db_path = obtain_path_db()
    param = (goal_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            DELETE FROM goals WHERE id = ?
            """,
                param,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_delete_table(table_name: str) -> bool:
    db_path = obtain_path_db()
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                DROP TABLE IF EXISTS {table_name}
                """
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


if __name__ == "__main__":
    pass
