import sys
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt
from appmain.common.heatmap import Heatmap
from datetime import datetime


class MonthHeatmap(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_month = datetime.now().month
        self.layout_main = QVBoxLayout(self)

        self.label_month = QLabel("This month")
        self.label_month.setObjectName("label_month")
        self.layout_main.addWidget(
            self.label_month,
            alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )
        self.HEATMAP = Heatmap()
        self.HEATMAP.setObjectName("heatmap")
        self.HEATMAP.initCalendar(self.current_month)
        self.layout_main.addWidget(self.HEATMAP)


def main():
    app = QApplication(sys.argv)
    window = MonthHeatmap()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
