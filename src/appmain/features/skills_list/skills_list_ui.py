import sys
from appmain.database.database import *
from appmain.features.skills_list.create_skill_dialog import CreateSkill
from appmain.features.skills_list.delete_skill_dialog import ConfirmDeleteSkill
from appmain.features.skills_list.rename_skill_dialog import RenameSkill
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMenu,
    QHBoxLayout,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction


class SkillsListUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_item_id = None

        # main layout
        self.layout_principal = QVBoxLayout(self)

        # QListWidget setup
        self.lista_widget = QListWidget()
        self.layout_principal.addWidget(self.lista_widget)

        # Layout Buttons
        self.layout_buttons = QHBoxLayout()
        self.layout_principal.addLayout(self.layout_buttons)
        self.layout_buttons.addStretch(3)

        # Create skill button
        self.button_create = QPushButton("New")
        self.layout_buttons.addWidget(self.button_create)
        self.button_create.clicked.connect(self.new_skill)

        # Delete skill button
        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.confirm_delete)
        self.layout_buttons.addStretch(1)
        self.layout_buttons.addWidget(self.button_delete)
        self.layout_buttons.addStretch(3)

        self.lista_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.lista_widget.customContextMenuRequested.connect(self.context_menu_open)

        self.lista_widget.currentItemChanged.connect(self.get_current_item_id)
        self.load_skills()

    # Show all skills function
    def load_skills(self):
        self.lista_widget.clear()
        skills_list = db_obtain_all_skills()

        self.lista_widget.setUpdatesEnabled(False)
        try:
            for skill in skills_list:
                item = QListWidgetItem(skill["name"])
                item.setData(Qt.ItemDataRole.UserRole, skill["id"])

                self.lista_widget.addItem(item)
        finally:
            self.lista_widget.setUpdatesEnabled(True)

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
        clicked_item = self.lista_widget.itemAt(position)

        if clicked_item:
            menu = QMenu(self)
            rename_action = menu.addAction("rename")
            rename_action.triggered.connect(self.rename_skill)
            menu.exec(self.lista_widget.mapToGlobal(position))


def main():
    app = QApplication(sys.argv)
    window = SkillsListUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
