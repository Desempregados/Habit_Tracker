import sys
from appmain.features.skills_list.skills_list_ui import SkillsListUI
from appmain.features.skill_interface.skill_interface import SkillInterface
from appmain.features.chronometer.chronometer_widget import ChronometerUI
from appmain.features.goals.goals_widget import GoalsUI
from appmain.features.home.home_widget import Home
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QStackedWidget,
)


class SkillsMaster(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.stacked_main = QStackedWidget()
        self.layout_main.addWidget(self.stacked_main)
        self.WIDGET_skills_list = SkillsListUI(self)
        self.WIDGET_skill_interface = SkillInterface(self)
        self.WIDGET_chronometer = ChronometerUI(self)
        self.WIDGET_goals = GoalsUI()
        self.WIDGET_home = Home()
        self.stacked_main.addWidget(self.WIDGET_home)
        self.stacked_main.addWidget(self.WIDGET_skills_list)
        self.stacked_main.addWidget(self.WIDGET_skill_interface)
        self.stacked_main.addWidget(self.WIDGET_chronometer)
        self.stacked_main.addWidget(self.WIDGET_goals)

        self.WIDGET_skills_list.list_widget.doubleClicked.connect(
            self.go_to_skill_interface
        )
        self.WIDGET_skills_list.button_back.clicked.connect(self.go_home)
        self.WIDGET_skill_interface.button_back.clicked.connect(self.go_to_skills_list)
        self.WIDGET_skill_interface.button_clock.clicked.connect(self.go_to_chronometer)
        self.WIDGET_skill_interface.button_goal.clicked.connect(self.go_to_goals)
        self.WIDGET_chronometer.button_back.clicked.connect(self.go_to_skill_interface)
        self.WIDGET_goals.button_back.clicked.connect(self.go_to_skill_interface)
        self.WIDGET_home.button_skills.clicked.connect(self.go_to_skills_list)
        self.setStyleSheet("background-color:rgba(30, 30, 30, 1);")

    def go_home(self):
        self.stacked_main.setCurrentIndex(0)

    def go_to_skills_list(self):
        self.stacked_main.setCurrentIndex(1)

    def go_to_skill_interface(self):
        current_skill_id = self.WIDGET_skills_list.current_item_id
        self.WIDGET_skill_interface.load_skill_data(current_skill_id)
        self.stacked_main.setCurrentIndex(2)

    def go_to_chronometer(self):
        current_skill_id = self.WIDGET_skills_list.current_item_id
        self.WIDGET_chronometer.load_skill_id(current_skill_id)
        self.stacked_main.setCurrentIndex(3)

    def go_to_goals(self):
        current_skill_id = self.WIDGET_skills_list.current_item_id
        self.WIDGET_goals.load_skill_data(current_skill_id)
        self.stacked_main.setCurrentIndex(4)


def main():
    app = QApplication(sys.argv)
    window = SkillsMaster()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
