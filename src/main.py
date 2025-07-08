from PyQt6.QtWidgets import QApplication
from appmain.features.skill_master.skills_master_widget import SkillsMaster
from appmain.database.database import db_create
import sys


def main():
    db_create()
    app = QApplication(sys.argv)
    window = SkillsMaster()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
