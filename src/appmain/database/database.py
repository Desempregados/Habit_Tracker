import sqlite3
from pathlib import Path
from datetime import date, timedelta


def _connection_boilerplate(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row


def obtain_path_db() -> Path:
    APP_NAME = "HabitTracker"
    DB_FILE = "habittracker.db"
    data_dir = Path.home() / ".local" / "share" / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / DB_FILE


# CREATE


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
            registry_time TEXT NOT NULL,
            dedicated_time INTEGER DEFAULT 0,

            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id INTEGER NOT NULL,
            goal_type TEXT NOT NULL,
            goal_value INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT "active",

            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
            CONSTRAINT unique_goal UNIQUE (skill_id, goal_type, start_date)
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

    db_path = obtain_path_db()
    params = (skill_name.strip(), str(date.today()))

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


def db_add_registry(skill_id: int, dedicated_time: int = 0) -> bool:
    params = (skill_id, str(date.today()), dedicated_time)
    db_path = obtain_path_db()
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            INSERT INTO registries  (skill_id, registry_time, dedicated_time)
            VALUES (?, ?, ?)
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_create_goal(
    skill_id: int, goal_type: str, goal_value: int, time_delta: int, status="active"
) -> bool:
    possible_types = ("time", "quantity")
    if goal_type not in possible_types:
        raise Exception("Goal type can only be time or quantity")

    start_date = date.today()
    end_date = date.today() + timedelta(days=time_delta - 1)
    params = (skill_id, goal_type, goal_value, str(start_date), str(end_date), status)
    db_path = obtain_path_db()
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            INSERT INTO goals  (skill_id, goal_type, goal_value, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


# READ


def db_obtain_all_skills() -> list:
    db_path = obtain_path_db()
    skills = []

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, creation_time FROM skills ORDER BY name")
            skills = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)

    return skills


def db_obtain_skill_by_id(skill_id: int) -> str:
    db_path = obtain_path_db()
    skill_name = None
    param = (skill_id,)

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM skills WHERE id = ? ", param)
            skill_name = cursor.fetchone()["name"]
            return skill_name
    except sqlite3.Error as e:
        print(e)
        return "error"


def db_obtain_dedicated_time_delta(skill_id: int, delta_time: int = 7) -> int:
    db_path = obtain_path_db()
    dedicated_time = None
    begining_date = date.today()
    final_date = date.today() - timedelta(days=delta_time - 1)
    param = (skill_id, str(final_date), str(begining_date))

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            SELECT IFNULL (SUM(dedicated_time), 0) AS total_time
            FROM registries
            WHERE
                skill_id = ?
                AND registry_time BETWEEN ? AND ?;
            """,
                param,
            )
            dedicated_time = cursor.fetchone()
            return dedicated_time["total_time"]

    except sqlite3.Error as e:
        print(e)
        return -1


def db_obtain_dedicated_time(skill_id: int) -> int:
    db_path = obtain_path_db()
    dedicated_time = None
    param = (skill_id,)

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            SELECT IFNULL (SUM(dedicated_time), 0) AS total_time
            FROM registries
            WHERE
                skill_id = ?
            """,
                param,
            )
            dedicated_time = cursor.fetchone()
            return dedicated_time["total_time"]

    except sqlite3.Error as e:
        print(e)
        return -1


def db_read_goal_status(goal_id: int) -> str:
    db_path = obtain_path_db()
    param = (goal_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT status FROM goals
                WHERE id = ?
            """,
                param,
            )
            status = cursor.fetchone()
            return status["status"]

    except sqlite3.Error as e:
        print(e)
        return "error"


def db_read_goal_value(goal_id: int) -> int:
    db_path = obtain_path_db()
    param = (goal_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT goal_value FROM goals
                WHERE id = ?
            """,
                param,
            )
            value = cursor.fetchone()
            return value["goal_value"]

    except sqlite3.Error as e:
        print(e)
        return -1


def db_read_goal_type(goal_id: int) -> int:
    db_path = obtain_path_db()
    param = (goal_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT goal_type FROM goals
                WHERE id = ?
            """,
                param,
            )
            goal_type = cursor.fetchone()
            return goal_type["goal_type"]

    except sqlite3.Error as e:
        print(e)
        return -1


def db_read_goal_by_skill(skill_id: int, only_actives: bool = True) -> list:
    db_path = obtain_path_db()
    param = (skill_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            if only_actives:
                cursor.execute(
                    """
                    SELECT * FROM goals
                    WHERE skill_id = ? AND status = 'active'
                    ORDER BY start_date;
                """,
                    param,
                )

            else:
                cursor.execute(
                    """
                    SELECT * FROM goals
                    WHERE skill_id = ?
                    ORDER BY start_date;
                """,
                    param,
                )

            goal = cursor.fetchall()
            return goal

    except sqlite3.Error as e:
        print(e)
        return []


def db_read_goal_actives() -> list:
    db_path = obtain_path_db()
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT goal_type FROM goals
                WHERE status = 'active'
            """,
            )
            goals = cursor.fetchall()
            return goals

    except sqlite3.Error as e:
        print(e)
        return []


# UPDATE


def db_rename_skill(skill_id: int, new_name: str) -> bool:
    db_path = obtain_path_db()
    param = (new_name, skill_id)

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            UPDATE skills SET name = ? WHERE id = ?
            """,
                param,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_update_registry(registry_id: int, new_time: int) -> bool:
    db_path = obtain_path_db()
    params = (new_time, registry_id)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            UPDATE registries SET dedicated_time = ? WHERE id = ?
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_update_goal_status(goal_id: int, status: str) -> bool:
    db_path = obtain_path_db()
    params = (status, goal_id)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            UPDATE goals SET status = ? WHERE id = ?
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


def db_update_goal_data(goal_id: int, new_value: int, new_end_date: date) -> bool:
    db_path = obtain_path_db()
    params = (new_value, str(new_end_date), goal_id)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            UPDATE goals SET goal_value = ? , end_date = ? WHERE id = ?
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False


# DELETE


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


if __name__ == "__main__":
    pass
