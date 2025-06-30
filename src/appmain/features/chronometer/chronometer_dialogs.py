import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QApplication,
)
from PyQt6.QtCore import Qt


class RestartChronometerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)

        self.label_ask = QLabel("Submit before restart?")
        self.label_ask.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_ask)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        self.layout_buttons.addStretch(1)

        self.button_yes = QPushButton("Yes")
        self.layout_buttons.addWidget(self.button_yes)

        self.button_no = QPushButton("No")
        self.layout_buttons.addWidget(self.button_no)

        self.button_cancel = QPushButton("Cancel")
        self.layout_buttons.addWidget(self.button_cancel)

        self.layout_buttons.addStretch(1)
        self.layout_main.addStretch(1)

        self.button_yes.clicked.connect(self.accept)
        self.button_no.clicked.connect(self.reject)
        self.button_cancel.clicked.connect(lambda: self.done(2))


class SubmitChronometerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.layout_main.addStretch(1)

        self.label_ask = QLabel("Submit Time?")
        self.label_ask.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_ask)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        self.layout_buttons.addStretch(1)

        self.button_yes = QPushButton("Yes")
        self.layout_buttons.addWidget(self.button_yes)

        self.button_no = QPushButton("No")
        self.layout_buttons.addWidget(self.button_no)

        self.layout_buttons.addStretch(1)
        self.layout_main.addStretch(1)

        self.button_yes.clicked.connect(self.accept)
        self.button_no.clicked.connect(self.reject)


def main():
    app = QApplication(sys.argv)
    window = SubmitChronometerDialog()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
