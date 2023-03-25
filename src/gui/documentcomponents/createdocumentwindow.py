from functools import partial

from PyQt6.QtWidgets import QLabel

from src.gui.documentcomponents.documentwindowbase import DocumentWindowBase


class CreateDocumentWindow(DocumentWindowBase):
    def __init__(self, createDocHandler):
        super().__init__()
        self.createDocHandler = createDocHandler
        self.saveButton.setText('Create New Document')
        self.saveButton.clicked.connect(self.saveNameClicked)

    def saveNameClicked(self):
        newName = self.nameField.text()
        if newName == '':
            return
        else:
            self.callCreateDocHandler(newName)
            self.close()

    def callCreateDocHandler(self, newName):
        self.createDocHandler(newName)


class CreateDocumentInFolderWindow(CreateDocumentWindow):
    def __init__(self, parentItem, createDocHandler):
        super().__init__(createDocHandler)
        self.parentItem = parentItem

    def callCreateDocHandler(self, newName):
        self.createDocHandler(self.parentItem, newName)

class CreateFolderWindow(DocumentWindowBase):
    def __init__(self, createFolderHandler):
        super().__init__()
        self.createFolderHandler = createFolderHandler
        self.saveButton.setText('Create New Folder')
        self.saveButton.clicked.connect(self.saveNameClicked)

    def saveNameClicked(self):
        newName = self.nameField.text()
        if newName == '':
            return
        else:
            self.callCreateFolderHandler(newName)
            self.close()

    def callCreateFolderHandler(self, newName):
        self.createDocHandler(newName)

class CreateFolderInFolderWindow(CreateFolderWindow):
    def __init__(self, parentItem, createFolderHandler):
        super().__init__(createFolderHandler)
        self.parentItem = parentItem

    def callCreateFolderHandler(self, newName):
        self.createFolderHandler(self.parentItem, newName)