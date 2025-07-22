import sys
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from pathlib import Path


class CreationMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.setObjectName("CreationMain")

        # ======================== Label Name ==============================

        self.label_name = QLabel("Name")
        self.label_name.setObjectName("label_name")
        self.layout_main.addWidget(
            self.label_name,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )

        # ========================= Line Edit habit description =============

        self.linedit_name = QLineEdit()
        self.linedit_name.setObjectName("linedit_name")
        self.layout_main.addWidget(
            self.linedit_name, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1
        )

        # ========================= Quantificators Label ======================

        self.label_quantificators = QLabel("Quantificators")
        self.label_quantificators.setObjectName("label_quantificators")
        self.layout_main.addWidget(
            self.label_quantificators, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1
        )

        # ========================== Layout Quantificators ===================

        self.layout_quantificators = QHBoxLayout()
        self.layout_main.addLayout(self.layout_quantificators, stretch=1)
        self.layout_quantificators.addStretch(1)

        # ========================== Button Time ==============================

        self.button_time = QPushButton("Time")
        self.button_time.setObjectName("button_time")
        self.layout_quantificators.addWidget(self.button_time, stretch=1)

        # =========================== Button Quantity =========================

        self.button_quantity = QPushButton("Quantity")
        self.button_quantity.setObjectName("button_quantity")
        self.layout_quantificators.addWidget(self.button_quantity, stretch=1)

        # =========================== Button Marks ============================

        self.button_marks = QPushButton("Marks")
        self.button_marks.setObjectName("button_marks")
        self.layout_quantificators.addWidget(self.button_marks, stretch=1)

        self.layout_quantificators.addStretch(1)

        # =========================== Button Complete ==========================

        self.button_complete = QPushButton("Complete")
        self.button_complete.setObjectName("button_complete")
        self.layout_main.addWidget(
            self.button_complete, alignment=Qt.AlignmentFlag.AlignRight, stretch=1
        )

        # ============================ Button Cancel ============================

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setObjectName("button_cancel")
        self.layout_main.addWidget(
            self.button_cancel, alignment=Qt.AlignmentFlag.AlignLeft, stretch=1
        )

        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)


def main():
    app = QApplication(sys.argv)
    window = CreationMain()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
