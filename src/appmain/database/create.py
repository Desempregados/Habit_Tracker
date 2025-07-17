import sqlite3
from datetime import date, timedelta, datetime
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


def db_create() -> bool:
    db_path = obtain_path_db()

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            creation_time TEXT NOT NULL

            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS registries(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id INTEGER NOT NULL,
            goal_id INTEGER NOT NULL,
            registry_time TEXT NOT NULL,
            dedicated_time INTEGER DEFAULT 0,

            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
            FOREIGN KEY (goal_id) REFERENCES goals (id) ON DELETE CASCADE
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT NOT NULL,
            skill_id INTEGER NOT NULL,
            goal_type TEXT NOT NULL,
            current_value INTEGER DEFAULT 0,
            goal_value INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT "active",

            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
            CONSTRAINT unique_goal UNIQUE (skill_id, goal_name)
            );
            """)

            # Goal type can be time or quantity

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_registries_skills_data
            ON registries (skill_id, registry_time);
            """)

            conn.commit()

            return True

    except sqlite3.Error as e:
        print(e)
        return False


def db_create_skill(skill_name: str) -> bool:
    if not skill_name.strip():
        return False

    date = datetime.now()
    form_date = date.strftime("%Y-%m-%d %H:%M:%S")
    db_path = obtain_path_db()
    params = (skill_name.strip(), str(form_date))

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO skills (name, creation_time) VALUES (?, ?)", params
            )
            conn.commit()
            return True

    except sqlite3.Error as e:
        print(e)
        return False


def db_add_registry(skill_id: int, dedicated_time: int = 0, goal_id: int = 0) -> bool:
    date = datetime.now()
    form_date = date.strftime("%Y-%m-%d %H:%M:%S")
    params = (skill_id, str(form_date), dedicated_time, goal_id)
    db_path = obtain_path_db()
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            INSERT INTO registries  (skill_id, registry_time, dedicated_time, goal_id)
            VALUES (?, ?, ?, ?)
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_create_goal(
    skill_id: int,
    goal_name: str,
    goal_type: str,
    goal_value: int,
    time_delta: int,
    status="active",
) -> bool:
    possible_types = ("time", "quantity")
    if goal_type not in possible_types:
        raise Exception("Goal type can only be time or quantity")

    start_date = date.today()
    end_date = date.today() + timedelta(days=time_delta - 1)
    params = (
        skill_id,
        goal_name,
        goal_type,
        goal_value,
        str(start_date),
        str(end_date),
        status,
    )
    db_path = obtain_path_db()
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            INSERT INTO goals  (skill_id, goal_name, goal_type, goal_value, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


if __name__ == "__main__":
    db_create()
