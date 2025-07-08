import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QDialog,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from appmain.features.goals.container_goal import ContainerGoal
from appmain.database.database import *
from appmain.features.goals.goals_dialog import NewGoalDialog


class GoalsUI(QWidget):
    def __init__(self, parent=None):
        self.skill_id = None
        # ===================== Boilerplate =============================

        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)

        # ===================== Button select skill =====================

        self.layout_button_select_skill = QHBoxLayout()
        self.layout_button_select_skill.addStretch(1)
        self.button_select_skill = QPushButton("Skill Name")
        self.layout_button_select_skill.addWidget(self.button_select_skill)
        self.layout_main.addLayout(self.layout_button_select_skill)
        self.layout_button_select_skill.addStretch(1)

        # ====================== Goals scroll area ============================

        self.scroll_area_goals = QScrollArea()
        self.scroll_area_goals.setWidgetResizable(True)
        self.scroll_area_goals.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area_goals.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # ====================== Widget scroll area ===========================

        self.widget_scroll_area_goals = QWidget()
        self.layout_scroll_area = QVBoxLayout()
        self.widget_scroll_area_goals.setLayout(self.layout_scroll_area)
        self.scroll_area_goals.setWidget(self.widget_scroll_area_goals)

        self.layout_main.addWidget(self.scroll_area_goals)

        # ====================== Button add goal =========================

        self.layout_button_add_goal = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button_add_goal)

        self.layout_button_add_goal.addStretch(1)
        self.button_add_goal = QPushButton("")
        self.layout_button_add_goal.addWidget(self.button_add_goal)
        self.layout_button_add_goal.addStretch(1)

        self.button_add_goal.clicked.connect(lambda: self.add_goal())

    def load_skill_data(self, skill_id: int):
        self.clear_containers()
        self.skill_id = skill_id
        skill_name = db_obtain_skill_by_id(skill_id)

        goals_list: list = db_read_goal_by_skill(skill_id, False)

        for goal in goals_list:
            goal_id = goal["id"]
            container = ContainerGoal(goal_id)
            container.goal_deleted.connect(lambda: self.load_skill_data(self.skill_id))
            self.layout_scroll_area.addWidget(container)

        self.layout_scroll_area.addStretch(1)

        self.button_select_skill.setText(skill_name)

    def clear_containers(self):
        while self.layout_scroll_area.count():
            child = self.layout_scroll_area.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def add_goal(self):
        dialog = NewGoalDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            results = dialog.get_inputs()
            name = results[0]
            value = results[1]

            db_create_goal(self.skill_id, name, "time", value, 7)
            self.load_skill_data(self.skill_id)


def main():
    app = QApplication(sys.argv)
    window = GoalsUI()
    window.load_skill_data(2)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
