import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QApplication,
    QLineEdit,
)
from PyQt6.QtCore import Qt
from pathlib import Path


class CreateSkill(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CreateSkillDialog")
        self.setWindowTitle("Create Skill")
        self.setMinimumWidth(250)
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)

        self.label_skill_name = QLabel("Skill Name")
        self.label_skill_name.setObjectName("label_skill_name")
        self.label_skill_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill_name)

        self.layout_main.addStretch(2)
        self.linedit_skill_name = QLineEdit()
        self.linedit_skill_name.setObjectName("linedit_skill_name")
        self.layout_main.addWidget(self.linedit_skill_name)
        self.layout_main.addStretch(3)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addStretch(2)
        self.layout_main.addLayout(self.layout_buttons)

        self.button_create = QPushButton("")
        self.button_create.setObjectName("button_new")
        self.layout_buttons.addWidget(self.button_create)
        self.button_cancel = QPushButton("")
        self.button_cancel.setObjectName("button_cancel")
        self.layout_buttons.addWidget(self.button_cancel)

        self.button_create.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.Load_stylesheet()

    def Load_stylesheet(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_skill.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    def get_text(self):
        return self.linedit_skill_name.text()


def main():
    app = QApplication(sys.argv)
    app.setCursorFlashTime(0)
    window = CreateSkill()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
