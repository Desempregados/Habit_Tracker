import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QDialog,
)
from PyQt6.QtCore import Qt
from appmain.common.shadows import AppShadows
from appmain.features.pomodoro.pomothread import Perfil_pomodoro
from appmain.features.pomodoro.configwindow import ConfigWindow
from appmain.common.animations import AnimationsPulse
from appmain.database.database import *
from appmain import assets


class PomodoroUI(QWidget):
    def __init__(self, parent=None):
        # =============== Boilerplate ========================

        super().__init__(parent)
        self.layout_principal = QVBoxLayout(self)
        self.p1 = Perfil_pomodoro()
        self.setObjectName("Pomodoro")

        # ================= Button back ====================

        self.layout_button_back = QHBoxLayout()
        self.layout_principal.addLayout(self.layout_button_back)

        self.button_back = QPushButton("")
        self.layout_button_back.addWidget(self.button_back)
        self.layout_button_back.addStretch(1)

        # ================= Label skill name ===============

        self.label_skill_name = QLabel("Skill Name")
        self.layout_principal.addWidget(self.label_skill_name)
        self.label_skill_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_skill_name.setStyleSheet(
            "font-size:30px; font-weight:bold; color:white;"
        )

        # ================= time label =====================

        self.shadow1 = AppShadows((0, 255, 159), 35)

        self.label_tempo = QLabel(f"{self.p1.form_time(self.p1.left_time)}", self)

        self.label_tempo.setGraphicsEffect(self.shadow1)
        self.layout_principal.addStretch(1)
        self.layout_principal.addWidget(self.label_tempo)

        # ================= Cycle Stage label ==============

        self.label_cycle_stage = QLabel(f"{self.p1.current_cycle}")
        self.shadow2 = AppShadows((0, 255, 159), 35)
        self.label_cycle_stage.setGraphicsEffect(self.shadow2)
        self.layout_principal.addWidget(self.label_cycle_stage)

        # ============= buttons (play, restart, skip)=======

        self.layout_botoes = QHBoxLayout()

        self.button_play = QPushButton("Start")
        self.button_reset = QPushButton("Restart")
        self.button_skip = QPushButton("Skip")

        self.layout_botoes.addStretch(5)
        self.layout_botoes.addWidget(self.button_play)

        self.layout_botoes.addStretch(1)
        self.layout_botoes.addWidget(self.button_reset)

        self.layout_botoes.addStretch(1)
        self.layout_botoes.addWidget(self.button_skip)
        self.layout_botoes.addStretch(5)

        self.layout_principal.addStretch(1)
        self.layout_principal.addLayout(self.layout_botoes)
        self.layout_principal.addStretch(3)

        # ====================== Settings Button ===========================

        self.layout_button_settings = QHBoxLayout()
        self.button_settings = QPushButton()
        self.button_settings.setObjectName("Settingsbutton")
        self.layout_button_settings.addStretch(1)
        self.layout_button_settings.addWidget(self.button_settings)
        self.layout_button_settings.addStretch(1)
        self.layout_principal.addLayout(self.layout_button_settings)
        self.layout_principal.addStretch(3)

        # ====================== Cycle numbers =============================

        self.current_tracker_layout = QHBoxLayout()
        self.label_current_cycle = QLabel(f"0/{self.p1.len_cycle}")
        self.label_current_cycle.setObjectName("Currentcycle")
        self.current_tracker_layout.addStretch(1)
        self.current_tracker_layout.addWidget(self.label_current_cycle)
        self.current_tracker_layout.addStretch(1)
        self.layout_principal.addLayout(self.current_tracker_layout)
        self.layout_principal.addStretch(2)

        # ====================== Message Box ================================

        self.warning_end_cycle = QMessageBox(self)
        self.warning_end_cycle.setWindowTitle("Warning")
        self.warning_end_cycle.setText("De volta ao trabalho")
        self.warning_end_cycle.setIcon(QMessageBox.Icon.Information)

        self.warning_end_cycle.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.warning_end_cycle.setFixedSize(1000, 1000)

        # ====================== Caling essential functions ================

        self.setUI()
        self.pomo_connect()

    # ========================= CSS Function ===================================

    def setUI(self):
        # ---------- time label ----------------

        self.label_tempo.setStyleSheet(
            "font-size:238px; font-weight:bold; color: white;"
        )
        self.label_tempo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---------- cycle stage label ---------

        self.label_cycle_stage.setStyleSheet(
            """
       #Pomodoro QLabel{
        font-size: 90px ;
        font-weight: bold;
        font-family: Hack;
        color: rgba(0,255,159,0.8);
        }
        """
        )
        self.label_cycle_stage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---------- buttons css ---------------

        self.setStyleSheet(
            f"""
        #Pomodoro {{
        background-color:rgba(30,30,30,1);
        }}
        #Pomodoro QLabel#Currentcycle{{
        color:white;
        }}
       #Pomodoro QPushButton{{
            color:white;
            font-size: 52px;
            font-family: Hack;
            padding:10px;
            border-radius:16px;
            border:4px solid rgba(200,130,255,1);
            background-color:rgba(0,255,159,0.4);
            font-weight: bold ;
            }}
       #Pomodoro QPushButton:hover{{
            background-color: rgba(0,255,159,0.6) ;
            }}
       #Pomodoro QPushButton:pressed {{
            background-color:rgba(0,255,159, 0.8);
        }}
       #Pomodoro QPushButton:focus {{
        outline: none;
        }}
       #Pomodoro QPushButton#Settingsbutton {{
        image:url({str(assets.get_path_asset("icons/settings.svg"))});
        padding:6px;
        font-size:30px;
        }}
        """
        )

        # ------------- Current cycle label ------------

        self.label_current_cycle.setStyleSheet(
            """
       #Pomodoro QLabel{
            font-weight:bold;
            font-size:70px;
            font-family:Hack;
            border:2px solid rgba(0,255, 159, 1);
            border-radius:33px;
            background-color:rgba(190,130,255, 0.2);
            padding:6px;
        }
        """
        )
        self.label_current_cycle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ----------- Message Box ------------------------

        self.warning_end_cycle.setStyleSheet(
            """
                                             QMessageBox{
                                             background-color:rgba(20,20,20,1);
                                             }
                                             QMessageBox QLabel {
                                             font-size:24px;
                                             font-weight:bold;
                                             color:white;
                                             }
                                             QMessageBox QPushButton{
                                             font-size:20px;
                                             font-weight:bold;
                                             background-color:rgba(40,40,40,1);
                                             border:2px solid rgb(0,255,159);
                                             border-radius:4px;
                                             }
                                             QDialogButtonBox{
                                             qproperty-centerButtons: true;
                                             }
                                             """
        )

    # ============ Connections ============================

    def pomo_connect(self):
        self.button_play.clicked.connect(self.click_start)
        self.button_reset.clicked.connect(self.click_restart)
        self.button_skip.clicked.connect(self.click_skip)
        self.button_settings.clicked.connect(self.open_settings)
        self.p1.sinal_tempo.connect(self.label_tempo.setText)
        self.p1.sinal_parar_tempo.connect(self.end_cycle)
        self.p1.sinal_current_cycle.connect(self.label_current_cycle.setText)

    # ============= Start Button ==========================

    def click_start(self):
        self.animation_pulse_button(self.button_play)
        if self.button_play.text() == "Start":
            self.p1.pomo_start()
            self.button_play.setText("Pause")

        elif self.button_play.text() == "Pause":
            self.p1.pomo_pause()
            self.button_play.setText("Start")

    # ============== Restart Button actions =======================

    def click_restart(self):
        self.animation_pulse_button(self.button_reset)
        if self.button_play.text() == "Pause":
            self.p1.pomo_pause()
            self.button_play.setText("Start")
        self.p1.pomo_restart()
        self.label_tempo.setText(f"{self.p1.form_time(self.p1.left_time)}")

    # =============== Skip Button actions =============================

    def click_skip(self):
        self.animation_pulse_button(self.button_skip)
        self.p1.pomo_skip()
        self.p1.pomo_pause()
        self.label_cycle_stage.setText(self.p1.current_cycle)
        self.button_play.setText("Start")

    # =============== End cycle function ===================

    def end_cycle(self):
        self.button_play.setText("Start")
        self.label_cycle_stage.setText(self.p1.current_cycle)

        if self.label_cycle_stage.text() == "Short Break":
            self.warning_end_cycle.setText("Time for a quick rest")
            self.warning_end_cycle.exec()

        elif self.label_cycle_stage.text() == "Long Break":
            self.warning_end_cycle.setText("Time for a long rest")
            self.warning_end_cycle.exec()

        else:
            self.warning_end_cycle.setText("Get back to work!!")
            self.warning_end_cycle.exec()

    # =============== Settings option =========================

    def open_settings(self):
        self.animation_pulse_button(self.button_settings, (40, 20), 150)
        self.window_settings = ConfigWindow(self)

        result = self.window_settings.exec()

        if result == QDialog.DialogCode.Accepted:
            settings = self.window_settings.get_settings()
            self.p1.pomo_profile_change(
                settings["work"],
                settings["short_break"],
                settings["long_break"],
                settings["cylcles_number"],
            )
            self.click_restart()
            self.label_current_cycle.setText(
                f"{(self.p1.completed_cycles - 1) % self.p1.len_cycle}/{self.p1.len_cycle}"
            )

    def animation_pulse_button(
        self, button: QPushButton, delta: tuple[int, int] = (30, 15), duration: int = 30
    ):
        self.animation_button = AnimationsPulse(button, delta, duration)
        button.setEnabled(False)
        self.animation_button.start()
        self.animation_button.finished.connect(lambda: button.setEnabled(True))

    def set_text_skill_name(self, id: int):
        skill_name = db_obtain_skill_by_id(id)
        self.label_skill_name.setText(skill_name)


# ============== Boilerplate ==============================


def main():
    app = QApplication(sys.argv)
    window = PomodoroUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
