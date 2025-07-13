import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QDialog,
    QScrollArea,
    QLabel,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from appmain.features.goals.container_goal import ContainerGoal
from pathlib import Path
from appmain.database.create import db_create_goal
from appmain.database.read import db_obtain_skill_by_id, db_read_goal_by_skill, db_obtain_dedicated_time
from appmain.features.goals.goals_dialog import NewGoalDialog


class GoalsUI(QWidget):
    def __init__(self, parent=None):
        self.skill_id = None
        # ===================== Boilerplate =============================

        super().__init__(parent)
        self.setObjectName("GoalsUI")
        self.layout_main = QVBoxLayout(self)

        # ===================== Button back =============================

        self.layout_top_buttons = QGridLayout()
        self.button_back = QPushButton("")
        self.button_back.setObjectName("button_back")
        self.layout_top_buttons.addWidget(
            self.button_back, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # ===================== Label select skill =====================

        self.label_skill_name = QLabel("Skill Name")
        self.label_skill_name.setObjectName("label_skill_name")
        self.layout_top_buttons.addWidget(
            self.label_skill_name, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout_top_buttons.setColumnStretch(0, 1)
        self.layout_top_buttons.setColumnStretch(2, 1)
        self.layout_main.addLayout(self.layout_top_buttons)

        # ====================== Label total time ==============================

        self.label_total_time = QLabel("00:00:00")
        self.label_total_time.setObjectName("label_total_time")
        self.layout_main.addWidget(
            self.label_total_time, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # ====================== Goals scroll area ============================

        self.scroll_area_goals = QScrollArea()
        self.scroll_area_goals.setObjectName("scroll_area")
        self.scroll_area_goals.setWidgetResizable(True)
        self.scroll_area_goals.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area_goals.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # ====================== Widget scroll area ===========================

        self.widget_scroll_area_goals = QWidget()
        self.widget_scroll_area_goals.setObjectName("widget_scroll_area")
        self.layout_scroll_area = QVBoxLayout()
        self.widget_scroll_area_goals.setLayout(self.layout_scroll_area)
        self.scroll_area_goals.setWidget(self.widget_scroll_area_goals)

        self.layout_main.addWidget(self.scroll_area_goals)

        # ====================== Button add goal =========================

        self.layout_button_add_goal = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button_add_goal)

        self.layout_button_add_goal.addStretch(1)
        self.button_add_goal = QPushButton("")
        self.button_add_goal.setObjectName("button_add_goal")
        self.layout_button_add_goal.addWidget(self.button_add_goal)
        self.layout_button_add_goal.addStretch(1)

        self.button_add_goal.clicked.connect(lambda: self.add_goal())

        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_goals.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    # ====================== Load skill data ============================

    def load_skill_data(self, skill_id: int):
        self.clear_containers()
        self.skill_id = skill_id
        skill_name = db_obtain_skill_by_id(skill_id)
        total_time = self.form_time(db_obtain_dedicated_time(skill_id))

        goals_list: list = db_read_goal_by_skill(skill_id, False)

        for goal in goals_list:
            goal_id = goal["id"]
            container = ContainerGoal(goal_id)
            container.goal_deleted.connect(lambda: self.load_skill_data(self.skill_id))
            self.layout_scroll_area.addWidget(container)

        self.layout_scroll_area.addStretch(1)

        self.label_skill_name.setText(skill_name)
        self.label_total_time.setText(total_time)

    # ========================= Clear containers ============================

    def clear_containers(self):
        while self.layout_scroll_area.count():
            child = self.layout_scroll_area.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # ========================= Add goals ====================================

    def add_goal(self):
        dialog = NewGoalDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            results = dialog.get_inputs()
            name = results[0]
            value = results[1]

            db_create_goal(self.skill_id, name, "time", value, 7)
            self.load_skill_data(self.skill_id)

    # ========================== Form time ====================================

    def form_time(self, s: int) -> str:
        return f"{int(s // 3600):02d}:{int((s // 60) % 60):02d}:{int(s % 60):02d}"


def main():
    app = QApplication(sys.argv)
    window = GoalsUI()
    window.load_skill_data(2)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
