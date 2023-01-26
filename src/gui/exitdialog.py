from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QVBoxLayout, QLabel


class ExitDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exit Quick Code")
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Back'), QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(QPushButton('Exit'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to exit?""")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
