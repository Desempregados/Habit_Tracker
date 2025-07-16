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


def db_obtain_all_registries() -> list:
    db_path = obtain_path_db()
    skills = []

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, skill_id, registry_time, dedicated_time
                FROM registries
                ORDER BY registry_time ASC""")
            skills = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)

    return skills


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


def db_read_goal_name(goal_id: int) -> int:
    db_path = obtain_path_db()
    param = (goal_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT goal_name FROM goals
                WHERE id = ?
            """,
                param,
            )
            name = cursor.fetchone()
            if name:
                return name["goal_name"]

            else:
                raise Exception("Invalid Goal id")

    except sqlite3.Error as e:
        print(e)
        return ""


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


def db_read_goal_current_value(goal_id: int) -> int:
    db_path = obtain_path_db()
    param = (goal_id,)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT current_value FROM goals
                WHERE id = ?
            """,
                param,
            )
            current_value = cursor.fetchone()
            return current_value["current_value"]

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


def db_real_all_goals() -> list:
    db_path = obtain_path_db()

    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id
                FROM goals
                ORDER BY (CAST(current_value AS REAL) / goal_value) ASC""")
            goals = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)

    return goals


if __name__ == "__main__":
    goals = db_obtain_all_registries()
    formato = "%Y-%m-%d"
    for a in goals:
        dia = a["registry_time"]
        dia_formatado = datetime.strptime(dia, formato)
        print(dia_formatado.day)
