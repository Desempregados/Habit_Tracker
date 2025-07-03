import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox
)
from PyQt6.QtCore import QTimer


class TimeSelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # --- Hours ---
        self.hours = QSpinBox()
        self.hours.setRange(0, 23)
        self.hours.setSuffix(" h")
        self.hours.setFixedWidth(70)

        # --- Minutes ---
        self.minutes = QSpinBox()
        self.minutes.setRange(0, 59)
        self.minutes.setSuffix(" m")
        self.minutes.setFixedWidth(70)

        # --- Seconds ---
        self.seconds = QSpinBox()
        self.seconds.setRange(0, 59)
        self.seconds.setSuffix(" s")
        self.seconds.setFixedWidth(70)

        layout.addWidget(self.hours)
        layout.addWidget(self.minutes)
        layout.addWidget(self.seconds)

        self.setLayout(layout)

    def get_total_seconds(self):
        return (self.hours.value() * 3600 +
                self.minutes.value() * 60 +
                self.seconds.value())

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

        self.setWindowTitle('Timer')
        self.setGeometry(100, 100, 350, 150)

        self.remaining_time_seconds = 0
        self.timer_running = False

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
        self.remaining_time_seconds = self.time_selector.get_total_seconds()

        if self.remaining_time_seconds > 0:
            self.timer_running = True
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.pause_button.setText("Pause")
            self.time_selector.setEnabled(False)
            self.timer.start()

    def pause_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.pause_button.setText("Resume")
        else:
            self.timer.start()
            self.timer_running = True
            self.pause_button.setText("Pause")

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.remaining_time_seconds = 0

        self.time_selector.set_time_in_seconds(0)

        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.time_selector.setEnabled(True)

    def update_countdown(self):
        if self.remaining_time_seconds > 0:
            self.remaining_time_seconds -= 1
            self.time_selector.set_time_in_seconds(self.remaining_time_seconds)
        else:
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