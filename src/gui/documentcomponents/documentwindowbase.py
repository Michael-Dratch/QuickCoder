from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton


class DocumentWindowBase(QWidget):
    def __init__(self):
        super().__init__()
        self.errorMessageShowing = False
        self.nameField = QLineEdit()
        self.saveButton = QPushButton('save')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.nameField)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

    def nameExists(self, name, documents):
        for document in documents:
            if document.name == name:
                return True
        return False

