import sys
from pathlib import Path
from appmain.database.create import db_create_skill
from appmain.database.read import db_obtain_all_skills
from appmain.database.update import db_rename_skill
from appmain.database.delete import db_delete_skill
from appmain.features.skills_list.create_skill_dialog import CreateSkill
from appmain.features.skills_list.delete_skill_dialog import ConfirmDeleteSkill
from appmain.features.skills_list.rename_skill_dialog import RenameSkill
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMenu,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QDialog,
)
from PyQt6.QtCore import Qt


class SkillsListUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SkillsListUI")

        self.current_item_id = None

        # main layout
        self.layout_principal = QVBoxLayout(self)

        self.button_back = QPushButton("")
        self.button_back.setObjectName("button_back")
        self.layout_principal.addWidget(
            self.button_back, alignment=Qt.AlignmentFlag.AlignLeft
        )
        # QListWidget setup
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("list_widget")
        self.layout_principal.addWidget(self.list_widget)

        # Layout Buttons
        self.layout_buttons = QHBoxLayout()
        self.layout_principal.addLayout(self.layout_buttons)
        self.layout_buttons.addStretch(3)

        # Create skill button
        self.button_create = QPushButton("")
        self.button_create.setObjectName("button_create")
        self.layout_buttons.addWidget(self.button_create)
        self.button_create.clicked.connect(self.new_skill)

        # Delete skill button
        self.button_delete = QPushButton("")
        self.button_delete.setObjectName("button_delete")
        self.button_delete.clicked.connect(self.confirm_delete)
        self.layout_buttons.addStretch(1)
        self.layout_buttons.addWidget(self.button_delete)
        self.layout_buttons.addStretch(3)

        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.context_menu_open)

        self.list_widget.currentItemChanged.connect(self.get_current_item_id)
        self.load_skills()
        self.Load_stylesheet()
        self.menu = QMenu(self)

    def Load_stylesheet(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_skill.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    # Show all skills function
    def load_skills(self):
        self.list_widget.clear()
        skills_list = db_obtain_all_skills()

        self.list_widget.setUpdatesEnabled(False)
        try:
            for skill in skills_list:
                item = QListWidgetItem(skill["name"])
                item.setData(Qt.ItemDataRole.UserRole, skill["id"])

                self.list_widget.addItem(item)
        finally:
            self.list_widget.setUpdatesEnabled(True)

    def get_current_item_id(self, new_item, old_item):
        if new_item is not None:
            self.current_item_id = new_item.data(Qt.ItemDataRole.UserRole)

        else:
            self.current_item_id = None

    # QDialog to create a new skill
    def new_skill(self):
        dialog = CreateSkill(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            skill_name = dialog.get_text()
            db_create_skill(skill_name)
            self.load_skills()

    def confirm_delete(self):
        dialog = ConfirmDeleteSkill(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            db_delete_skill(self.current_item_id)
            self.load_skills()

    def rename_skill(self):
        dialog = RenameSkill(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            db_rename_skill(self.current_item_id, dialog.get_text())
            self.load_skills()

    def context_menu_open(self, position):
        clicked_item = self.list_widget.itemAt(position)

        if clicked_item:
            menu = QMenu(self)
            rename_action = menu.addAction("rename")
            rename_action.triggered.connect(self.rename_skill)
            menu.exec(self.list_widget.mapToGlobal(position))


def main():
    app = QApplication(sys.argv)
    window = SkillsListUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
