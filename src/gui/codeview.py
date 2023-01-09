from PyQt6.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QWidget

class CodeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,100,600)
        self.setMaximumWidth(200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Code View"))
