from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)
from pathlib import Path
from src.appmain.common.spinbox_custom import CustomSpinBoxWidget  # seu componente customizado


class TimerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NewGoalDialog")

        self.value = 0
        self.timer_running = False


        
        # ================= Qtimer init ====================
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.atualizar_contagem)

        # ================= Layout principal ====================
        self.layout_main = QVBoxLayout(self)

        # ================= Seção de tempo (SpinBoxes) ===============
        self.layout_values = QHBoxLayout()
        self.layout_values.setContentsMargins(0, 0, 0, 0)
        self.layout_values.addStretch(1)

        self.spin_box_hours = CustomSpinBoxWidget()
        self.label_dots1 = QLabel(":")
        self.spin_box_minutes = CustomSpinBoxWidget()
        self.spin_box_minutes.setMaximun(59)
        self.label_dots2 = QLabel(":")
        self.spin_box_seconds = CustomSpinBoxWidget()
        self.spin_box_seconds.setMaximun(59)

        self.layout_values.addWidget(self.spin_box_hours)
        self.layout_values.addWidget(self.label_dots1)
        self.layout_values.addWidget(self.spin_box_minutes)
        self.layout_values.addWidget(self.label_dots2)
        self.layout_values.addWidget(self.spin_box_seconds)
        self.layout_values.addStretch(1)

        self.layout_main.addLayout(self.layout_values)

        # ================= Seção de botões =====================
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addStretch(1)

        self.button_start = QPushButton("Start")  # ícone play
        self.button_start.setObjectName("button_confirm")
        self.button_start.clicked.connect(self.iniciar_timer)
        self.layout_buttons.addWidget(self.button_start)

        self.button_pause = QPushButton("Cancel")  # ícone pause
        self.button_pause.setObjectName("button_cancel")
        self.button_pause.clicked.connect(self.pause_timer)
        self.layout_buttons.addWidget(self.button_pause)

        self.button_reset = QPushButton("Reset")  # ícone reset
        self.button_reset.setObjectName("button_cancel")
        self.button_reset.clicked.connect(self.reset_timer)
        self.layout_buttons.addWidget(self.button_reset)

        self.layout_buttons.addStretch(1)
        self.layout_main.addLayout(self.layout_buttons)

        self.Load_qss()

    # ================ Estilo ===================
    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_goals.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            self.setStyleSheet(f.read())

    # ================ Lógica ===================

    def get_total_segundos(self):
        h = self.spin_box_hours.spin_box.value()
        m = self.spin_box_minutes.spin_box.value()
        s = self.spin_box_seconds.spin_box.value()
        return h * 3600 + m * 60 + s
        
    def set_time_in_seconds(self, total):
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        self.spin_box_hours.spin_box.setValue(h)
        self.spin_box_minutes.spin_box.setValue(m)
        self.spin_box_seconds.spin_box.setValue(s)

    
    def iniciar_timer(self):
        self.value = self.get_total_segundos()
        if self.value > 0:
            print(f"Timer iniciado com {self.value} segundos.")
            self.timer_running = True
            self.button_start.setEnabled(False)
            self.button_pause.setEnabled(True)
            self.button_pause.setText("Pausar")
            self.timer.start()
        

    def atualizar_contagem(self):
        self.tempo_restante_segundos = self.get_total_segundos()
        if self.tempo_restante_segundos > 0:
            self.tempo_restante_segundos -= 1
            self.set_time_in_seconds(self.tempo_restante_segundos)
        else:
            self.timer.stop()
            self.reset_timer()
            print("Time's up")


    def pause_timer(self):
        if self.timer_running:
            self.timer.stop()
            print("Timer pausado.")
            self.timer_running = False
        else:
            self.timer.start()
            print("Timer retomado.")
            self.timer_running = True

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.set_time_in_seconds(0)
        print("Timer resetado.")

        self.button_start.setEnabled(True)
        self.button_pause.setEnabled(False)
        self.button_pause.setText("Pausar")


