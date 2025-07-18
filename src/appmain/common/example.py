import sys
import calendar
import random
from PyQt6.QtWidgets import (
    QApplication,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QAbstractItemView,
    QStyledItemDelegate,
)
from PyQt6.QtGui import QColor, QBrush, QPainter, QPen
from PyQt6.QtCore import Qt, QRectF
from datetime import datetime


# =============================================================================
# Mock da função de banco de dados CORRIGIDA
# Agora, ela gera dados para o ano e mês específicos que são passados como argumento.
# =============================================================================
def db_obtain_all_registries_info(year, month):
    """
    Gera dados de exemplo para popular o heatmap para um mês e ano específicos.
    No seu projeto real, você continuará usando sua função original.
    """
    registries = []
    # Pega o número de dias no mês/ano solicitado
    num_days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, num_days_in_month + 1):
        # Aumenta a chance de ter um registro no dia para ficar mais visível
        if random.random() > 0.2:  # 80% de chance
            num_registries_for_day = random.randint(1, 3)
            for _ in range(num_registries_for_day):
                registries.append(
                    {
                        "registry_time": f"{year}-{month:02d}-{day:02d} 10:00:00",
                        "dedicated_time": random.randint(5, 120),  # tempo em minutos
                    }
                )
    return registries


# =============================================================================
# Conteúdo do seu arquivo style.qss (sem alterações)
# =============================================================================
STYLE_QSS = """
QTableWidget {
    font-weight: 700;
    font-size: 16px;
    gridline-color: transparent;
    font-family: "Roboto";
    background-color: rgb(30, 30, 30);
    color: white;
    border: none;
    padding: 2px;
}

QHeaderView {
    background-color: rgb(30, 30, 30);
}

QHeaderView::section {
    color: white;
    border: none;
    background-color: rgb(30, 30, 30);
    font-family: "Roboto";
    font-size: 20px;
    font-weight: bold;
    padding: 5px;
}
"""


# =============================================================================
# QStyledItemDelegate para desenhar as células arredondadas (sem alterações)
# =============================================================================
class RoundedCellDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 10

    def paint(
        self,
        painter: QPainter,
        option,
        index,
    ):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        background_brush = index.data(Qt.ItemDataRole.BackgroundRole)
        text = index.data(Qt.ItemDataRole.DisplayRole)
        cell_rect = QRectF(option.rect).adjusted(2, 2, -2, -2)

        if background_brush is None:
            bg_color = QColor(40, 40, 40)
            painter.setBrush(bg_color)
        else:
            painter.setBrush(background_brush)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(cell_rect, self.radius, self.radius)

        if text:
            painter.setPen(QPen(Qt.GlobalColor.white))
            painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.restore()


class Heatmap(QTableWidget):
    # Definições de cores (sem alterações)
    color5 = QColor(0, 240, 139)
    color4 = QColor(color5)
    color3 = QColor(color5)
    color2 = QColor(color5)
    color1 = QColor(color5)

    color4.setAlphaF(0.8)
    color3.setAlphaF(0.6)
    color2.setAlphaF(0.4)
    color1.setAlphaF(0.2)

    brush5 = QBrush(color5)
    brush4 = QBrush(color4)
    brush3 = QBrush(color3)
    brush2 = QBrush(color2)
    brush1 = QBrush(color1)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = datetime.now()

        self.setColumnCount(7)
        self.setRowCount(6)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)

        # Ajustado para o padrão brasileiro (Domingo a Sábado)
        self.setHorizontalHeaderLabels(["D", "S", "T", "Q", "Q", "S", "S"])

        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setItemDelegate(RoundedCellDelegate(self))

        self.Load_qss()

        self.initCalendar(self.current_date.month, self.current_date.year)

    def Load_qss(self):
        self.setStyleSheet(STYLE_QSS)

    def initCalendar(self, month, year=datetime.now().year):
        self.clearContents()
        # Define o primeiro dia da semana como Domingo
        calendar.setfirstweekday(calendar.SUNDAY)
        month_calendar = calendar.monthcalendar(year, month)

        # Ajusta o número de linhas da tabela se necessário
        if len(month_calendar) != self.rowCount():
            self.setRowCount(len(month_calendar))

        for week_index, week in enumerate(month_calendar):
            for day_index, day in enumerate(week):
                if day != 0:
                    day_item = QTableWidgetItem(str(day))
                    day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(week_index, day_index, day_item)

        self.initColors(month, year)

    def initColors(self, month, year):
        # AQUI ESTÁ A MUDANÇA PRINCIPAL
        # Passa o ano e mês para a função que busca os dados
        registries = db_obtain_all_registries_info(year, month)
        days = {}
        total_time = 0

        # O resto da lógica permanece a mesma, mas agora ela vai encontrar os dados
        for registry in registries:
            day_str = registry["registry_time"]
            time = registry["dedicated_time"]
            formated_time = datetime.strptime(day_str, "%Y-%m-%d %H:%M:%S")

            if (formated_time.month == month) and (formated_time.year == year):
                total_time += time
                form_day = str(formated_time.day)
                days[form_day] = days.get(form_day, 0) + time

        # Adicionado para depuração: veja os dados que estão sendo usados
        print(f"Dados para colorir (Mês {month}/{year}): {days}")

        if not days:
            print(
                "Nenhum registro encontrado para este mês. As cores não serão aplicadas."
            )
            return

        max_value = max(days.values())
        mean = total_time / len(days)
        i_step = mean / 2
        s_step = (max_value + mean) / 2

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = self.item(i, j)
                if not item or not item.text():
                    continue

                text = item.text()
                # Define uma cor de fundo padrão para dias com registros, mas que podem
                # não se encaixar nas categorias, ou para dias sem registros.
                item.setBackground(QBrush(QColor(60, 60, 60)))

                if text in days:
                    value = days[text]
                    if value <= i_step:
                        item.setBackground(self.brush1)
                    elif value <= mean:
                        item.setBackground(self.brush2)
                    elif value <= s_step:
                        item.setBackground(self.brush3)
                    elif value < max_value:
                        item.setBackground(self.brush4)
                    else:
                        item.setBackground(self.brush5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Heatmap()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
