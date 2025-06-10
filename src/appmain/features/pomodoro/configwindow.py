import sys
from PyQt6.QtWidgets import QDialog,QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QApplication, QGridLayout, QSpinBox
from PyQt6.QtCore import Qt
from appmain.common.shadows import AppShadows
from appmain import assets

class ConfigWindow(QDialog):
    def __init__(self, parent = None):

        # ======================= boilerplate =====================

        super().__init__(parent)
        self.setWindowTitle("Configurations")
        self.setGeometry(700, 500, 300, 200)
        self.setObjectName("ConfigWindow")

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # ===================== Label Title =======================

        self.shadow_lable = AppShadows((0, 255, 159), 35)
        self.label_titulo = QLabel("Configurations")
        self.label_titulo.setGraphicsEffect(self.shadow_lable)
        self.layout_principal.addStretch(1)
        self.layout_principal.addWidget(self.label_titulo)

        # ===================== Config options ====================

        # ----- Declare buttons ------

        self.layout_config = QGridLayout()
        self.box_work = QSpinBox()
        self.box_short = QSpinBox()
        self.box_long = QSpinBox()
        self.box_cycle = QSpinBox()

        # ---- Minimum and maximum values ------
        self.box_work.setMinimum(1)
        self.box_short.setMinimum(1)
        self.box_long.setMinimum(1)
        self.box_cycle.setMinimum(1)

        self.box_work.setMaximum(120)
        self.box_short.setMaximum(120)
        self.box_long.setMaximum(120)
        self.box_cycle.setMaximum(10)

        # ---- Placeholder text and initial value ----

        self.box_work.setSuffix(" mins")
        self.box_short.setSuffix(" mins")
        self.box_long.setSuffix(" mins")
        self.box_cycle.setSuffix(" cycles")
        self.box_work.setValue(25)
        self.box_short.setValue(5)
        self.box_long.setValue(15)
        self.box_cycle.setValue(3)

        # ---- Labels for the boxes ----

        self.label_work = QLabel("Work lenght")
        self.label_short = QLabel("Short Break")
        self.label_long = QLabel("Long Break")
        self.label_cycle = QLabel("Cycles")

        # ---- Positions of the widgets -----

        self.layout_config.addWidget(self.label_work, 0, 1)
        self.layout_config.addWidget(self.label_short, 1, 1)
        self.layout_config.addWidget(self.label_long, 2, 1)
        self.layout_config.addWidget(self.label_cycle, 3, 1)
        self.layout_config.addWidget(self.box_work, 0, 2)
        self.layout_config.addWidget(self.box_short, 1, 2)
        self.layout_config.addWidget(self.box_long, 2, 2)
        self.layout_config.addWidget(self.box_cycle, 3, 2)
        self.layout_config.setColumnStretch(0, 1)
        self.layout_config.setColumnStretch(3, 1)
        self.layout_principal.addLayout(self.layout_config)
        self.layout_principal.addStretch(1)

        # ==================== Save and cancel buttons =========

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addStretch(1)
        self.button_save = QPushButton("Save")
        self.button_save.setObjectName("Savebutton")
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setObjectName("Cancelbutton")
        self.layout_buttons.addWidget(self.button_save)
        self.layout_buttons.addStretch(1)
        self.layout_buttons.addWidget(self.button_cancel)
        self.layout_buttons.addStretch(1)
        self.layout_principal.addLayout(self.layout_buttons)
        self.layout_principal.addStretch(1)

        # ==================== Buttons signals =====================

        self.button_save.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        # ==================== Essential functions start ===========

        self.setUI()

    def setUI(self):

        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
        #ConfigWindow {{
        background-color:rgba(30,30,30,1);
        }}
        #ConfigWindow QLabel{{
        color:white;
        font-size: 40px;
        font-weight: bold;
        font-family: Hack;
        }}
        #ConfigWindow QSpinBox{{
        background-color:gray;
        border-radius:16px;
        padding:13px;
        font-size:20px;
        }}
        #ConfigWindow QSpinBox::up-button, QSpinBox::down-button {{
        background-color:transparent;
        width:30px;
        }}
       #ConfigWindow QSpinBox::up-arrow{{
        image:url({str(assets.get_path_asset("icons/arrow-up.svg"))});
        width:26px;
        height:26px;
        }}
       #ConfigWindow QSpinBox::down-arrow{{
        image:url({str(assets.get_path_asset("icons/arrow-down.svg"))});
        width:26px;
        height:26px;
        }}
       #ConfigWindow QLabel{{
        font-size:24px;
        }}
       #ConfigWindow QPushButton{{
        color:white;
        font-size:24px;
        border-radius:22px;
        width:170px;
        height:70px;
        border:None;
        }}

       #ConfigWindow QPushButton#Savebutton{{
        background-color:#72E098;
        }}

       #ConfigWindow QPushButton#Savebutton:pressed{{
        background-color:#19E069;
        }}

       #ConfigWindow QPushButton#Cancelbutton{{
        background-color:#E05959;
        }}

       #ConfigWindow QPushButton#Cancelbutton:pressed{{
        background-color:#E03642;
        }}

        """)

    def get_settings(self):
        settings = {"work": self.box_work.value(),
                         "short_break": self.box_short.value(),
                         "long_break": self.box_long.value(),
                         "cylcles_number": self.box_cycle.value()}

        return settings


def main():
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
