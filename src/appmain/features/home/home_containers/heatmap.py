import sys
from PyQt6.QtWidgets import QCalendarWidget, QApplication


class IncompleteGoals(QCalendarWidget):
    def __init__(self, parent=None):
        # ================================ Boilerplate =======================

        super().__init__(parent)


def main():
    app = QApplication(sys.argv)
    window = IncompleteGoals()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
