from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor


class AppShadows(QGraphicsDropShadowEffect):
    def __init__(
        self,
        color: tuple[int, int, int, int],
        intensity: int,
        offset: tuple[int, int] = (0, 0),
    ):
        super().__init__()
        self.color = color
        self.intensity = intensity
        self.offset = offset
        if len(color) == 3:
            self.setColor(QColor(color[0], color[1], color[2], 255))
        else:
            self.setColor(QColor(color[0], color[1], color[2], color[3]))
        self.setBlurRadius(intensity)
        self.setOffset(offset[0], offset[1])


if __name__ == "__main__":
    shadow = AppShadows((9, 9, 9), 23)
