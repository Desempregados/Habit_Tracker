from database import _connection_boilerplate, obtain_path_db
import sqlite3
from datetime import date


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


def db_add_goal_value(goal_id: int, value: int) -> bool:
    db_path = obtain_path_db()
    params = (value, goal_id)
    try:
        with sqlite3.connect(db_path) as conn:
            _connection_boilerplate(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
            UPDATE goals SET current_value = current_value + ? WHERE id = ?
            """,
                params,
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(e)
        return False

