import sys
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt
from appmain.features.home.home_containers.incomplete_goals import IncompleteGoals
from appmain.features.home.home_containers.heatmap import MonthHeatmap
from appmain.features.home.home_containers.today_activities import TodayActivities
from pathlib import Path


class Home(QWidget):
    def __init__(self, parent=None):
        # ================================ Boilerplate =======================

        super().__init__(parent)
        self.setObjectName("Home")
        self.layout_main = QVBoxLayout(self)

        self.label_home = QLabel("󰋜")
        self.label_home.setObjectName("label_home")
        self.layout_main.addWidget(
            self.label_home,
            alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
            stretch=0,
        )
        self.layout_main.addStretch(1)
        self.button_skills = QPushButton("󰈸")
        self.button_skills.setObjectName("button_skills")
        self.layout_main.addWidget(
            self.button_skills,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )
        self.label_skills = QLabel("Skills")
        self.label_skills.setObjectName("label_skills")
        self.layout_main.addWidget(
            self.label_skills,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )

        self.layout_bottom = QHBoxLayout()
        self.layout_main.addLayout(self.layout_bottom, stretch=3)

        # ======================= Incomplete goals =========================

        self.INCOMPLETEGOALS = IncompleteGoals()
        self.INCOMPLETEGOALS.setObjectName("IncompleteGoals")

        self.frame_incomplete_goals = QFrame()
        self.frame_incomplete_goals.setObjectName("frame_incomplete_goals")

        self.layout_frame_incomplete = QVBoxLayout(self.frame_incomplete_goals)
        self.layout_frame_incomplete.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_incomplete.addWidget(self.INCOMPLETEGOALS)

        self.layout_bottom.addWidget(self.frame_incomplete_goals, stretch=1)

        # ======================= Today activities =========================

        self.TODAYACTIVITIES = TodayActivities()
        self.TODAYACTIVITIES.setObjectName("TodayActivities")

        self.frame_today = QFrame()
        self.frame_today.setObjectName("frame_today")

        self.layout_frame_today = QVBoxLayout(self.frame_today)
        self.layout_frame_today.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_today.addWidget(self.TODAYACTIVITIES)

        self.layout_bottom.addWidget(self.frame_today, stretch=1)

        # ======================== Month heatmap ============================

        self.MONTHHEATMAP = MonthHeatmap()
        self.MONTHHEATMAP.setObjectName("Heatmap")

        self.frame_heatmap = QFrame()
        self.frame_heatmap.setObjectName("frame_heatmap")

        self.layout_frame_heatmap = QVBoxLayout(self.frame_heatmap)
        self.layout_frame_heatmap.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_heatmap.addWidget(self.MONTHHEATMAP)

        self.layout_bottom.addWidget(self.frame_heatmap, stretch=1)

        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)


def main():
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
