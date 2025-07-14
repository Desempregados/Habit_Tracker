from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFontDatabase, QIcon
from appmain.features.skill_master.skills_master_widget import SkillsMaster
from appmain.database.create import db_create
from appmain.assets import get_path_asset
from pathlib import Path
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainWindow")

        self.setWindowTitle("Skills Tracker")
        self.SKILLS_MASTER = SkillsMaster()
        self.setCentralWidget(self.SKILLS_MASTER)
        self.fonts = {}
        self.load_fonts()
        self.load_icon()

        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "main_window.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    def load_fonts(self):
        fonts_to_load = ["Roboto.ttf", "UbuntuNerd.ttf"]

        path_ui = get_path_asset(f"fonts/{fonts_to_load[0]}")
        path_nerd = get_path_asset(f"fonts/{fonts_to_load[1]}")

        font_id_ui = QFontDatabase.addApplicationFont(str(path_ui))
        font_id_nerd = QFontDatabase.addApplicationFont(str(path_nerd))

        family_ui = QFontDatabase.applicationFontFamilies(font_id_ui)[0]
        self.fonts["UI"] = family_ui

        family_nerd = QFontDatabase.applicationFontFamilies(font_id_nerd)[0]
        self.fonts["nerd"] = family_nerd

    def load_icon(self):
        icon_path = get_path_asset("icons/Arch.png")
        icon = QIcon(str(icon_path))
        self.setWindowIcon(icon)


def main():
    db_create()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
