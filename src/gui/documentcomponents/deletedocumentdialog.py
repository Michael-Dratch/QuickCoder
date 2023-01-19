from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QVBoxLayout, QLabel


class DeleteDocumentDialog(QDialog):
    def __init__(self, docName):
        super().__init__()
        self.setWindowTitle("Delete Document")
        self.docName = docName

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Cancel'), QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(QPushButton('Delete'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to delete {}?""".format(docName))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

