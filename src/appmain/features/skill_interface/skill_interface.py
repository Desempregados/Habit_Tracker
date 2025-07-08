import sys
from pathlib import Path
from appmain.database.database import *
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QButtonGroup,
    QProgressBar,
)
from PyQt6.QtCore import Qt


class SkillInterface(QWidget):
    def __init__(self, parent=None):
        # ======================= Boilerplate ===================
        self.item_id = None

        super().__init__(parent)
        self.setObjectName("SkillsInterface")

        self.layout_main = QVBoxLayout(self)

        # ======================= Button back ===================

        self.layout_button_back = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button_back)
        self.button_back = QPushButton("")
        self.button_back.setObjectName("button_back")
        self.layout_button_back.addWidget(self.button_back)
        self.layout_button_back.addStretch(1)

        # ======================== Label skill name ==============

        self.label_skill_name = QLabel("Skill Name")
        self.label_skill_name.setObjectName("label_skill_name")
        self.label_skill_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill_name)

        # ========================= Button clock ==================

        self.layout_button_clock = QHBoxLayout()
        self.layout_button_clock.addStretch(1)
        self.layout_main.addLayout(self.layout_button_clock)
        self.button_clock = QPushButton("")
        self.button_clock.setObjectName("button_clock")
        self.layout_button_clock.addWidget(self.button_clock)
        self.layout_button_clock.addStretch(1)

        self.layout_main.addStretch(1)

        # ========================= Label goal ====================

        self.label_goal = QLabel("00:00:00/11:11:11")
        self.label_goal.setObjectName("label_goal")
        self.label_goal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.layout_main.addWidget(self.label_goal)

        # ========================= Progress bar ==================

        self.progress_bar = QProgressBar()
        # self.layout_main.addWidget(self.progress_bar)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(50)

        # ========================= Goal button ====================

        self.layout_button_goal = QHBoxLayout()
        self.button_goal = QPushButton("")
        self.button_goal.setObjectName("button_goal")
        self.layout_button_goal.addStretch(1)
        self.layout_button_goal.addWidget(self.button_goal)
        self.layout_button_goal.addStretch(1)
        self.layout_main.addLayout(self.layout_button_goal)
        self.layout_main.addStretch(2)

        # ========================= Label dedicated time ===========

        self.label_skill_dedicated_time = QLabel("Dedicated Time")
        self.label_skill_dedicated_time.setObjectName("dedicated_time")
        self.label_skill_dedicated_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill_dedicated_time)

        # ========================== Time interval selection ========

        self.layout_time_interval = QHBoxLayout()
        self.layout_main.addLayout(self.layout_time_interval)
        self.layout_time_interval.addStretch(2)

        self.buttongroup_time_interval = QButtonGroup(self)
        self.buttongroup_time_interval.setExclusive(True)

        # ========================== Button today ====================

        self.button_today = QPushButton("today")
        self.button_today.setCheckable(True)
        self.buttongroup_time_interval.addButton(self.button_today)
        self.layout_time_interval.addWidget(self.button_today)
        self.button_today.clicked.connect(lambda: self.load_time(0))
        self.button_today.setObjectName("button_today")
        self.layout_time_interval.addStretch(1)

        # ========================== Button week =====================

        self.button_week = QPushButton("week")
        self.button_week.setCheckable(True)
        self.buttongroup_time_interval.addButton(self.button_week)
        self.layout_time_interval.addWidget(self.button_week)
        self.button_week.clicked.connect(lambda: self.load_time(1))
        self.button_week.setObjectName("button_week")
        self.layout_time_interval.addStretch(1)

        # ========================== Button all time ==================

        self.button_alltime = QPushButton("all time")
        self.button_alltime.setCheckable(True)
        self.buttongroup_time_interval.addButton(self.button_alltime)
        self.layout_time_interval.addWidget(self.button_alltime)
        self.button_alltime.clicked.connect(lambda: self.load_time(2))
        self.button_alltime.setObjectName("button_alltime")

        self.layout_time_interval.addStretch(2)
        self.layout_main.addStretch(1)

        # =========================== Label show_time ==================

        self.label_show_time = QLabel("00:00")
        self.label_show_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_show_time)
        self.label_show_time.setObjectName("label_show_time")

        self.layout_main.addStretch(2)

        self.Load_stylesheet()

    def Load_stylesheet(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_skill_interface.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    def load_skill_data(self, item_id: int):
        self.item_id = item_id

        skill_name = db_obtain_skill_by_id(item_id)
        self.label_skill_name.setText(skill_name)
        self.button_week.click()

    def load_time(self, opt: int):
        if opt == 0:
            self.label_show_time.setText(
                self.form_time(db_obtain_dedicated_time_delta(self.item_id, 1))
            )

        if opt == 1:
            self.label_show_time.setText(
                self.form_time(db_obtain_dedicated_time_delta(self.item_id))
            )

        if opt == 2:
            self.label_show_time.setText(
                self.form_time(db_obtain_dedicated_time(self.item_id))
            )

    def form_time(self, s: int) -> str:
        return f"{int(s // 3600):02d}:{int((s // 60) % 60):02d}:{int(s % 60):02d}"


def main():
    app = QApplication(sys.argv)
    window = SkillInterface()
    window.load_skill_data(2)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
