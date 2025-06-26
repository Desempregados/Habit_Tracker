import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QApplication,
)
from PyQt6.QtCore import Qt


class RenameSkill(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)

        self.label_skill_name = QLabel("New Skill Name")
        self.label_skill_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill_name)

        self.layout_main.addStretch(2)
        self.linedit_skill_name = QLineEdit()
        self.layout_main.addWidget(self.linedit_skill_name)
        self.layout_main.addStretch(3)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addStretch(2)
        self.layout_main.addLayout(self.layout_buttons)

        self.button_create = QPushButton("Confirm")
        self.layout_buttons.addWidget(self.button_create)
        self.button_cancel = QPushButton("Cancel")
        self.layout_buttons.addWidget(self.button_cancel)

        self.button_create.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

    def get_text(self):
        return self.linedit_skill_name.text()


def main():
    app = QApplication(sys.argv)
    window = RenameSkill()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
