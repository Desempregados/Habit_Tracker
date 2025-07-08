import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
)
from PyQt6.QtCore import QTimer

from timer_logic import TimerLogic


class TimeSelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)

        self.hours = QSpinBox()
        self.hours.setRange(0, 23)
        self.hours.setSuffix(" h")
        self.hours.setFixedWidth(70)

        self.minutes = QSpinBox()
        self.minutes.setRange(0, 59)
        self.minutes.setSuffix(" m")
        self.minutes.setFixedWidth(70)

        self.seconds = QSpinBox()
        self.seconds.setRange(0, 59)
        self.seconds.setSuffix(" s")
        self.seconds.setFixedWidth(70)

        layout.addWidget(self.hours)
        layout.addWidget(self.minutes)
        layout.addWidget(self.seconds)
        self.setLayout(layout)
        layout.addStretch(1)

    def get_total_seconds(self):
        return (
            self.hours.value() * 3600 + self.minutes.value() * 60 + self.seconds.value()
        )

    def set_time_in_seconds(self, total_seconds):
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        self.hours.setValue(h)
        self.minutes.setValue(m)
        self.seconds.setValue(s)

    def setEnabled(self, enabled):
        self.hours.setEnabled(enabled)
        self.minutes.setEnabled(enabled)
        self.seconds.setEnabled(enabled)


class TimerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer")
        self.setGeometry(100, 100, 350, 150)

        self.logic = TimerLogic()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_countdown)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.time_selector = TimeSelectorWidget()
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        button_layout.addWidget(self.reset_button)

        main_layout.addWidget(self.time_selector)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def start_timer(self):
        total_seconds = self.time_selector.get_total_seconds()
        if self.logic.start(total_seconds):
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.pause_button.setText("Pause")
            self.time_selector.setEnabled(False)
            self.timer.start()

    def pause_timer(self):
        if self.logic.timer_running:
            self.logic.pause()
            self.timer.stop()
            self.pause_button.setText("Resume")
        else:
            self.logic.resume()
            self.timer.start()
            self.pause_button.setText("Pause")

    def reset_timer(self):
        self.timer.stop()
        self.logic.reset()
        self.time_selector.set_time_in_seconds(0)
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.time_selector.setEnabled(True)

    def update_countdown(self):
        finished = self.logic.tick()
        self.time_selector.set_time_in_seconds(self.logic.remaining_time_seconds)
        if finished:
            self.timer.stop()
            self.reset_timer()
            print("Time's up!")


def main():
    app = QApplication(sys.argv)
    window = TimerUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
