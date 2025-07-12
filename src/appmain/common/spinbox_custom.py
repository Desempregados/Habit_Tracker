import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QSpinBox,
    QVBoxLayout,
    QAbstractSpinBox,
    QPushButton,
    QHBoxLayout,
)

from PyQt6.QtGui import QWheelEvent
from PyQt6.QtCore import pyqtSignal, Qt


class CSpinBox(QSpinBox):
    scrollup = pyqtSignal()
    scrolldown = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.scrollup.emit()
        else:
            self.scrolldown.emit()
        event.accept()


class CustomSpinBoxWidget(QWidget):
    def __init__(self, parent=None):
        # ================= Boilerplate arrows spinbox ===================

        super().__init__(parent)
        self.setProperty("class", "CustomSpinBox")

        self.layout_main = QHBoxLayout(self)
        # ================= Layout items ======================

        self.layout_main.addStretch(1)
        self.layout_items = QVBoxLayout()
        self.layout_main.addLayout(self.layout_items)

        # ================= button up ==========================

        self.layout_items.addStretch(1)
        self.button_up = QPushButton("")
        self.button_up.setObjectName("button_up")
        self.layout_items.addWidget(self.button_up)

        # ================= No arrows spinbox ===================

        self.spin_box = CSpinBox()
        self.layout_items.addWidget(self.spin_box)
        self.spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        # ================= button down ==========================

        self.button_down = QPushButton("")
        self.button_down.setObjectName("button_down")
        self.layout_items.addWidget(self.button_down)
        self.layout_items.addStretch(1)
        self.layout_main.addStretch(1)

        self.setConnections()

    def setConnections(self):
        self.button_up.clicked.connect(self.increase_value)
        self.button_down.clicked.connect(self.decrease_value)
        self.spin_box.scrollup.connect(self.increase_value)
        self.spin_box.scrolldown.connect(self.decrease_value)

    def increase_value(self):
        self.spin_box.stepUp()
        self.spin_box.lineEdit().deselect()

    def decrease_value(self):
        self.spin_box.stepDown()
        self.spin_box.lineEdit().deselect()

    def setMaximun(self, n: int):
        self.spin_box.setMaximum(n)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomSpinBoxWidget()
    window.show()
    sys.exit(app.exec())
