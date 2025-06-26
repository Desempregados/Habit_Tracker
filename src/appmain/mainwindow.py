import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
)
from appmain.common.shadows import AppShadows
from appmain.features.pomodoro.pomogui import Janela
from appmain.features.greeting.greeting import Greeting


class main_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit tracker")
        self.setGeometry(500, 500, 500, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)
        self.setObjectName("MainWindow")

        self.shadow1 = AppShadows((0, 255, 159, 255), 45)

        bosta = "allan"
        self.layout_botao_abrir = QHBoxLayout()
        self.button_back_title = QPushButton("<-")

        self.button_back_title.setGraphicsEffect(self.shadow1)

        self.layout_botao_abrir.addWidget(self.button_back_title)
        self.button_back_title.hide()

        self.layout_botao_abrir.addStretch(1)
        self.button_open_pomo = QPushButton("Pomodoro")
        self.shadow2 = AppShadows((0, 255, 159), 35)
        self.button_open_pomo.setGraphicsEffect(self.shadow2)
        self.layout_botao_abrir.addWidget(self.button_open_pomo)
        self.layout_botao_abrir.addStretch(1)
        self.layout_principal.addLayout(self.layout_botao_abrir)

        self.stackedwidget = QStackedWidget()
        self.janela1 = Greeting()
        self.janela2 = Janela()
        self.stackedwidget.addWidget(self.janela1)
        self.stackedwidget.addWidget(self.janela2)
        self.layout_principal.addWidget(self.stackedwidget)

        self.connections()
        self.initUI()

    def connections(self):
        self.button_open_pomo.clicked.connect(self.window_open)
        self.button_back_title.clicked.connect(self.back_title)

    def initUI(self):
        self.setStyleSheet(
            """
        #MainWindow {
        background-color:rgb(30,30,30);
        }
        """
        )
        self.button_open_pomo.setStyleSheet(
            """
        #MainWindow QPushButton{
        color:white;
        font-size: 40px;
        font-family: Hack;
        font-weight:bold;
        border:2px solid rgba(190,134,255,1);
        border-radius: 32px;
        background-color:rgba(0,255,159,0.2);
        padding:10px;
        }
        #MainWindow QPushButton:hover{
        background-color:rgba(0,255,159,0.4);
        }
       #MainWindow QPushButton:pressed{
        background-color:rgba(0,255,159,0.6);
        }
        """
        )

        self.button_back_title.setStyleSheet(
            """
       #MainWindow QPushButton{
        color:white;
        font-size: 20px;
        font-family: Hack;
        font-weight:bold;
        border:2px solid rgba(190,134,255,1);
        border-radius: 32px;
        background-color:rgba(0,255,159,0.2);
        padding:10px;
        width:60px;
        height:40px;
        }
       #MainWindow QPushButton:hover{
        background-color:rgba(0,255,159,0.4);
        }
       #MainWindow QPushButton:pressed{
        background-color:rgba(0,255,159,0.6);
        }
        """
        )

    def window_open(self):
        self.stackedwidget.setCurrentIndex(1)
        self.button_open_pomo.hide()
        self.button_back_title.show()

    def back_title(self):
        self.stackedwidget.setCurrentIndex(0)
        self.button_open_pomo.show()
        self.button_back_title.hide()


def main():
    app = QApplication(sys.argv)
    window = main_app()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
