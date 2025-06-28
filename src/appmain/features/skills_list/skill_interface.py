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
)
from PyQt6.QtCore import Qt


class SkillInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SkillsInterface")

        self.layout_main = QVBoxLayout(self)

        self.layout_button_back = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button_back)
        self.button_back = QPushButton("")
        self.button_back.setObjectName("button_back")
        self.layout_button_back.addWidget(self.button_back)
        self.layout_button_back.addStretch(2)

        self.label_skill_name = QLabel("Skill Name")
        self.label_skill_name.setObjectName("label_skill_name")
        self.label_skill_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill_name)

        self.layout_button_clock = QHBoxLayout()
        self.layout_button_clock.addStretch(1)
        self.layout_main.addLayout(self.layout_button_clock)
        self.button_clock = QPushButton("")
        self.button_clock.setObjectName("button_clock")
        self.layout_button_clock.addWidget(self.button_clock)
        self.layout_button_clock.addStretch(1)

        self.label_skill_dedicated_time = QLabel("Dedicated Time")
        self.label_skill_dedicated_time.setObjectName("dedicated_time")
        self.label_skill_dedicated_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill_dedicated_time)

        self.Load_stylesheet()

    def Load_stylesheet(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_skill.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    def load_skill_data(self, item_id: int):
        skill_name = db_obtain_skill_by_id(item_id)
        skill_dedicated_time = db_obtain_dedicated_time(item_id, 7)
        formated_dedicated_time = self.form_time(skill_dedicated_time)

        self.label_skill_name.setText(skill_name)
        self.label_skill_dedicated_time.setText(
            f"Dedicated time in the last seven days:\n{formated_dedicated_time}"
        )

    def form_time(self, s: int) -> str:
        return f"{int(s // 60):02d}:{int(s % 60):02d}"


def main():
    app = QApplication(sys.argv)
    window = SkillInterface()
    window.load_skill_data(2)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
