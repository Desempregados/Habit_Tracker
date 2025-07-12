import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QDialog,
    QStatusBar,
)
from PyQt6.QtCore import Qt
from appmain.database.database import *
from appmain.features.chronometer.chronometer_logic import ChronometerLogic
from appmain.common.clickable_label import ClickableLabel
from appmain.features.chronometer.chronometer_dialogs import (
    RestartChronometerDialog,
    SubmitChronometerDialog,
)


class ChronometerUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ============ Boilerplate ==================

        self.setObjectName("ChronometerUI")

        self.skill_id = None

        self.label_mode = 0

        self.CHRONOMETER_LOGIC = ChronometerLogic()

        self.layout_main = QVBoxLayout(self)

        # =========== Back button =======================

        self.layout_button_back = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button_back)
        self.button_back = QPushButton("")
        self.button_back.setObjectName("button_back")
        self.layout_button_back.addWidget(self.button_back)
        self.layout_button_back.addStretch(1)
        self.layout_main.addStretch(3)

        # ============= Skill name label ==================

        self.label_skill = QLabel("Skill Name")
        self.label_skill.setObjectName("label_skill_name")
        self.label_skill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_skill)

        # ============== Time label ========================

        self.label_time = ClickableLabel("00:00:00")
        self.label_time.setObjectName("label_time")
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_time)
        self.label_time.clicked.connect(lambda: self.click_label())

        self.layout_main.addStretch(3)

        # =============== Buttons layout ====================

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        self.layout_buttons.addStretch(1)

        # ================= Button restart ==================

        self.button_restart = QPushButton("󰜉")
        self.button_restart.setObjectName("button_restart")
        self.layout_buttons.addWidget(self.button_restart)
        self.button_restart.setEnabled(False)

        self.layout_buttons.addStretch(1)
        # ================== Button play ====================

        self.button_start = QPushButton("")
        self.button_start.setObjectName("button_start")
        self.layout_buttons.addWidget(self.button_start)

        self.layout_buttons.addStretch(1)

        # ================== Button submit ===================

        self.layout_submit = QHBoxLayout()
        self.layout_submit.addStretch(1)
        self.layout_main.addLayout(self.layout_submit)

        self.button_submit = QPushButton("")
        self.button_submit.setObjectName("button_submit")
        self.layout_submit.addWidget(self.button_submit)
        self.layout_submit.addStretch(1)
        self.button_submit.setEnabled(False)

        self.layout_main.addStretch(3)

        # =================== Status bar ====================0

        self.statusbar = QStatusBar(self)
        self.layout_main.addWidget(self.statusbar)
        self.statusbar.setObjectName("status_bar")

        # =================== Setup funcions =================

        self.Setup_connections()
        self.Load_qss()

    # ====================== Load qss ==================================

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_skill.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            style_qss = f.read()
            self.setStyleSheet(style_qss)

    # ======================= Load skill id ============================

    def load_skill_id(self, real_skill_id: int):
        self.skill_id = real_skill_id

        self.CHRONOMETER_LOGIC.load_id(real_skill_id)
        self.load_skill_info(real_skill_id)

    # ======================= Load connections ==========================

    def Setup_connections(self):
        self.button_start.clicked.connect(self.play_button)
        self.button_restart.clicked.connect(self.restart_button)
        self.button_submit.clicked.connect(self.submit_button)
        self.CHRONOMETER_LOGIC.signal_update_timer.connect(self.update_time)

    # ======================== Play button actions ======================

    def play_button(self):
        button_text = self.button_start.text()
        if button_text == "":
            self.button_restart.setEnabled(True)
            self.button_submit.setEnabled(True)
            self.CHRONOMETER_LOGIC.start_timer()
            self.button_start.setText("")
        else:
            self.CHRONOMETER_LOGIC.pause_timer()
            self.button_start.setText("")

    # ========================== Load skill info by id ==================

    def load_skill_info(self, skill_id: int):
        skill_name = db_obtain_skill_by_id(skill_id)
        self.label_skill.setText(skill_name)

    # ======================== Keep updating time label ==================

    def update_time(self, current_time: str):
        total_time = db_obtain_dedicated_time(self.skill_id)
        total_time_week = db_obtain_dedicated_time_delta(self.skill_id, 7)
        total_time_today = db_obtain_dedicated_time_delta(self.skill_id, 1)

        if self.label_mode % 4 == 0:
            self.label_time.setText(self.form_time(current_time))

        elif self.label_mode % 4 == 1:
            self.label_time.setText(self.form_time(current_time + total_time_today))

        elif self.label_mode % 4 == 2:
            self.label_time.setText(self.form_time(current_time + total_time_week))

        elif self.label_mode % 4 == 3:
            self.label_time.setText(self.form_time(current_time + total_time))

    # ========================= Restart button actions ===================

    def restart_button(self):
        if self.button_start.text() == "":
            self.play_button()
        dialog = RestartChronometerDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.submit_button()
        elif result == QDialog.DialogCode.Rejected:
            self.button_restart.setEnabled(False)
            self.button_submit.setEnabled(False)
            self.CHRONOMETER_LOGIC.restart_timer()
            self.reset_timer()

    # ========================== submit button actions ====================

    def submit_button(self):
        if self.button_start.text() == "":
            self.play_button()

        dialog = SubmitChronometerDialog(self)
        dialog.load_goals(self.skill_id)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            goal_id = dialog.goal_id
            if goal_id != -1:
                self.CHRONOMETER_LOGIC.add_time_to_goal(goal_id)
            self.CHRONOMETER_LOGIC.submit_time()
            self.button_restart.setEnabled(False)
            self.button_submit.setEnabled(False)
            self.reset_timer()
            self.popup_submited()

    # ========================== show popup ================================

    def popup_submited(self):
        self.statusbar.showMessage("Time submited", 2000)

    # =========================== format time =============================

    def form_time(self, s: int) -> str:
        return f"{int(s // 3600):02d}:{int((s // 60) % 60):02d}:{int(s % 60):02d}"

    # ============================ Click label actions =============================

    def click_label(self):
        self.label_mode += 1
        self.CHRONOMETER_LOGIC.signal_update_timer.emit(
            self.CHRONOMETER_LOGIC.current_time
        )

    # ============================ Reset timer ======================================

    def reset_timer(self):
        self.label_mode = 0
        self.update_time(0)


def main():
    app = QApplication(sys.argv)
    window = ChronometerUI()
    window.load_skill_id(2)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
