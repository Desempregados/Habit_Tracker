import sys
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout
from appmain.features.home.home_containers.incomplete_goals import IncompleteGoals
from appmain.features.home.home_containers.heatmap import MonthHeatmap
from appmain.features.home.home_containers.today_activities import TodayActivities


class Home(QWidget):
    def __init__(self, parent=None):
        # ================================ Boilerplate =======================

        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)
        self.setStyleSheet("background-color:rgb(30,30,30);")

        # ================================ Botton widgets =====================

        self.layout_bottom = QHBoxLayout()
        self.layout_main.addLayout(self.layout_bottom, stretch=1)
        self.INCOMPLETEGOALS = IncompleteGoals()
        self.layout_bottom.addWidget(self.INCOMPLETEGOALS, stretch=1)
        self.TODAYACTIVITIES = TodayActivities()
        self.layout_bottom.addWidget(self.TODAYACTIVITIES, stretch=1)

        self.MONTHHEATMAP = MonthHeatmap()
        self.layout_bottom.addWidget(self.MONTHHEATMAP, stretch=1)


def main():
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
