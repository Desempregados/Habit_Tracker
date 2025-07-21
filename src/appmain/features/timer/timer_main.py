from PyQt6.QtWidgets import QApplication
import sys

from src.appmain.features.timer.timer_dialog import TimerWindow



def main():
    app = QApplication(sys.argv)
    window = TimerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
