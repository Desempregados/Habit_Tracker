from time import sleep
from PyQt6.QtCore import pyqtSignal, QTimer


class Timer:
    def __init__(self):
        super().__init__()
        self.segundos, self.minutos, self.horas = 0,0,0
        self.running = False
        
    def start_timer(self):
        self.running = True
        while self.running:
            try:
                sleep(1)
                self.segundos += 1
                if self.segundos == 60:
                    self.segundos = 0
                    self.minutos +=1
                if self.minutos == 60:
                    self.minutos = 0
                    self.horas += 1
                self.update()
            except KeyboardInterrupt:
                self.pause_timer()


    def update(self):
        print(f"{self.horas}:{self.minutos}:{self.segundos}")


    def pause_timer(self):
        try:
            while True:
                self.running = False
        except KeyboardInterrupt:
            self.start_timer()


Timer().start_timer()

