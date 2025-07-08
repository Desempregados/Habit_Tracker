import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)

from PyQt6.QtCore import Qt, pyqtSignal
from appmain.common.clickable_label import ClickableLabel
from appmain.database.database import *


class ContainerGoal(QWidget):
    goal_deleted = pyqtSignal()

    def __init__(self, goal_id=None, parent=None):
        # ===================== Boilerplate ===============================

        self.goal_id = goal_id

        super().__init__(parent)
        self.layout_main = QHBoxLayout(self)

        # ===================== Label Skill Type ==========================

        self.label_skill_type = QLabel("")
        self.layout_main.addWidget(self.label_skill_type)

        # ===================== Layout rogress bar =========================

        self.layout_progress = QVBoxLayout()
        self.layout_main.addLayout(self.layout_progress)
        self.layout_progress.addStretch(1)
        # ====================== Label goal name ===========================

        self.label_goal_name = QLabel("Goal name")
        self.layout_progress.addWidget(self.label_goal_name)

        # ====================== Label progress ============================

        self.label_progress = ClickableLabel("00:00:00")
        self.layout_progress.addWidget(self.label_progress)
        self.label_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ====================== Progress bar ===============================

        self.progress_bar = QProgressBar()
        self.layout_progress.addWidget(self.progress_bar)
        self.layout_progress.addStretch(1)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(50)

        # ====================== Layout options =============================

        self.layout_options = QVBoxLayout()
        self.layout_options.addStretch(1)
        self.layout_main.addLayout(self.layout_options)

        # ====================== Button Edit ================================

        self.button_edit = QPushButton("")
        self.layout_options.addWidget(self.button_edit)

        # ====================== Button Delete ===============================

        self.button_delete = QPushButton("")
        self.layout_options.addWidget(self.button_delete)
        self.layout_options.addStretch(1)
        self.button_delete.clicked.connect(lambda: self.delete_goal())

        if goal_id:
            self.load_goal_data(self.goal_id)

    def form_time(self, s: int) -> str:
        return f"{int(s // 3600):02d}:{int((s // 60) % 60):02d}:{int(s % 60):02d}"

    def load_goal_data(self, goal_id: int):
        goal_name = db_read_goal_name(goal_id)
        goal_time = self.form_time(db_read_goal_value(goal_id))
        self.label_goal_name.setText(goal_name)
        self.label_progress.setText(goal_time)

    def delete_goal(self):
        resposta = QMessageBox.question(
            self,
            "Confirmation",
            "delete goal permanently?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if resposta == QMessageBox.StandardButton.Yes:
            db_delete_goal(self.goal_id)
            self.goal_deleted.emit()


def main():
    app = QApplication(sys.argv)
    window = ContainerGoal(4)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
