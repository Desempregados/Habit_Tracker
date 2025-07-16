# main_calendar.py
import sys
import calendar
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QHeaderView,
)
from PyQt6.QtCore import Qt


class CustomCalendar(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Configurações da Janela Principal ---
        self.setWindowTitle("Calendário Customizado com QTableWidget")
        self.setGeometry(100, 100, 700, 500)

        # Armazena a data atual que estamos visualizando
        self.current_date = datetime.now()

        # --- Layouts e Widgets ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 1. Layout de Navegação (Botões e Label do Mês)
        nav_layout = QHBoxLayout()

        self.prev_button = QPushButton("< Anterior")
        self.prev_button.clicked.connect(self.show_previous_month)

        self.month_year_label = QLabel()
        self.month_year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Adicionando um pouco de estilo para o label ficar mais destacado
        self.month_year_label.setStyleSheet("font-size: 16pt; font-weight: bold;")

        self.next_button = QPushButton("Próximo >")
        self.next_button.clicked.connect(self.show_next_month)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.month_year_label)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)

        # 2. Widget da Tabela (o Calendário em si)
        self.calendar_table = QTableWidget()
        self.calendar_table.setColumnCount(7)  # 7 dias da semana
        self.calendar_table.setRowCount(6)  # Máximo de 6 semanas em um mês

        # --- Estilização da Tabela ---
        # Esconde os cabeçalhos de linha e coluna (números)
        self.calendar_table.verticalHeader().setVisible(False)
        # self.calendar_table.horizontalHeader().setVisible(False) # Descomente se não quiser os dias da semana

        # Ajusta as colunas para preencher o espaço disponível
        header = self.calendar_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Preenche o calendário com a data atual
        self.populate_calendar()

        # Adiciona os layouts e widgets ao layout principal
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.calendar_table)

    def populate_calendar(self):
        """
        Preenche o QTableWidget com os dias do mês/ano armazenados
        em self.current_date.
        """
        year = self.current_date.year
        month = self.current_date.month

        # Atualiza o label com o mês e ano
        # Usando a formatação do strftime para obter o nome do mês em português
        month_name = self.current_date.strftime("%B").capitalize()
        self.month_year_label.setText(f"{month_name} de {year}")

        # Define os cabeçalhos dos dias da semana
        days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        self.calendar_table.setHorizontalHeaderLabels(days_of_week)

        # O calendar do python por padrão começa a semana na Segunda (0)
        calendar.setfirstweekday(calendar.MONDAY)
        month_calendar = calendar.monthcalendar(year, month)

        # Limpa a tabela antes de popular (importante para navegação)
        self.calendar_table.clearContents()

        # Itera sobre a matriz do calendário e preenche a tabela
        for week_index, week in enumerate(month_calendar):
            for day_index, day in enumerate(week):
                if day == 0:
                    # Célula vazia para dias de fora do mês
                    self.calendar_table.setItem(
                        week_index, day_index, QTableWidgetItem("")
                    )
                    continue

                # Cria o item da tabela com o número do dia
                day_item = QTableWidgetItem(str(day))
                day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # --- Customização (aqui a mágica acontece) ---
                # Exemplo: Desabilitar dias que não são do mês (melhor do que deixar em branco)
                day_item.setFlags(day_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                # Exemplo: Colorir o dia de hoje
                today = datetime.now()
                if year == today.year and month == today.month and day == today.day:
                    font = day_item.font()
                    font.setBold(True)
                    day_item.setFont(font)
                    day_item.setBackground(Qt.GlobalColor.lightGray)

                self.calendar_table.setItem(week_index, day_index, day_item)

    def show_previous_month(self):
        """Navega para o mês anterior."""
        current_year = self.current_date.year
        current_month = self.current_date.month

        # Lógica para voltar o mês e o ano
        if current_month == 1:
            new_month = 12
            new_year = current_year - 1
        else:
            new_month = current_month - 1
            new_year = current_year

        self.current_date = self.current_date.replace(
            year=new_year, month=new_month, day=1
        )
        self.populate_calendar()

    def show_next_month(self):
        """Navega para o próximo mês."""
        current_year = self.current_date.year
        current_month = self.current_date.month

        # Lógica para avançar o mês e o ano
        if current_month == 12:
            new_month = 1
            new_year = current_year + 1
        else:
            new_month = current_month + 1
            new_year = current_year

        self.current_date = self.current_date.replace(
            year=new_year, month=new_month, day=1
        )
        self.populate_calendar()


# --- Execução da Aplicação ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomCalendar()
    window.show()
    sys.exit(app.exec())
