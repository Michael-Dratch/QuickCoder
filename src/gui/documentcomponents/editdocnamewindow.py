from functools import partial

from PyQt6.QtWidgets import QLabel

from src.gui.documentcomponents.documentwindowbase import DocumentWindowBase


class EditDocNameWindow(DocumentWindowBase):
    def __init__(self, item, docName, docID, saveNameHandler, changeDocLabelHandler):
        super().__init__()
        self.nameField.setText(docName)
        self.setWindowTitle('Change Document Name')
        self.saveButton.clicked.connect(partial(self.saveNameClicked,
                                                item,
                                                docID,
                                                saveNameHandler,
                                                changeDocLabelHandler))

    def saveNameClicked(self, item, docID, saveNameHandler, changeDocLabelHandler):
        newName = self.nameField.text()
        if newName == '':
            return
        else:
            saveNameHandler(docID, newName)
            changeDocLabelHandler(item, newName)
            self.close()


class EditFolderNameWindow(DocumentWindowBase):
    def __init__(self, item, docName, changeFolderLabelHandler):
        super().__init__()
        self.nameField.setText(docName)
        self.setWindowTitle('Change Folder Name')
        self.saveButton.clicked.connect(partial(self.saveNameClicked,
                                                item,
                                                changeFolderLabelHandler))

    def saveNameClicked(self, item, changeFolderLabelHandler):
        newName = self.nameField.text()
        if newName == '':
            return
        else:
            changeFolderLabelHandler(item, newName)
            self.close()
