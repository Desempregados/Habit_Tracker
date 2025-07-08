import sys
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtGui import QIntValidator


class NewGoalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout_main = QVBoxLayout(self)

        # ==================== Line edit name ======================

        self.linedit_name = QLineEdit()
        self.layout_main.addWidget(self.linedit_name)
        self.linedit_name.setPlaceholderText("Name")

        # ==================== Line edit value =====================

        self.linedit_value = QLineEdit()
        self.layout_main.addWidget(self.linedit_value)

        self.validator_integer = QIntValidator()
        self.linedit_value.setValidator(self.validator_integer)
        self.linedit_value.setPlaceholderText("Time goal")

        # ==================== Layout Buttons ======================

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addStretch(1)
        self.layout_main.addLayout(self.layout_buttons)

        # ===================== Button confirm =====================

        self.button_confirm = QPushButton("confirm")
        self.layout_buttons.addWidget(self.button_confirm)
        self.button_confirm.clicked.connect(lambda: self.check_accept())

        # ====================== Button cancel ======================

        self.button_cancel = QPushButton("cancel")
        self.layout_buttons.addWidget(self.button_cancel)
        self.layout_buttons.addStretch(1)
        self.button_cancel.clicked.connect(self.reject)

    def check_accept(self):
        name = str(self.linedit_name.text())
        value = str(self.linedit_value.text())
        if (len(name) > 0) and (len(value) > 0):
            if int(value) > 0:
                self.accept()
            else:
                print("value must be a greater than zero")

        else:
            print("not valid")

    def get_inputs(self):
        name = str(self.linedit_name.text())
        value = int(self.linedit_value.text())

        return (name, value)


def main():
    app = QApplication(sys.argv)
    window = NewGoalDialog()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
