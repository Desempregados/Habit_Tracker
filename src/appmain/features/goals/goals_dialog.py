import sys
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)
from pathlib import Path
from appmain.common.spinbox_custom import CustomSpinBoxWidget


class NewGoalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NewGoalDialog")

        self.layout_main = QVBoxLayout(self)
        self.value = None
        self.name = None

        # ==================== Line edit name ======================

        self.linedit_name = QLineEdit()
        self.layout_main.addWidget(self.linedit_name)
        self.linedit_name.setPlaceholderText("Name")

        # ====================  Spin box values =====================

        self.layout_values = QHBoxLayout()
        self.layout_values.setContentsMargins(0, 0, 0, 0)
        self.layout_main.addLayout(self.layout_values)
        self.layout_values.addStretch(1)

        # ==================== Spin box hours =======================

        self.spin_box_hours = CustomSpinBoxWidget()
        self.label_dots1 = QLabel(":")
        self.layout_values.addWidget(self.spin_box_hours)
        self.layout_values.addWidget(self.label_dots1)

        # ==================== Spin box minutes =======================

        self.spin_box_minutes = CustomSpinBoxWidget()
        self.label_dots2 = QLabel(":")
        self.spin_box_minutes.setMaximun(59)
        self.layout_values.addWidget(self.spin_box_minutes)
        self.layout_values.addWidget(self.label_dots2)

        # ==================== Spin box seconds =======================

        self.spin_box_seconds = CustomSpinBoxWidget()
        self.spin_box_seconds.setMaximun(59)
        self.layout_values.addWidget(self.spin_box_seconds)
        self.layout_values.addStretch(1)

        # ==================== Layout Buttons ======================

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addStretch(1)
        self.layout_main.addLayout(self.layout_buttons)

        # ===================== Button confirm =====================

        self.button_confirm = QPushButton("")
        self.button_confirm.setObjectName("button_confirm")
        self.layout_buttons.addWidget(self.button_confirm)
        self.button_confirm.clicked.connect(lambda: self.check_accept())

        # ====================== Button cancel ======================

        self.button_cancel = QPushButton("")
        self.button_cancel.setObjectName("button_cancel")
        self.layout_buttons.addWidget(self.button_cancel)
        self.layout_buttons.addStretch(1)
        self.button_cancel.clicked.connect(self.reject)

        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_goals.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    def check_accept(self):
        self.name = str(self.linedit_name.text())
        hours = int(self.spin_box_hours.spin_box.value() * 3600)
        minutes = int(self.spin_box_minutes.spin_box.value() * 60)
        seconds = int(self.spin_box_seconds.spin_box.value())
        self.value = hours + minutes + seconds

        if (len(self.name) > 0) and (self.value > 0):
            print(self.value)
            self.accept()

        else:
            print("not valid")

    def get_inputs(self):
        name = str(self.name)
        value = int(self.value)

        return (name, value)


def main():
    app = QApplication(sys.argv)
    window = NewGoalDialog()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
