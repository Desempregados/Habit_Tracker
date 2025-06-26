import sys
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QDialog,
)
from PyQt6.QtCore import Qt
from appmain.database.database import *
from appmain.features.chronometer.chronometer_logic import ChronometerLogic
from appmain.features.chronometer.chronometer_dialogs import (
    RestartChronometerDialog,
    SubmitChronometerDialog,
)


class ChronometerUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.skill_id = None

        self.CHRONOMETER_LOGIC = ChronometerLogic()

        self.layout_main = QVBoxLayout(self)

        self.layout_button_back = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button_back)
        self.button_back = QPushButton("back")
        self.layout_button_back.addWidget(self.button_back)
        self.layout_button_back.addStretch(1)

        self.label_skill = QLabel("Skill Name")
        self.label_time = QLabel("00:00")
        self.label_skill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_main.addStretch(3)

        self.layout_main.addWidget(self.label_skill)

        self.layout_main.addStretch(1)

        self.layout_main.addWidget(self.label_time)

        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        self.layout_buttons.addStretch(1)

        self.button_restart = QPushButton("󰜉")
        self.layout_buttons.addWidget(self.button_restart)

        self.button_start = QPushButton("")
        self.layout_buttons.addWidget(self.button_start)

        self.layout_buttons.addStretch(1)

        self.layout_submit = QHBoxLayout()
        self.layout_submit.addStretch(1)
        self.layout_main.addLayout(self.layout_submit)

        self.button_submit = QPushButton("")
        self.layout_submit.addWidget(self.button_submit)
        self.layout_submit.addStretch(1)

        self.label_submited = QLabel("Time commited")
        self.label_submited.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_main.addWidget(self.label_submited)

        self.layout_main.addStretch(3)

        self.Setup_connections()

    def load_skill_id(self, real_skill_id: int):
        self.skill_id = real_skill_id

        self.CHRONOMETER_LOGIC.load_id(real_skill_id)
        self.load_skill_info(real_skill_id)

    def Setup_connections(self):
        self.button_start.clicked.connect(self.play_button)
        self.button_restart.clicked.connect(self.restart_button)
        self.button_submit.clicked.connect(self.submit_button)
        self.CHRONOMETER_LOGIC.signal_update_timer.connect(self.update_time)

    def play_button(self):
        button_text = self.button_start.text()
        if button_text == "":
            self.button_restart.setEnabled(True)
            self.CHRONOMETER_LOGIC.start_timer()
            self.button_start.setText("")
        else:
            self.CHRONOMETER_LOGIC.pause_timer()
            self.button_start.setText("")

    def load_skill_info(self, skill_id: int):
        skill_name = db_obtain_skill_by_id(skill_id)
        self.label_skill.setText(skill_name)

    def update_time(self, formated_time: str):
        self.label_time.setText(formated_time)

    def restart_button(self):
        if self.button_start.text() == "":
            self.play_button()
        dialog = RestartChronometerDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.button_restart.setEnabled(False)
            self.CHRONOMETER_LOGIC.restart_timer()
        elif result == QDialog.DialogCode.Rejected:
            self.button_restart.setEnabled(False)
            self.CHRONOMETER_LOGIC.restart_timer()

    def submit_button(self):
        if self.button_start.text() == "":
            self.play_button()

        dialog = SubmitChronometerDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.CHRONOMETER_LOGIC.submit_time()
            self.button_restart.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = ChronometerUI()
    window.load_skill_id(2)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
