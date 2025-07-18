import sys
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from datetime import datetime
from appmain.database.read import (
    db_read_registry_info,
    db_obtain_skill_by_id,
    db_read_goal_name,
    db_obtain_all_registries_id,
)


class RegistryContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.valid = None
        self.layout_main = QHBoxLayout(self)
        self.setObjectName("registry_container")

        # ======================== Label skill ====================

        self.label_skill = QLabel("skill name")
        self.label_skill.setObjectName("label_skill_name")
        self.layout_main.addWidget(
            self.label_skill,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )

        # ======================== Label goal =====================

        self.label_goal = QLabel("goal")
        self.label_goal.setObjectName("label_goal")
        self.layout_main.addWidget(
            self.label_goal,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )

        # ======================== Label dedicated time ===========

        self.label_dedicated = QLabel("00:00:00")
        self.label_dedicated.setObjectName("label_dedicated")
        self.layout_main.addWidget(
            self.label_dedicated,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )
        # ======================== Label time =====================

        self.label_time = QLabel("00:00:00")
        self.label_time.setObjectName("label_time")
        self.layout_main.addWidget(
            self.label_time,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )

        self.setData(3)

    def setData(self, registry_id: int):
        data = (db_read_registry_info(registry_id))[0]
        skill_id = data["skill_id"]
        goal_id = data["goal_id"]
        registry_time = data["registry_time"]
        dedicated_time = self.form_time(data["dedicated_time"])

        form_registry_time = datetime.strptime(registry_time, "%Y-%m-%d %H:%M:%S")

        skill_name = db_obtain_skill_by_id(skill_id)
        if goal_id:
            goal_name = db_read_goal_name(goal_id)
        else:
            goal_name = "no goal"

        if form_registry_time.day == datetime.now().day:
            self.label_skill.setText(skill_name)
            self.label_goal.setText(goal_name)
            self.label_time.setText(registry_time)
            self.label_dedicated.setText(dedicated_time)
            self.valid = True
        else:
            self.valid = False

    def form_time(self, s: int) -> str:
        return f"{int(s // 3600):02d}:{int((s // 60) % 60):02d}:{int(s % 60):02d}"


class TodayActivities(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.containers = []

        # ======================== Label Today activities ========

        self.label_today = QLabel("Today Activities")
        self.label_today.setObjectName("label_today")
        self.layout_main.addWidget(
            self.label_today, alignment=Qt.AlignmentFlag.AlignCenter, stretch=0
        )

        # ======================== Scroll area setup ==============

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area_today")
        self.scroll_area.setWidgetResizable(True)

        self.widget_scroll = QWidget()
        self.widget_scroll.setObjectName("widget_scroll_today")
        self.layout_scroll = QGridLayout()
        self.widget_scroll.setLayout(self.layout_scroll)
        self.scroll_area.setWidget(self.widget_scroll)
        self.layout_main.addWidget(self.scroll_area, stretch=1)

        # ========================= Label skill ====================

        self.label_skill = QLabel("skill")
        self.label_skill.setObjectName("label_header_skill")
        self.layout_scroll.addWidget(
            self.label_skill,
            0,
            0,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # ========================= Label skill ====================

        self.label_goal = QLabel("goal")
        self.label_goal.setObjectName("label_header_goal")
        self.layout_scroll.addWidget(
            self.label_goal,
            0,
            1,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # ========================= Label skill ====================

        self.label_dedicated_time = QLabel("dedicated_time")
        self.label_dedicated_time.setObjectName("label_header_dedicated")
        self.layout_scroll.addWidget(
            self.label_dedicated_time,
            0,
            2,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # ========================= Label skill ====================

        self.label_time = QLabel("time")
        self.label_time.setObjectName("label_header_time")
        self.layout_scroll.addWidget(
            self.label_time,
            0,
            3,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        self.loadContainers()
        self.resizeEvent(None)

    def loadContainers(self):
        r = 1
        registries_id = db_obtain_all_registries_id()
        for i in registries_id:
            container = RegistryContainer()
            container.setData(i)
            if container.valid:
                self.layout_scroll.addWidget(container, r, 0, 1, 4)
                self.containers.append(container)
                r += 1

        self.layout_scroll.setRowStretch(r, 2)

    def resizeEvent(self, event):
        viewport_height = self.scroll_area.viewport().height()
        if self.containers:
            target_height = viewport_height / 6.5
            for container in self.containers:
                container.setMinimumHeight(int(target_height))

        super().resizeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = TodayActivities()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
