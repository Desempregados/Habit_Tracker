from PyQt6.QtWidgets import QApplication
import sys

from appmain.features.timer.timer_dialog import TemporizadorDialog


def main():
    app = QApplication(sys.argv)
    window = TemporizadorDialog()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
