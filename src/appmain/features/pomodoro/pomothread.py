from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QCoreApplication
import sys


class Perfil_pomodoro(QObject):
    sinal_tempo = pyqtSignal(str)
    sinal_parar_tempo = pyqtSignal()
    sinal_ciclo_estado = pyqtSignal(str)
    sinal_current_cycle = pyqtSignal(str)
    sinal_dedicated_time = pyqtSignal(int)

    def __init__(
        self,
        len_work: int = 25,
        len_short: int = 5,
        len_long: int = 15,
        len_cycle: int = 3,
        parent=None,
    ):
        super().__init__(parent)
        self.len_work: int = len_work
        self.len_short: int = len_short
        self.len_long: int = len_long
        self.len_cycle: int = len_cycle
        self.left_time: int = self.min_sec(self.len_work)
        self.time_dedicated: int = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.countdown)

        self.current_cycle: str = "Work"
        self.completed_cycles: int = 1
        self.full_pomodoros: int = 1

    def min_sec(self, t: int) -> int:
        return int(t * 60)

    def form_time(self, s: int) -> str:
        return f"{int(s // 60):02d}:{int(s % 60):02d}"

    def pomo_start(self) -> None:
        self.timer.start(1000)
        self.sinal_tempo.emit(self.form_time(self.left_time))

    def pomo_pause(self) -> None:
        if self.timer.isActive():
            self.timer.stop()

    def pomo_restart(self) -> None:
        if self.current_cycle == "Work":
            self.left_time = self.min_sec(self.len_work)

        elif self.current_cycle == "Short Break":
            self.left_time = self.min_sec(self.len_short)

        elif self.current_cycle == "Long Break":
            self.left_time = self.min_sec(self.len_long)

    def pomo_skip(self) -> None:
        self.next_cycle()
        self.pomo_restart()

    def next_cycle(self):
        if (self.current_cycle == "Work") and (
            self.completed_cycles % self.len_cycle == 0
        ):
            self.current_cycle = "Long Break"
            self.left_time = self.min_sec(self.len_long)
            self.sinal_tempo.emit(self.form_time(self.left_time))
            self.completed_cycles += 1
            self.full_pomodoros += 1
            self.sinal_current_cycle.emit(f"{self.len_cycle}/{self.len_cycle}")

        elif self.current_cycle == "Work":
            self.current_cycle = "Short Break"
            self.left_time = self.min_sec(self.len_short)
            self.sinal_tempo.emit(self.form_time(self.left_time))
            self.completed_cycles += 1
            self.sinal_current_cycle.emit(
                f"{(self.completed_cycles - 1) % self.len_cycle}/{self.len_cycle}"
            )

        elif self.current_cycle == "Short Break":
            self.current_cycle = "Work"
            self.left_time = self.min_sec(self.len_work)
            self.sinal_tempo.emit(self.form_time(self.left_time))

        elif self.current_cycle == "Long Break":
            self.current_cycle = "Work"
            self.left_time = self.min_sec(self.len_work)
            self.sinal_tempo.emit(self.form_time(self.left_time))
            self.sinal_current_cycle.emit(f"0/{self.len_cycle}")

    def countdown(self) -> None:
        self.left_time -= 1
        self.time_dedicated += 1
        self.sinal_tempo.emit(self.form_time(self.left_time))

        if self.left_time <= 0:
            self.timer.stop()
            self.next_cycle()
            self.sinal_parar_tempo.emit()
            self.time_dedicated = 0

    def pomo_profile_change(
        self, new_work_len, new_short_break, new_long_break, new_cycle_len
    ):
        self.len_short = new_short_break
        self.len_long = new_long_break
        self.len_work = new_work_len
        self.len_cycle = new_cycle_len
        self.pomo_restart


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    p1 = Perfil_pomodoro(0.05, 10, 1, 3)
    p1.pomo_profile_change(1, 1, 1, 1)
    p1.sinal_tempo.connect(
        lambda tempo_str: print(f"GUI (simulada) display: {tempo_str}")
    )
    p1.sinal_ciclo_estado.connect(
        lambda ciclo: print(f"Sinal de ciclo concluído: {ciclo}")
    )

    p1.pomo_start()
    sys.exit(app.exec())
