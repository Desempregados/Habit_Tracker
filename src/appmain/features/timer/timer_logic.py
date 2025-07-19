from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSpinBox


class SeletorDeTempoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "CustomSpinBox")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.horas = QSpinBox()
        self.horas.setRange(0, 23)
        self.horas.setSuffix(" h")
        self.horas.setFixedWidth(70)

        self.minutos = QSpinBox()
        self.minutos.setRange(0, 59)
        self.minutos.setSuffix(" m")
        self.minutos.setFixedWidth(70)

        self.segundos = QSpinBox()
        self.segundos.setRange(0, 59)
        self.segundos.setSuffix(" s")
        self.segundos.setFixedWidth(70)

        layout.addWidget(self.horas)
        layout.addWidget(self.minutos)
        layout.addWidget(self.segundos)

        self.setLayout(layout)

    def get_total_segundos(self):
        return (self.horas.value() * 3600 +
                self.minutos.value() * 60 +
                self.segundos.value())

    def set_tempo_em_segundos(self, total_segundos):
        h = total_segundos // 3600
        m = (total_segundos % 3600) // 60
        s = total_segundos % 60

        self.horas.setValue(h)
        self.minutos.setValue(m)
        self.segundos.setValue(s)

    def setEnabled(self, enabled):
        self.horas.setEnabled(enabled)
        self.minutos.setEnabled(enabled)
        self.segundos.setEnabled(enabled)
