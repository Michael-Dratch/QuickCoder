from PyQt6.QtWidgets import QWidget


class ColorPanel(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setGeometry(0, 0, 10, 10)
        self.color = color
        self.setStyleSheet("""background-color: {}""".format(color))
