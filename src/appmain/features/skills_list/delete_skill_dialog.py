import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QApplication,
)
from PyQt6.QtCore import Qt


class ConfirmDeleteSkill(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)

        self.label_confim = QLabel("Delete skill permanently?")
        self.label_confim.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_confim)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        self.button_confirm = QPushButton("Yes")
        self.button_cancel = QPushButton("No")
        self.layout_buttons.addWidget(self.button_confirm)
        self.layout_buttons.addWidget(self.button_cancel)

        self.button_confirm.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)


def main():
    app = QApplication(sys.argv)
    window = ConfirmDeleteSkill()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
