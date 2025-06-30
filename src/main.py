from PyQt6.QtWidgets import QApplication
from appmain.features.skill_master.skills_master_widget import SkillsMaster
import sys


def main():
    app = QApplication(sys.argv)
    window = SkillsMaster()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
