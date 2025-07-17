import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QApplication,
    QComboBox,
)
from PyQt6.QtCore import Qt
from appmain.database.read import db_read_goal_by_skill
from pathlib import Path


class RestartChronometerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RestartDialog")
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)

        self.label_ask = QLabel("Restart Without Submit?")
        self.label_ask.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_ask)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        self.layout_buttons.addStretch(1)

        self.button_yes = QPushButton("")
        self.button_yes.setObjectName("button_yes")
        self.layout_buttons.addWidget(self.button_yes)
        self.layout_buttons.addStretch(1)

        self.button_no = QPushButton("")
        self.button_no.setObjectName("button_no")
        self.layout_buttons.addWidget(self.button_no)

        self.layout_buttons.addStretch(1)
        self.layout_main.addStretch(1)

        self.button_yes.clicked.connect(self.accept)
        self.button_no.clicked.connect(self.reject)


class SubmitChronometerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SubmitDialog")
        self.goal_id = 0
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)

        # ================ label ask ============================

        self.label_ask = QLabel("Submit time to wich goal?")
        self.label_ask.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_ask)

        # ================ Combo box goals ======================

        self.combo_box_goals = QComboBox()
        self.combo_box_goals.setObjectName("combo_box_goals")
        self.layout_main.addWidget(self.combo_box_goals)
        self.combo_box_goals.addItem("no goal", 0)

        # ================ Layout buttons =======================

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        self.layout_buttons.addStretch(1)

        # ================ Button yes ============================

        self.button_yes = QPushButton("")
        self.button_yes.setObjectName("button_yes")
        self.layout_buttons.addWidget(self.button_yes)
        self.layout_buttons.addStretch(1)

        # ================ Button no ============================

        self.button_no = QPushButton("")
        self.button_no.setObjectName("button_no")
        self.layout_buttons.addWidget(self.button_no)

        self.layout_buttons.addStretch(1)
        self.layout_main.addStretch(1)

        # =============== connections ============================

        self.button_yes.clicked.connect(self.accept_action)
        self.button_no.clicked.connect(self.reject)

        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_skill.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    def load_goals(self, skill_id: int):
        goals = db_read_goal_by_skill(skill_id)
        for goal in goals:
            item = (goal["goal_name"], goal["id"])
            self.combo_box_goals.addItem(item[0], item[1])

    def accept_action(self):
        self.goal_id = self.combo_box_goals.currentData()
        self.accept()


def main():
    app = QApplication(sys.argv)
    window = SubmitChronometerDialog()
    window.load_goals(18)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
