from PyQt6.QtCore import (
    pyqtSignal,
    QTimer,
    QObject,
)
from appmain.database.create import db_add_registry
from appmain.database.update import db_add_goal_value



class ChronometerLogic(QObject):
    signal_update_timer = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.working_id = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.up_time)
        self.current_time = 0

    def load_id(self, id: int):
        self.working_id = id

    def form_time(self, s: int) -> str:
        return f"{int(s // 60):02d}:{int(s % 60):02d}"

    def start_timer(self):
        self.timer.start(1000)

    def up_time(self):
        self.current_time += 1
        self.signal_update_timer.emit(self.current_time)

    def pause_timer(self):
        self.timer.stop()

    def restart_timer(self):
        self.timer.stop()
        self.current_time = 0
        self.signal_update_timer.emit(self.form_time(self.current_time))

    def submit_time(self):
        db_add_registry(self.working_id, self.current_time)
        self.restart_timer()

    def add_time_to_goal(self, goal_id: int):
        db_add_goal_value(goal_id, self.current_time)
