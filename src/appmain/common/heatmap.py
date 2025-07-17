import sys
import calendar
from PyQt6.QtWidgets import (
    QApplication,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QAbstractItemView,
)
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtCore import Qt
from datetime import datetime
from appmain.database.read import db_obtain_all_registries_info


class Heatmap(QTableWidget):
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
        self.setStyleSheet(
            "background-color:rgb(50, 50, 50); color:white; font-weight:bold; font-size: 20px;"
        )
        self.current_date = datetime.now()
        # ================================= Table ======================

        self.setColumnCount(7)
        self.setRowCount(5)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)

        self.setHorizontalHeaderLabels(["S", "M", "T", "W", "T", "F", "S"])

        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # ================================== Initialize functions =============

        self.initCalendar(7)

    # ======================================= Set the calendar days ===========

    def initCalendar(self, month, year=datetime.now().year):
        self.clearContents()
        month_calendar = calendar.monthcalendar(year, month)

        for week_index, week in enumerate(month_calendar):
            for day_index, day in enumerate(week):
                if day == 0:
                    self.setItem(week_index, day_index, QTableWidgetItem(""))

                else:
                    day_item = QTableWidgetItem(str(day))
                    day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(week_index, day_index, day_item)

        self.initColors(month, year)

    def initColors(self, month, year):
        registries = db_obtain_all_registries_info()
        days = {}
        total_time = 0

        for registry in registries:
            day = registry["registry_time"]
            time = registry["dedicated_time"]

            formated_time = datetime.strptime(day, "%Y-%m-%d %H:%M:%S")

            if (formated_time.month == month) and (formated_time.year == year):
                total_time += time
                form_day = str(formated_time.day)

                if form_day in days:
                    days[form_day] = days[form_day] + time
                else:
                    days[form_day] = time

        max_value = max(days.values())
        mean = total_time // len(days)
        i_step = mean // 2
        s_step = (max_value + mean) // 2

        for i in range(5):
            for j in range(7):
                item = self.item(i, j)
                text = str(item.text())
                if text == "":
                    background = QColor(45, 45, 45)
                    brush = QBrush(background)
                    item.setBackground(brush)

                elif int(text) == 0:
                    continue

                elif text in days:
                    if days[text] <= i_step:
                        item.setBackground(self.brush1)

                    elif days[text] <= mean:
                        item.setBackground(self.brush2)

                    elif days[text] <= s_step:
                        item.setBackground(self.brush3)

                    elif days[text] < max_value:
                        item.setBackground(self.brush4)

                    else:
                        item.setBackground(self.brush5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Heatmap()
    window.show()
    sys.exit(app.exec())
