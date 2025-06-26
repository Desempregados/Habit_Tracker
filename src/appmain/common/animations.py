from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QPoint,
    QParallelAnimationGroup,
    QSize,
    QSequentialAnimationGroup,
)
import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout


class AnimationsPos(QPropertyAnimation):
    def __init__(
        self,
        widget: QWidget,
        delta: tuple[int, int] = (0, -50),
        duration: int = 1000,
        parent=None,
    ):
        super().__init__(widget, b"pos", parent)

        self.delta_pos = QPoint(delta[0], delta[1])
        self.setDuration(duration)
        self.setEndValue(widget.pos() + self.delta_pos)
        self.setEasingCurve(QEasingCurve(QEasingCurve.Type.InOutCubic))


class AnimationsSize(QParallelAnimationGroup):
    def __init__(
        self,
        widget: QWidget,
        delta: tuple[int, int] = (20, 10),
        duration: int = 1000,
        parent=None,
    ):
        super().__init__(parent)

        self.delta_size = QSize(delta[0], delta[1])
        self.animation_size = QPropertyAnimation(widget, b"size", parent)
        self.animation_size.setDuration(duration)
        self.animation_size.setEndValue(widget.size() + self.delta_size)
        self.animation_size.setEasingCurve(QEasingCurve(QEasingCurve.Type.InOutCubic))

        self.og_pos = widget.pos()

        self.new_pos = self.og_pos - QPoint(
            self.delta_size.width() // 2, self.delta_size.height() // 2
        )

        self.animation_pos = QPropertyAnimation(widget, b"pos", parent)
        self.animation_pos.setDuration(duration)
        self.animation_pos.setEndValue(self.new_pos)
        self.animation_pos.setEasingCurve(QEasingCurve(QEasingCurve.Type.InOutCubic))

        self.addAnimation(self.animation_pos)
        self.addAnimation(self.animation_size)


class AnimationsPulse(QSequentialAnimationGroup):
    def __init__(
        self,
        widget,
        delta: tuple[int, int] = (50, 50),
        duration: int = 200,
        parent=None,
    ):
        super().__init__(parent)

        self.first_part = AnimationsSize(widget, (delta[0], delta[1]), duration)
        self.seocond_part = AnimationsSize(widget, (0, 0), duration)

        self.addAnimation(self.first_part)
        self.addAnimation(self.seocond_part)


class AppTeste(QWidget):
    def __init__(self):
        super().__init__()
        self.button_test = QPushButton("Test")
        self.layout_test = QVBoxLayout()
        self.setLayout(self.layout_test)
        self.layout_button = QHBoxLayout()
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.button_test)
        self.layout_button.addStretch(1)
        self.layout_test.addLayout(self.layout_button)
        self.button_test.setStyleSheet(
            """
        QPushButton{
        font-size: 26px;
        font-weight: bold;
        border: 3px solid black;
        background-color: rgb(230,230,230);
        width: 400px;
        height: 100px;
        color: black;
        border-radius: 36px;
        }
        QPushButton:hover{
        background-color:rgb(210,210,210);
        }
        QPushButton:pressed{
        background-color:rgb(190,190,190);
        }
        """
        )
        self.button_test.clicked.connect(self.click_animation)

    def click_animation(self):
        self.animation_pulse = AnimationsPulse(self.button_test, (120, 100), 20)
        self.animation_pulse.finished.connect(self.enable_button)
        self.button_test.setEnabled(False)
        self.animation_pulse.start()

    def enable_button(self):
        self.button_test.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = AppTeste()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
