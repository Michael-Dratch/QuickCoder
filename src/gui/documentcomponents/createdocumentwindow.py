from functools import partial

from PyQt6.QtWidgets import QLabel

from src.gui.documentcomponents.documentwindowbase import DocumentWindowBase


class CreateDocumentWindow(DocumentWindowBase):
    def __init__(self, documents, createDocHandler):
        super().__init__()
        self.saveButton.setText('Create New Document')
        self.saveButton.clicked.connect(partial(self.saveNameClicked,
                                                documents,
                                                createDocHandler))

    def saveNameClicked(self, documents, createDocHandler):
        newName = self.nameField.text()
        if newName == '':
            return
        if self.nameExists(newName, documents):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Document name already exists'))
                self.errorMessageShowing = True
        else:
            createDocHandler(newName)
            self.close()
