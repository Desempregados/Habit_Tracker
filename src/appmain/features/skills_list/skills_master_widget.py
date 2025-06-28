import sys
from appmain.features.skills_list.skills_list_ui import SkillsListUI
from appmain.features.skills_list.skill_interface import SkillInterface
from appmain.features.chronometer.chronometer_widget import ChronometerUI
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
        self.WIDGET_skills_list = SkillsListUI()
        self.WIDGET_skill_interface = SkillInterface()
        self.WIDGET_chronometer = ChronometerUI()
        self.stacked_main.addWidget(self.WIDGET_skills_list)
        self.stacked_main.addWidget(self.WIDGET_skill_interface)
        self.stacked_main.addWidget(self.WIDGET_chronometer)

        self.WIDGET_skills_list.list_widget.doubleClicked.connect(
            self.go_to_skill_interface
        )
        self.WIDGET_skill_interface.button_back.clicked.connect(self.go_to_skills_list)
        self.WIDGET_skill_interface.button_clock.clicked.connect(self.go_to_chronometer)
        self.WIDGET_chronometer.button_back.clicked.connect(self.go_to_skill_interface)
        self.setStyleSheet("background-color:rgba(30, 30, 30, 1);")

    def go_to_skills_list(self):
        self.stacked_main.setCurrentIndex(0)

    def go_to_skill_interface(self):
        current_skill_id = self.WIDGET_skills_list.current_item_id
        self.WIDGET_skill_interface.load_skill_data(current_skill_id)
        self.stacked_main.setCurrentIndex(1)

    def go_to_chronometer(self):
        current_skill_id = self.WIDGET_skills_list.current_item_id
        self.WIDGET_chronometer.load_skill_id(current_skill_id)
        self.stacked_main.setCurrentIndex(2)


def main():
    app = QApplication(sys.argv)
    window = SkillsMaster()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
