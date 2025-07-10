from PyQt6.QtWidgets import QApplication
from appmain.main_window.main_window import MainWindow
from appmain.database.database import db_create
import sys


def main():
    db_create()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
