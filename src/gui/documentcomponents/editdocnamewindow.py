from functools import partial

from PyQt6.QtWidgets import QLabel

from src.gui.documentcomponents.documentwindowbase import DocumentWindowBase


class EditCodeNameWindow(DocumentWindowBase):
    def __init__(self, doc, documents, saveNameHandler, changeDocLabelHandler):
        super().__init__()
        self.nameField.setText(doc.name)
        self.saveButton.clicked.connect(partial(self.saveNameClicked,
                                                doc,
                                                documents,
                                                self.nameField,
                                                saveNameHandler,
                                                changeDocLabelHandler))

    def saveNameClicked(self, doc, documents, saveNameHandler, changeDocLabelHandler):
        newName = self.nameField.text()
        if newName == '':
            return
        if self.nameExists(newName, documents):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Document name already exists'))
                self.errorMessageShowing = True
        else:
            saveNameHandler(doc, newName)
            changeDocLabelHandler(doc, newName)
            self.close()

