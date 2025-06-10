import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from appmain.common.shadows import AppShadows


class Greeting(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)
        self.setObjectName("Greeting")
        self.label_title = QLabel("Bem Vindo")
        self.label_title.setObjectName("GreetingLabel")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shadow = AppShadows((0, 255, 159), 25)
        self.label_title.setGraphicsEffect(self.shadow)
        self.layout_principal.addWidget(self.label_title)

        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"""
        #Greeting {{
        background-color :rgb(30, 30, 30);
        }}
        #Greeting QLabel{{
        font-size:140px;
        color:rgb(0,255,159);
        font-family:Hack;
        font-weight:bold;
        }}
        """)


def main():
    app = QApplication(sys.argv)
    window = Greeting()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
