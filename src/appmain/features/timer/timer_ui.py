import sys
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import QTimer
from timer_dialog import TemporizadorDialog as SeletorDeTempoWidget


class TemporizadorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("NewGoalDialog")
        self.setWindowTitle('Temporizador Estilo Safira 2.0')
        self.setGeometry(100, 100, 350, 150)

        self.tempo_restante_segundos = 0
        self.timer_rodando = False

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.atualizar_contagem)

        self.inicializar_ui()
        self.Load_qss()

    def Load_qss(self):
        STYLE_DIR = Path(__file__).resolve().parent / "style_goals.qss"
        with open(STYLE_DIR, "r", encoding="UTF-8") as f:
            self.setStyleSheet(f.read())

    def inicializar_ui(self):
        main_layout = QVBoxLayout()

        self.seletor_tempo = SeletorDeTempoWidget()

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Iniciar")
        self.start_button.setObjectName("button_confirm")
        self.start_button.clicked.connect(self.iniciar_timer)

        self.pause_button = QPushButton("Pausar")
        self.pause_button.setObjectName("button_cancel")
        self.pause_button.clicked.connect(self.pausar_timer)
        self.pause_button.setEnabled(False)

        self.reset_button = QPushButton("Resetar")
        self.reset_button.setObjectName("button_cancel")
        self.reset_button.clicked.connect(self.resetar_timer)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addWidget(self.seletor_tempo)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def iniciar_timer(self):
        self.tempo_restante_segundos = self.seletor_tempo.get_total_segundos()

        if self.tempo_restante_segundos > 0:
            self.timer_rodando = True
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.pause_button.setText("Pausar")
            self.seletor_tempo.setEnabled(False)
            self.timer.start()

    def pausar_timer(self):
        if self.timer_rodando:
            self.timer.stop()
            self.timer_rodando = False
            self.pause_button.setText("Retomar")
        else:
            self.timer.start()
            self.timer_rodando = True
            self.pause_button.setText("Pausar")

    def resetar_timer(self):
        self.timer.stop()
        self.timer_rodando = False
        self.tempo_restante_segundos = 0

        self.seletor_tempo.set_tempo_em_segundos(0)

        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pausar")
        self.seletor_tempo.setEnabled(True)

    def atualizar_contagem(self):
        if self.tempo_restante_segundos > 0:
            self.tempo_restante_segundos -= 1
            self.seletor_tempo.set_tempo_em_segundos(self.tempo_restante_segundos)
        else:
            self.timer.stop()
            self.resetar_timer()
            print("O tempo acabou!")
