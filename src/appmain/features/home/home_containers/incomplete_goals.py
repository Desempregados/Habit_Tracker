import sys
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QGridLayout,
    QProgressBar,
)
from PyQt6.QtCore import Qt
from appmain.database.read import (
    db_read_goal_value,
    db_read_goal_name,
    db_read_goal_current_value,
    db_real_all_goals,
)


class ContainerGoal(QWidget):
    def __init__(self, goal_id, parent=None):
        super().__init__(parent)
        self.goal_id = goal_id
        self.layout_main = QGridLayout(self)

        # =============================== Label name =========================

        self.label_name = QLabel("Goal name")
        self.layout_main.addWidget(self.label_name, 0, 0)

        # =============================== Progress bar =======================

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(10)
        self.layout_main.addWidget(self.progress_bar, 0, 1)
        self.setInfo()

        self.layout_main.setColumnStretch(0, 1)
        self.layout_main.setColumnStretch(1, 2)

    def setInfo(self):
        goal_name = db_read_goal_name(self.goal_id)
        current_value = db_read_goal_current_value(self.goal_id)
        goal_value = db_read_goal_value(self.goal_id)
        progress = int((current_value / goal_value) * 100)
        print(progress)

        self.label_name.setText(goal_name)
        self.progress_bar.setValue(progress)


class IncompleteGoals(QWidget):
    def __init__(self, parent=None):
        # ================================ Boilerplate =======================

        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.setStyleSheet("background-color:rgb(130,130,130);")

        # ================================ Label Goals ========================

        self.label_goals = QLabel("Incomplete Goals")
        self.layout_main.addWidget(
            self.label_goals,
            alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )

        # ================================= Scroll Area ========================

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.widget_scroll = QWidget()
        self.layout_scroll = QVBoxLayout()
        self.widget_scroll.setLayout(self.layout_scroll)
        self.scroll_area.setWidget(self.widget_scroll)
        self.layout_main.addWidget(self.scroll_area)

        self.insert_goals()

    def insert_goals(self):
        goals = db_real_all_goals()
        for goal in goals:
            id = goal["id"]
            container = ContainerGoal(id)
            self.layout_scroll.addWidget(container)


def main():
    app = QApplication(sys.argv)
    window = IncompleteGoals()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
